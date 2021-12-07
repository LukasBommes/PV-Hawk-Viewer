def main():
    import sys

    from PySide6.QtWidgets import QApplication

    from .components.mainwindow import MainController, MainView, MainModel
    from .components.analysis import AnalysisController, AnalysisModel
    from .components.source_frame import SourceFrameController, SourceFrameModel
    from .components.patches import PatchesController, PatchesModel
    from .components.map import MapModel
    from .components.annotation_editor import AnnotationEditorController, AnnotationEditorModel
    from .components.string_editor import StringEditorController, StringEditorModel



    class App(QApplication):
        def __init__(self, sys_argv):
            super(App, self).__init__(sys_argv)

            # models
            self.main_model = MainModel()
            self.main_model.source_frame_model = SourceFrameModel()
            self.main_model.patches_model = PatchesModel()
            self.main_model.analysis_model = AnalysisModel()
            self.main_model.map_model = MapModel()
            self.main_model.annotation_editor_model = AnnotationEditorModel()
            self.main_model.string_editor_model = StringEditorModel()

            # controllers
            self.main_controller = MainController(self.main_model)
            self.main_controller.source_frame_controller = SourceFrameController(self.main_model)
            self.main_controller.patches_controller = PatchesController(self.main_model)
            self.main_controller.analysis_controller = AnalysisController(self.main_model)
            self.main_controller.annotation_editor_controller = AnnotationEditorController(self.main_model)
            self.main_controller.string_editor_controller = StringEditorController(self.main_model)
            
            self.main_view = MainView(self.main_model, self.main_controller)
            screen = self.main_view.screen()
            self.main_view.resize(screen.availableSize() * 0.7)
            self.main_view.show()

    app = App(sys.argv)
    sys.exit(app.exec())



if __name__ == "__main__":
    main()