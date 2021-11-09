import sys
import os
import re
import shutil
import glob
import json
import pickle
import datetime
import cv2
import numpy as np

from PySide6.QtWidgets import QApplication

# from src.ui.ui_toolbar_temp_range import Ui_TempRange
# from src.ui.ui_toolbar_colormap_selection import Ui_ColormapSelection

from src.views.main_view import MainView

from src.controllers.analysis_module_temperatures_controller import AnalysisModuleTemperaturesController
from src.controllers.source_frame_controller import SourceFrameController
from src.controllers.main_controller import MainController

from src.models.analysis_module_temperatures_model import AnalysisModuleTemperaturesModel
from src.models.source_frame_model import SourceFrameModel
from src.models.main_model import MainModel



########################################################################
#
#       Views
#
########################################################################



# class TempRangeView(QWidget):
#     def __init__(self, model, controller, parent=None):
#         super().__init__(parent)
#         self.model = model
#         self.controller = controller
#         self.parent = parent
#         self.ui = Ui_TempRange()
#         self.ui.setupUi(self)
#         # connect signals and slots
#         self.ui.minTempSpinBox.valueChanged.connect(lambda: self.parent.setMinTemp(self.ui.minTempSpinBox.value()))
#         self.ui.maxTempSpinBox.valueChanged.connect(lambda: self.parent.setMaxTemp(self.ui.maxTempSpinBox.value()))


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



########################################################################
#
#       Controllers
#
########################################################################




########################################################################
#
#       Models
#
########################################################################


# class MapModel(QObject):
#     min_temp_changed = Signal(int)
#     max_temp_changed = Signal(int)
#     colormap_changed = Signal(int)

#     def __init__(self):
#         super().__init__()
#         self._min_temp = None
#         self._max_temp = None
#         self._colormap = None
    
#     @property
#     def min_temp(self):
#         return self._min_temp

#     @min_temp.setter
#     def min_temp(self, value):
#         self._min_temp = value
#         self.min_temp_changed.emit(value)

#     @property
#     def max_temp(self):
#         return self._max_temp

#     @max_temp.setter
#     def max_temp(self, value):
#         self._max_temp = value
#         self.max_temp_changed.emit(value)

#     @property
#     def colormap(self):
#         return self._colormap

#     @colormap.setter
#     def colormap(self, value):
#         self._colormap = value
#         self.colormap_changed.emit(value)




class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        # models
        self.main_model = MainModel()
        self.main_model.source_frame_model = SourceFrameModel()
        self.main_model.analysis_module_temperatures_model = AnalysisModuleTemperaturesModel()

        # controllers
        self.main_controller = MainController(self.main_model)
        self.main_controller.source_frame_controller = SourceFrameController(self.main_model)
        self.main_controller.analysis_module_temperatures_controller = AnalysisModuleTemperaturesController(self.main_model)

        self.main_view = MainView(self.main_model, self.main_controller)
        self.main_view.show()



if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
