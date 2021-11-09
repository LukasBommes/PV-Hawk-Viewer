
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt, Slot

from src.ui.ui_analysis_module_temperatures import Ui_ModuleTemperatures


class AnalysisModuleTemperaturesView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # open in new window
        self.model = model
        self.controller = controller
        self.parent = parent
        self.ui = Ui_ModuleTemperatures()
        self.ui.setupUi(self)
        self.reset()
        # connect signals and slots
        self.ui.pushButtonCompute.clicked.connect(self.controller.analysis_module_temperatures_controller.compute)
        self.ui.pushButtonCancel.clicked.connect(self.controller.analysis_module_temperatures_controller.cancel)
        self.ui.pushButtonOk.clicked.connect(self.close)
        self.model.analysis_module_temperatures_model.name_changed.connect(self.ui.nameLineEdit.setText)
        self.ui.nameLineEdit.textChanged.connect(lambda value: setattr(self.model.analysis_module_temperatures_model, 'name', value))
        self.model.analysis_module_temperatures_model.border_margin_changed.connect(self.ui.truncateWidthSpinBox.setValue)
        self.ui.truncateWidthSpinBox.valueChanged.connect(lambda value: setattr(self.model.analysis_module_temperatures_model, 'border_margin', value))
        self.model.analysis_module_temperatures_model.neighbor_radius_changed.connect(self.ui.neighborRadiusSpinBox.setValue)
        self.ui.neighborRadiusSpinBox.valueChanged.connect(lambda value: setattr(self.model.analysis_module_temperatures_model, 'neighbor_radius', value))
        self.model.analysis_module_temperatures_model.progress_changed.connect(self.ui.progressBar.setValue)
        self.model.analysis_module_temperatures_model.progress_text_changed.connect(self.ui.progressLabel.setText)

        self.controller.analysis_module_temperatures_controller.name_exists.connect(self.show_name_exist_dialog)
        self.model.analysis_module_temperatures_model.status_changed.connect(self.status_changed)

        # set default values
        self.controller.analysis_module_temperatures_controller.reset()

    def reset(self):
        self.ui.pushButtonOk.hide()
        self.ui.pushButtonCompute.show()
        self.ui.pushButtonCancel.setEnabled(False)
        self.ui.pushButtonCompute.setEnabled(True)
        self.ui.truncateWidthSpinBox.setEnabled(True)
        self.ui.neighborRadiusSpinBox.setEnabled(True)

    @Slot(object)
    def status_changed(self, status):
        if status is None:
            self.reset()
        elif status == "started":
            self.ui.pushButtonCancel.setEnabled(True)
            self.ui.pushButtonCompute.setEnabled(False)
            self.ui.truncateWidthSpinBox.setEnabled(False)
            self.ui.neighborRadiusSpinBox.setEnabled(False)
        elif status == "cancelled":
            self.ui.pushButtonCompute.hide()
            self.ui.pushButtonOk.show()
            self.ui.pushButtonCancel.setEnabled(False)
        elif status == "finished":
            self.ui.pushButtonCompute.hide()
            self.ui.pushButtonOk.show()
            self.ui.pushButtonCancel.setEnabled(False)
            self.controller.update_source_names()

    @Slot()
    def show_name_exist_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("An analysis with this name already exists. Please specify a different name.")
        msg.setIcon(QMessageBox.Critical)
        msg.exec()

    def closeEvent(self, event):
        self.controller.analysis_module_temperatures_controller.cancel()
        event.accept()