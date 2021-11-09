from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QComboBox
from PySide6.QtCore import Slot


class DataColumnSelectionView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.parent = parent
        self.build_ui()
        
        # connect signals and slots
        self.model.dataset_opened.connect(lambda: self.comboBox.setEnabled(True))
        self.model.dataset_opened.connect(self.update_options)
        self.model.dataset_closed.connect(lambda: self.comboBox.setEnabled(False))
        self.model.dataset_closed.connect(self.update_options)
        self.model.selected_source_changed.connect(self.update_options)
        self.comboBox.currentIndexChanged.connect(lambda value: setattr(self.model, 'selected_column', value))
        self.model.selected_column_changed.connect(self.comboBox.setCurrentIndex)

        self.update_options()

    def build_ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setText("Data Column")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setFixedWidth(150)
        self.comboBox.setEnabled(False)
        self.horizontalLayout.addWidget(self.comboBox)

    @Slot()
    def update_options(self):
        self.comboBox.clear()
        data_columns = self.controller.get_column_names()
        self.comboBox.addItems(data_columns)
        if len(data_columns) > 0:
            self.model.selected_column = 0
        else:
            self.model.selected_column = None