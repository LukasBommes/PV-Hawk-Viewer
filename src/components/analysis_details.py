from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Slot

from src.ui.ui_analysis_details import Ui_AnalysisDetails


class AnalysisDetailsView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # open in new window
        self.model = model
        self.controller = controller
        self.ui = Ui_AnalysisDetails()
        self.ui.setupUi(self)
        self.parent = parent
        # connect signals and slots
        self.ui.pushButtonClose.clicked.connect(self.close)
        self.model.meta_changed.connect(self.update)
        self.update()

    def to_display(self, text):
        """Converts a string of the form 'my_setting' to 'My Setting'."""
        return " ".join([str.capitalize(s) for s in str.split(text, "_")])

    def truncate_string(self, value, max_len=100):
        value = str(value)
        if len(value) > max_len:
            value = value[:max_len] + "..."
        return value

    @Slot()
    def update(self):  
        meta = self.model.meta
        if meta is None:
            self.ui.lineEditAnalysisType.setText("")
            self.ui.lineEditTimestamp.setText("")
            self.ui.lineEditDatasetPath.setText("")
            self.ui.listWidgetHyperparameters.clear()
            return

        self.ui.lineEditAnalysisType.setText(self.to_display(meta["type"]))
        self.ui.lineEditTimestamp.setText(meta["timestamp"])
        self.ui.lineEditDatasetPath.setText(meta["dataset_dir"])
        hyperparameters = [
            "{}: {}".format(self.to_display(name), self.truncate_string(value)) 
            for name, value 
            in meta["hyperparameters"].items()
        ]
        self.ui.listWidgetHyperparameters.clear()
        self.ui.listWidgetHyperparameters.addItems(hyperparameters)