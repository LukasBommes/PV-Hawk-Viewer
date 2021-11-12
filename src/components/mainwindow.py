import os
import json
import shutil
import pickle
import numpy as np

from PySide6.QtWidgets import QMainWindow, QToolBar, QDockWidget, \
    QMessageBox, QFileDialog
from PySide6.QtCore import Qt, Slot, QUrl, QDir, Signal, QObject
from PySide6.QtWebChannel import QWebChannel

from src.common import get_immediate_subdirectories

from src.ui.ui_mainwindow import Ui_MainWindow
from src.components.map import MapView, ColorbarView
from src.components.annotation_editor import AnnotationEditorView
from src.components.data_sources import DataSourcesView
from src.components.source_frame import SourceFrameView
from src.components.analysis_module_temperatures import AnalysisModuleTemperaturesView
from src.components.toolbar import DataColumnSelectionView, DataRangeView


class MainView(QMainWindow):
    def __init__(self, model, controller):
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

        # add colorbar for map view
        self.colorbarView = ColorbarView(self.model, self.controller)
        self.ui.gridLayout.addWidget(self.colorbarView.widget, 1, 0, 1, 1)

        # self.toolBarColormapSelection = QToolBar(self)
        # self.addToolBar(Qt.TopToolBarArea, self.toolBarColormapSelection)
        # self.toolBarColormapSelection.setEnabled(False)
        # self.colormapWidget = ColormapSelectionWidget(self.model, self.controller, parent=self)
        # self.toolBarColormapSelection.addWidget(self.colormapWidget)

        # setup toolbars
        self.toolBarDataColumnSelection = QToolBar(u"Data Selection Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBarDataColumnSelection)
        self.dataColumnSelectionView = DataColumnSelectionView(self.model, self.controller, parent=self)
        self.toolBarDataColumnSelection.addWidget(self.dataColumnSelectionView)

        self.toolBarDataRange = QToolBar(u"Data Range Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBarDataRange)
        self.dataRangeWidget = DataRangeView(self.model, self.controller, parent=self)
        self.toolBarDataRange.addWidget(self.dataRangeWidget)

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

        # for debugging
        #self.ui.actionSave_Defect_Annotation.setEnabled(True)

        # connect signals and slots
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionOpen_Dataset.triggered.connect(self.open_dataset)
        self.ui.actionClose_Dataset.triggered.connect(self.controller.close_dataset)
        self.ui.actionNew_Defect_Annotation.triggered.connect(self.new_defect_annotation)
        self.ui.actionLoad_Defect_Annotation.triggered.connect(self.load_defect_annotation)
        self.ui.actionSave_Defect_Annotation.triggered.connect(self.save_defect_annotation)
        self.ui.actionClose_Defect_Annotation.triggered.connect(self.close_defect_annotation)
        self.ui.actionModule_Temperatures.triggered.connect(self.show_analysis_module_temperatures)
        self.ui.menuView.addAction(self.dataSourcesWidget.toggleViewAction())
        self.ui.menuView.addAction(self.annotationEditorWidget.toggleViewAction())
        self.ui.menuView.addAction(self.sourceFrameWidget.toggleViewAction())
        self.ui.menuView.addAction(self.toolBarDataColumnSelection.toggleViewAction())
        self.ui.menuView.addAction(self.toolBarDataRange.toggleViewAction())
        self.model.dataset_opened.connect(self.dataset_opened)
        self.model.dataset_closed.connect(self.dataset_closed)

        self.model.app_mode_changed.connect(self.app_mode_changed)
        self.model.annotation_editor_model.has_changes_changed.connect(self.defect_annotation_has_changes)
        self.model.annotation_editor_model.current_file_name_changed.connect(self.defect_annotation_has_changes)
        
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
        if dir == "":
            return
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
        self.ui.actionNew_Defect_Annotation.setEnabled(True)
        self.ui.actionLoad_Defect_Annotation.setEnabled(True)
        self.ui.actionNew_String_Annotation.setEnabled(True)
        self.ui.actionLoad_String_Annotation.setEnabled(True)

    def dataset_closed(self):
        self.ui.actionClose_Dataset.setEnabled(False)
        self.ui.actionOpen_Dataset.setEnabled(True)        
        self.ui.actionModule_Temperatures.setEnabled(False)
        self.ui.actionNew_Defect_Annotation.setEnabled(False)
        self.ui.actionLoad_Defect_Annotation.setEnabled(False)
        self.ui.actionSave_Defect_Annotation.setEnabled(False)
        self.ui.actionClose_Defect_Annotation.setEnabled(False)
        self.ui.actionNew_String_Annotation.setEnabled(False)
        self.ui.actionLoad_String_Annotation.setEnabled(False)
        self.ui.actionSave_String_Annotation.setEnabled(False)
        self.ui.actionClose_String_Annotation.setEnabled(False)

    @Slot(str)
    def app_mode_changed(self, app_mode):
        if app_mode == "defect_annotation":
            self.annotationEditorWidget.show()
            self.ui.actionClose_Defect_Annotation.setEnabled(True)
            self.defect_annotation_has_changes(False)
        else:
            self.annotationEditorWidget.hide()
            self.ui.actionSave_Defect_Annotation.setEnabled(False)
            self.ui.actionClose_Defect_Annotation.setEnabled(False)

        if app_mode is None or app_mode == "data_visualization":
            self.setWindowTitle("PV Mapper")

        #if app_mode == "string_annotation":
        #
        #else:
        #

    @Slot(bool)
    def defect_annotation_has_changes(self, has_changes):
        if self.model.app_mode != "defect_annotation":
            return
        file_name = os.path.basename(self.model.annotation_editor_model.current_file_name)
        if has_changes:
            self.ui.actionSave_Defect_Annotation.setEnabled(True)            
            self.setWindowTitle("PV Mapper - {}*".format(file_name))
        else:
            self.ui.actionSave_Defect_Annotation.setEnabled(False)
            self.setWindowTitle("PV Mapper - {}".format(file_name))

    @Slot()
    def new_defect_annotation(self):
        self.model.app_mode = "defect_annotation"
        self.controller.new_defect_annotation.emit()

    @Slot()
    def load_defect_annotation(self):
        self.model.app_mode = "defect_annotation"
        self.controller.load_defect_annotation.emit()

    @Slot()
    def save_defect_annotation(self):
        self.controller.save_defect_annotation.emit()

    @Slot()
    def close_defect_annotation(self):
        self.controller.close_defect_annotation.emit()

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

    def closeEvent(self, event):
        """Ask whether unsaved changes should be saved"""
        self.controller.mainwindow_close_requested.emit(event)



class MainController(QObject):
    source_deleted = Signal()
    new_defect_annotation = Signal()
    save_defect_annotation = Signal()
    load_defect_annotation = Signal()
    close_defect_annotation = Signal()
    mainwindow_close_requested = Signal(object)

    def __init__(self, model):
        super().__init__()
        self.model = model

    @Slot(str)
    def open_dataset(self, dataset_dir):
        self.model.dataset_dir = dataset_dir
        self.model.patch_meta = pickle.load(open(os.path.join(
            self.model.dataset_dir, "patches", "meta.pkl"), "rb"))
        self.update_source_names()
        self.load_source("Module Layout")
        self.update_track_ids()
        self.model.dataset_is_open = True
        self.model.app_mode = "data_visualization"

    @Slot()
    def close_dataset(self):  # TODO: reset all subordinate models as well
        self.model.reset()
        self.model.dataset_is_open = False
        self.model.app_mode = None

    @Slot()
    def update_source_names(self):
        source_names = []
        if self.model.dataset_dir is not None:
            try:
                source_names = sorted(get_immediate_subdirectories(
                    os.path.join(self.model.dataset_dir, "analyses")))
            except FileNotFoundError:
                pass
        source_names.insert(0, "Module Layout")
        self.model.source_names = source_names

    @Slot()
    def update_track_ids(self):
        self.model.track_ids = list(self.get_column("track_id").values())

    @Slot(str)
    def load_source(self, selected_source):
        print("Updating", selected_source)
        if self.model.dataset_dir is None:
            return
        if selected_source is None:
            return
        if selected_source == "Module Layout":
            self.model.data = json.load(open(os.path.join(
                self.model.dataset_dir, "mapping", "module_geolocations_refined.geojson"), "r"))
            self.model.meta = None            
        else:
            self.model.data = json.load(open(os.path.join(
                self.model.dataset_dir, "analyses", selected_source, "results.geojson"), "r"))
            self.model.meta = json.load(open(os.path.join(
                self.model.dataset_dir, "analyses", selected_source, "meta.json"), "r"))
        self.model.selected_source = selected_source

    @Slot()
    def delete_source(self, selected_source):
        if self.model.dataset_dir is None:
            return
        if selected_source is None:
            return
        if selected_source == "Module Layout":
            return
        if selected_source == self.model.selected_source:
            self.source_deleted.emit()
        rmdir = os.path.join(self.model.dataset_dir, "analyses", selected_source)
        print("Deleting {}".format(rmdir))
        shutil.rmtree(rmdir, ignore_errors=True)
        self.update_source_names()

    @Slot()
    def get_column_names(self):
        if self.model.dataset_dir is None:
            return []
        columns_names = set()
        for feature in self.model.data["features"]:
            columns_names = columns_names | set(feature["properties"].keys())
        columns_names -= set(["track_id"])
        return sorted(list(columns_names))

    @Slot()
    def get_selected_column(self):
        if self.model.selected_column is None:
            return {}
        columns_names = self.get_column_names()
        try:
            column = columns_names[self.model.selected_column]
        except IndexError:
            return {}
        else:
            return self.get_column(column)

    @Slot()
    def get_column(self, column):
        if self.model.dataset_dir is None:
            return {}
        column_values = {}
        for feature in self.model.data["features"]:
            track_id = feature["properties"]["track_id"]
            try:
                val = feature["properties"][column]
                if val is None:
                    val = np.nan
                column_values[track_id] = val
            except KeyError:
                continue
        return column_values



class MainModel(QObject):
    dataset_opened = Signal()
    dataset_closed = Signal()
    source_names_changed = Signal(object)
    selected_source_changed = Signal(str)
    selected_column_changed = Signal(int)
    track_id_changed = Signal(str)
    patch_idx_changed = Signal(int)
    app_mode_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.dataset_dir = None
        self.data = None
        self.meta = None
        self.patch_meta = None
        self.track_ids = None
        self._app_mode = None # "None", "data_visualization", "defect_annotation", "string_annotation"
        self._source_names = None
        self._dataset_is_open = False
        self._selected_source = None
        self._selected_column = None
        self._track_id = None
        self._patch_idx = None

    @property
    def app_mode(self):
        return self._app_mode

    @app_mode.setter
    def app_mode(self, value):
        self._app_mode = value
        self.app_mode_changed.emit(value)

    @property
    def selected_column(self):
        return self._selected_column

    @selected_column.setter
    def selected_column(self, value):
        self._selected_column = value
        self.selected_column_changed.emit(value)

    @property
    def track_id(self):
        return self._track_id

    @track_id.setter
    def track_id(self, value):
        self._track_id = value
        self._patch_idx = 0
        self.track_id_changed.emit(value)
        self.patch_idx_changed.emit(value)

    @property
    def patch_idx(self):
        return self._patch_idx

    @patch_idx.setter
    def patch_idx(self, value):
        self._patch_idx = value
        self.patch_idx_changed.emit(value)

    @property
    def dataset_is_open(self):
        return self._dataset_is_open

    @dataset_is_open.setter
    def dataset_is_open(self, value):
        self._dataset_is_open = value
        if self._dataset_is_open:
            self.dataset_opened.emit()
        else:
            self.dataset_closed.emit()

    @property
    def source_names(self):
        return self._source_names

    @source_names.setter
    def source_names(self, value):
        self._source_names = value
        self.source_names_changed.emit(value)

    @property
    def selected_source(self):
        return self._selected_source

    @selected_source.setter
    def selected_source(self, value):
        self._selected_source = value
        self.selected_source_changed.emit(value)