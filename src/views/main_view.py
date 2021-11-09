from PySide6.QtWidgets import QMainWindow, QToolBar, QDockWidget, \
    QMessageBox, QFileDialog
from PySide6.QtCore import Qt, Slot, QUrl, QDir
from PySide6.QtWebChannel import QWebChannel

from src.common import get_immediate_subdirectories
from src.ui.ui_mainwindow import Ui_MainWindow
from src.views.map_view import MapView
from src.views.annotation_editor_view import AnnotationEditorView
from src.views.data_sources_view import DataSourcesView
from src.views.source_frame_view import SourceFrameView
from src.views.analysis_module_temperatures_view import AnalysisModuleTemperaturesView
from src.views.data_column_selection_view import DataColumnSelectionView


class MainView(QMainWindow):
    def __init__(self, model, controller):
        #super(MainView, self).__init__()
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = model
        self.controller = controller

        # register map view
        self.map_view = MapView(model, controller, parent=self)
        channel = QWebChannel(self.ui.widget.page())
        self.ui.widget.page().setWebChannel(channel)
        channel.registerObject("map_view", self.map_view)

        # setup toolbars
        # self.toolBarTempRange = QToolBar(self)
        # self.addToolBar(Qt.TopToolBarArea, self.toolBarTempRange)
        # self.toolBarTempRange.setEnabled(False)
        # self.tempRangeWidget = TempRangeWidget(model, controller, parent=self)
        # self.toolBarTempRange.addWidget(self.tempRangeWidget)

        # self.toolBarColormapSelection = QToolBar(self)
        # self.addToolBar(Qt.TopToolBarArea, self.toolBarColormapSelection)
        # self.toolBarColormapSelection.setEnabled(False)
        # self.colormapWidget = ColormapSelectionWidget(model, controller, parent=self)
        # self.toolBarColormapSelection.addWidget(self.colormapWidget)

        # setup toolbars
        self.toolBarDataColumnSelection = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBarDataColumnSelection)
        self.dataColumnSelectionView = DataColumnSelectionView(self.model, self.controller, parent=self)
        self.toolBarDataColumnSelection.addWidget(self.dataColumnSelectionView)

        # setup widgets
        self.annotationEditorWidget = QDockWidget(u"Annotation Editor", self)
        self.annotation_editor = AnnotationEditorView(self.model, self.controller, parent=self)
        self.annotationEditorWidget.setWidget(self.annotation_editor)
        
        self.sourceFrameWidget = QDockWidget(u"Source Frame", self)
        self.source_frame = SourceFrameView(self.model, self.controller, parent=self)
        self.sourceFrameWidget.setWidget(self.source_frame)
        
        self.dataSourcesWidget = QDockWidget(u"Data Sources", self)
        self.data_sources = DataSourcesView(self.model, self.controller, parent=self)
        self.dataSourcesWidget.setWidget(self.data_sources)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.dataSourcesWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.annotationEditorWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sourceFrameWidget)

        # child windows
        self.module_temperatures_window = None

        # connect signals and slots
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionOpen_Dataset.triggered.connect(self.open_dataset)
        self.ui.actionClose_Dataset.triggered.connect(self.controller.close_dataset)
        self.ui.actionNew_Annotation.triggered.connect(self.new_annotation)
        self.ui.actionLoad_Annotation.triggered.connect(self.load_annotation)
        self.ui.actionSave_Annotation.triggered.connect(self.save_annotation)
        self.ui.actionModule_Temperatures.triggered.connect(self.show_analysis_module_temperatures)
        self.ui.menuView.addAction(self.dataSourcesWidget.toggleViewAction())
        self.ui.menuView.addAction(self.annotationEditorWidget.toggleViewAction())
        self.ui.menuView.addAction(self.sourceFrameWidget.toggleViewAction())
        self.model.dataset_opened.connect(self.dataset_opened)
        self.model.dataset_closed.connect(self.dataset_closed)
        
        # load HTML document for map view
        index_file = QDir.current().filePath("src/index.html")
        index_url = QUrl.fromLocalFile(index_file)
        self.ui.widget.load(index_url)

    def valid_dataset(self, dir):
        probe_dirs = get_immediate_subdirectories(dir)
        if not "mapping" in probe_dirs:
            return False
        if not "patches" in probe_dirs:
            return False
        if not "patches_final" in probe_dirs:
            return False
        if not "splitted" in probe_dirs:
            return False
        return True

    @Slot()
    def open_dataset(self):
        dir = QFileDialog.getExistingDirectory(
            self, caption="Open Dataset", options=QFileDialog.ShowDirsOnly)
        if self.valid_dataset(dir):
            self.controller.open_dataset(dir)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Not a valid PV Mapper Dataset.")
            msg.setIcon(QMessageBox.Critical)
            msg.exec()

    def dataset_opened(self):
        self.ui.actionClose_Dataset.setEnabled(True)
        self.ui.actionOpen_Dataset.setEnabled(False)
        self.ui.actionModule_Temperatures.setEnabled(True)

    def dataset_closed(self):
        self.ui.actionClose_Dataset.setEnabled(False)
        self.ui.actionOpen_Dataset.setEnabled(True)        
        self.ui.actionModule_Temperatures.setEnabled(False)

    @Slot()
    def new_annotation(self):
        pass

    @Slot()
    def load_annotation(self):
        pass

    @Slot()
    def save_annotation(self):
        pass

    @Slot()
    def show_analysis_module_temperatures(self):
        if not self.model.dataset_is_open:
            return
        if self.module_temperatures_window is None:
            self.module_temperatures_window = AnalysisModuleTemperaturesView(self.model, self.controller, self)
        self.controller.analysis_module_temperatures_controller.reset()
        self.module_temperatures_window.show()

    def about(self):
        QMessageBox.about(
            self,
            "About Sample Editor",
            "<p>A sample text editor app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",
        )