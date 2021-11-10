from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QComboBox
from PySide6.QtCore import Slot

from src.ui.ui_toolbar_data_range import Ui_DataRange
# from src.ui.ui_toolbar_colormap_selection import Ui_ColormapSelection


class DataRangeView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.parent = parent
        self.ui = Ui_DataRange()
        self.ui.setupUi(self)
        self.disable()
        # connect signals and slots
        self.model.map_model.min_val_changed.connect(self.ui.minValSpinBox.setValue)
        self.model.map_model.max_val_changed.connect(self.ui.maxValSpinBox.setValue)
        self.ui.maxValSpinBox.valueChanged.connect(lambda value: setattr(self.model.map_model, 'max_val', value))
        self.ui.minValSpinBox.valueChanged.connect(lambda value: setattr(self.model.map_model, 'min_val', value))
        self.model.selected_source_changed.connect(self.enable)
        self.model.dataset_closed.connect(self.disable)

        # set default values (TODO: set automatically based on selected data column)
        self.model.map_model.min_val = -5
        self.model.map_model.max_val = 5

    def enable(self):
        if self.model.selected_source is None:
            self.disable()
        elif self.model.selected_source == "Module Layout":
            self.disable()
        else:
            self.ui.minValSpinBox.setEnabled(True)
            self.ui.maxValSpinBox.setEnabled(True)

    def disable(self):
        self.ui.minValSpinBox.setEnabled(False)
        self.ui.maxValSpinBox.setEnabled(False)


# class ColormapSelectionView(QWidget):
#     def __init__(self, model, controller, parent=None):
#         super().__init__(parent)
#         self.model = model
#         self.controller = controller
#         self.parent = parent
#         self.ui = Ui_ColormapSelection()
#         self.ui.setupUi(self)
#         self.ui.comboBox.addItems(["Gray", "Plasma", "Jet"])
#         self.ui.comboBox.setCurrentIndex(0)
#         # connect signals and slots
#         self.ui.comboBox.currentIndexChanged.connect(lambda: self.parent.setColormap(self.ui.comboBox.currentIndex()))


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
        if self.model.selected_source is None:
            self.comboBox.setEnabled(False)
        elif self.model.selected_source == "Module Layout":
            self.comboBox.setEnabled(False)
        else:
            self.comboBox.setEnabled(True)
            data_columns = self.controller.get_column_names()
            self.comboBox.addItems(data_columns)  # probably causes currentIndexChanged to be fired