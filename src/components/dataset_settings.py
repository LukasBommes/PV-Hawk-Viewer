import os
import json

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Slot, Signal, QObject

from ..ui.ui_dataset_settings import Ui_DatasetSettings


class DatasetSettingsView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # open in new window
        self.model = model
        self.controller = controller
        self.ui = Ui_DatasetSettings()
        self.ui.setupUi(self)

        # connect signals and slots
        self.ui.pushButtonCancel.clicked.connect(self.close)
        self.ui.pushButtonSave.clicked.connect(self.save)
        self.ui.gainSpinBox.valueChanged.connect(lambda value: setattr(self.model.dataset_settings_model, 'gain', value))
        self.model.dataset_settings_model.gain_changed.connect(self.ui.gainSpinBox.setValue)
        self.ui.offsetSpinBox.valueChanged.connect(lambda value: setattr(self.model.dataset_settings_model, 'offset', value))
        self.model.dataset_settings_model.offset_changed.connect(self.ui.offsetSpinBox.setValue)
        
        # set defaults
        self.ui.gainSpinBox.setValue(self.model.dataset_settings_model.gain)
        self.ui.offsetSpinBox.setValue(self.model.dataset_settings_model.offset)

    def save(self):
        self.controller.save_dataset_settings()
        self.close()



class DatasetSettingsModel(QObject):
    gain_changed = Signal(float)
    offset_changed = Signal(float)

    def __init__(self):
        super().__init__()
        self._gain = None
        self._offset = None

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, value):
        self._gain = value
        self.gain_changed.emit(value)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.offset_changed.emit(value)

    


