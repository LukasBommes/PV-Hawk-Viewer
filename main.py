import sys
import numpy as np

from PySide6.QtWidgets import QApplication

from src.components.mainwindow import MainController, MainView, MainModel
from src.components.analysis_module_temperatures import AnalysisModuleTemperaturesController, AnalysisModuleTemperaturesModel
from src.components.source_frame import SourceFrameController, SourceFrameModel
from src.components.map import MapModel



class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        # models
        self.main_model = MainModel()
        self.main_model.source_frame_model = SourceFrameModel()
        self.main_model.analysis_module_temperatures_model = AnalysisModuleTemperaturesModel()
        self.main_model.map_model = MapModel()

        # controllers
        self.main_controller = MainController(self.main_model)
        self.main_controller.source_frame_controller = SourceFrameController(self.main_model)
        self.main_controller.analysis_module_temperatures_controller = AnalysisModuleTemperaturesController(self.main_model)

        self.main_view = MainView(self.main_model, self.main_controller)
        self.main_view.show()



if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
