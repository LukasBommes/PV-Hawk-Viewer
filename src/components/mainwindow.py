import os
import json
import csv
import shutil
import pickle
import datetime
import numpy as np

from PySide6.QtWidgets import QMainWindow, QToolBar, QDockWidget, \
    QMessageBox, QFileDialog, QLabel, QMenu
from PySide6.QtCore import Qt, Slot, QUrl, QDir, Signal, QObject
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtGui import QIcon, QPixmap

from src.common import get_immediate_subdirectories

from src.ui.ui_mainwindow import Ui_MainWindow
from src.components.map import MapView, ColorbarView, DataColumnSelectionView, \
    DataRangeView, ColormapSelectionView, LayerSelectionView
from src.components.annotation_editor import AnnotationEditorView
from src.components.data_sources import DataSourcesView
from src.components.source_frame import SourceFrameView
from src.components.patches import PatchesView
from src.components.analysis import AnalysisView
from src.components.analysis_details import AnalysisDetailsView
from src.components.string_editor import StringEditorView


class MainView(QMainWindow):
    def __init__(self, model, controller):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = model
        self.controller = controller

        # set window icon
        app_icon = QIcon(QPixmap("src/resources/app_icon.png"))
        self.setWindowIcon(app_icon)

        # add icons QStyle.SP_MessageBoxCritical
        self.ui.actionOpen_Dataset.setIcon(QIcon.fromTheme("document-open"))
        self.ui.actionClose_Dataset.setIcon(QIcon.fromTheme("window-close"))
        self.ui.actionQuit.setIcon(QIcon.fromTheme("application-exit"))
        self.ui.actionNew_Defect_Annotation.setIcon(QIcon.fromTheme("document-new"))
        self.ui.actionLoad_Defect_Annotation.setIcon(QIcon.fromTheme("document-open"))
        self.ui.actionSave_Defect_Annotation.setIcon(QIcon.fromTheme("document-save"))
        self.ui.actionClose_Defect_Annotation.setIcon(QIcon.fromTheme("window-close"))
        self.ui.actionExport_String_Annotation.setIcon(QIcon.fromTheme("document-save"))
        self.ui.actionClose_String_Annotation.setIcon(QIcon.fromTheme("window-close"))
        self.ui.actionAbout.setIcon(QIcon.fromTheme("help-about"))        
        
        # register map view
        self.map_view = MapView(model, controller, parent=self)
        self.channel = QWebChannel(self.ui.widget.page())
        self.ui.widget.page().setWebChannel(self.channel)
        self.ui.widget.setContextMenuPolicy(Qt.NoContextMenu)
        self.channel.registerObject("map_view", self.map_view)

        # register string editor controller with web engine
        self.channel.registerObject("string_editor_controller", self.controller.string_editor_controller)

        # add colorbar for map view
        self.colorbarView = ColorbarView(self.model, self.controller)
        self.ui.gridLayout.addWidget(self.colorbarView.widget, 1, 0, 1, 1)

        # setup toolbars
        self.toolBarDataColumnSelection = QToolBar(u"Data Selection Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBarDataColumnSelection)
        self.dataColumnSelectionView = DataColumnSelectionView(self.model, self.controller, parent=self)
        self.toolBarDataColumnSelection.addWidget(self.dataColumnSelectionView)

        self.toolBarDataRange = QToolBar(u"Data Range Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBarDataRange)
        self.dataRangeWidget = DataRangeView(self.model, self.controller, parent=self)
        self.toolBarDataRange.addWidget(self.dataRangeWidget)

        self.toolBarColormapSelection = QToolBar(u"Colormap Selection Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBarColormapSelection)
        self.colormapSelectionWidget = ColormapSelectionView(self.model, self.controller, parent=self)
        self.toolBarColormapSelection.addWidget(self.colormapSelectionWidget)

        self.toolBarLayerSelection = QToolBar(u"Layer Selection Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBarLayerSelection)
        self.layerSelectionWidget = LayerSelectionView(self.model, self.controller, parent=self)
        self.toolBarLayerSelection.addWidget(self.layerSelectionWidget)

        # setup widgets
        self.annotationEditorWidget = QDockWidget(u"Annotation Editor", self)
        self.annotation_editor = AnnotationEditorView(self.model, self.controller, parent=self)
        self.annotationEditorWidget.setWidget(self.annotation_editor)
        
        self.stringEditorWidget = QDockWidget(u"String Editor", self)
        self.string_editor = StringEditorView(self.model, self.controller, parent=self)
        self.stringEditorWidget.setWidget(self.string_editor)

        self.sourceFrameWidget = QDockWidget(u"Source Frame", self)
        self.source_frame = SourceFrameView(self.model, self.controller, parent=self)
        self.sourceFrameWidget.setWidget(self.source_frame)

        self.patchesWidget = QDockWidget(u"Patches", self)
        self.patches = PatchesView(self.model, self.controller, parent=self)
        self.patchesWidget.setWidget(self.patches)
        
        self.dataSourcesWidget = QDockWidget(u"Data Sources", self)
        self.data_sources = DataSourcesView(self.model, self.controller, parent=self)
        self.dataSourcesWidget.setWidget(self.data_sources)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.stringEditorWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dataSourcesWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.annotationEditorWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sourceFrameWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.patchesWidget)
        self.tabifyDockWidget(self.patchesWidget, self.sourceFrameWidget)

        # setup status bar        
        self.numModulesLabel = QLabel()
        self.ui.statusBar.addPermanentWidget(self.numModulesLabel)
        self.numPatchesLabel = QLabel()        
        self.ui.statusBar.addPermanentWidget(self.numPatchesLabel)
        self.flightDurationLabel = QLabel()
        self.ui.statusBar.addPermanentWidget(self.flightDurationLabel)
        self.trajectoryLengthLabel = QLabel()
        self.ui.statusBar.addPermanentWidget(self.trajectoryLengthLabel)

        # file menu
        self.ui.actionOpen_Dataset.triggered.connect(self.open_dataset)
        self.ui.actionClose_Dataset.triggered.connect(self.controller.close_dataset_request)
        self.ui.actionQuit.triggered.connect(self.close)

        # annotation menu
        self.ui.actionNew_Defect_Annotation.triggered.connect(self.new_defect_annotation)
        self.ui.actionLoad_Defect_Annotation.triggered.connect(self.load_defect_annotation)
        self.ui.actionSave_Defect_Annotation.triggered.connect(self.save_defect_annotation)
        self.ui.actionClose_Defect_Annotation.triggered.connect(self.close_defect_annotation)
        self.ui.actionAnnotate_Strings.triggered.connect(self.annotate_strings)
        self.ui.actionExport_String_Annotation.triggered.connect(self.export_string_annotation)
        self.ui.actionClose_String_Annotation.triggered.connect(self.close_string_annotation)

        # analysis menu
        self.ui.actionNew_Analysis.triggered.connect(lambda: self.show_child_window("analysis"))

        # view menu
        self.ui.menuView.addAction(self.dataSourcesWidget.toggleViewAction())
        self.ui.menuView.addAction(self.stringEditorWidget.toggleViewAction())
        self.ui.menuView.addAction(self.annotationEditorWidget.toggleViewAction())
        self.ui.menuView.addAction(self.sourceFrameWidget.toggleViewAction())
        self.ui.menuView.addAction(self.patchesWidget.toggleViewAction())
        self.toolbar_view_menu = QMenu(u"Toolbars")
        self.toolbar_view_menu.addAction(self.toolBarDataColumnSelection.toggleViewAction())
        self.toolbar_view_menu.addAction(self.toolBarDataRange.toggleViewAction())
        self.toolbar_view_menu.addAction(self.toolBarColormapSelection.toggleViewAction())
        self.toolbar_view_menu.addAction(self.toolBarLayerSelection.toggleViewAction())        
        self.ui.menuView.addMenu(self.toolbar_view_menu)

        # about menu
        self.ui.actionAbout.triggered.connect(self.about)

        # connect signals and slots
        self.model.dataset_opened.connect(self.dataset_opened)
        self.model.dataset_closed.connect(self.dataset_closed)
        self.model.dataset_stats_changed.connect(self.update_status_bar)
        self.model.app_mode_changed.connect(self.app_mode_changed)
        self.model.annotation_editor_model.has_changes_changed.connect(self.defect_annotation_has_changes)
        self.model.annotation_editor_model.current_file_name_changed.connect(self.defect_annotation_has_changes)
        self.controller.annotation_editor_controller.close_dataset.connect(self.controller.close_dataset)
        
        # load HTML document for map view
        index_file = QDir.current().filePath("src/index.html")
        index_url = QUrl.fromLocalFile(index_file)
        self.ui.widget.load(index_url)

        self.update_status_bar(stats=None)
        self.child_windows = {}

        # set defaults
        self.model.app_mode = None

        # for development
        #dir = "/home/lukas/HI-ERN-2020/Dataset-Viewer-Georeferencing-Desktop/test_data"
        #self.controller.open_dataset(dir)

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
        self.ui.actionNew_Analysis.setEnabled(True)
        self.ui.actionNew_Defect_Annotation.setEnabled(True)
        self.ui.actionLoad_Defect_Annotation.setEnabled(True)
        self.ui.actionAnnotate_Strings.setEnabled(True)
        self.ui.actionExport_String_Annotation.setEnabled(True)
        self.ui.actionClose_String_Annotation.setEnabled(False)
        self.ui.statusBar.showMessage("Dataset opened", 5000)

    def dataset_closed(self):
        self.ui.actionClose_Dataset.setEnabled(False)
        self.ui.actionOpen_Dataset.setEnabled(True)        
        self.ui.actionNew_Analysis.setEnabled(False)
        self.ui.actionNew_Defect_Annotation.setEnabled(False)
        self.ui.actionLoad_Defect_Annotation.setEnabled(False)
        self.ui.actionSave_Defect_Annotation.setEnabled(False)
        self.ui.actionClose_Defect_Annotation.setEnabled(False)
        self.ui.actionAnnotate_Strings.setEnabled(False)
        self.ui.actionExport_String_Annotation.setEnabled(False)
        self.ui.actionClose_String_Annotation.setEnabled(False)
        self.ui.statusBar.showMessage("Dataset closed", 5000)

    @Slot(object)
    def update_status_bar(self, stats):
        if stats is None:
            stats = {
                "num_modules": 0,
                "num_patches": 0,
                "flight_duration": "00:00:00.000",
                "trajectory_length": 0,
            }

        self.numModulesLabel.setText("Modules: {}".format(stats["num_modules"]))
        self.numPatchesLabel.setText("Patches: {}".format(stats["num_patches"]))
        self.flightDurationLabel.setText("Flight duration: {}".format(stats["flight_duration"]))
        self.trajectoryLengthLabel.setText("Trajectory length: {} m".format(int(stats["trajectory_length"])))

    @Slot(str)
    def app_mode_changed(self, app_mode):
        print("app_mode ", app_mode)
        if app_mode == "defect_annotation":
            self.annotationEditorWidget.show()
            self.annotationEditorWidget.setEnabled(True)
            self.ui.actionClose_Defect_Annotation.setEnabled(True)
            self.defect_annotation_has_changes(False)
        else:
            self.annotationEditorWidget.hide()
            self.annotationEditorWidget.setEnabled(False)
            self.ui.actionSave_Defect_Annotation.setEnabled(False)
            self.ui.actionClose_Defect_Annotation.setEnabled(False)

        if app_mode == "string_annotation":
            self.stringEditorWidget.show()
            self.stringEditorWidget.setEnabled(True)
            self.ui.actionClose_String_Annotation.setEnabled(True)
        else:
            self.stringEditorWidget.hide()
            self.stringEditorWidget.setEnabled(False)
            self.ui.actionClose_String_Annotation.setEnabled(False)

        if app_mode is None or app_mode == "data_visualization":
            self.setWindowTitle("PV Mapper")
        

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
        self.controller.load_defect_annotation.emit()

    @Slot()
    def save_defect_annotation(self):
        self.controller.save_defect_annotation.emit()

    @Slot()
    def close_defect_annotation(self):
        self.controller.close_defect_annotation.emit()

    @Slot()
    def annotate_strings(self):
        if self.model.app_mode == "defect_annotation":
            self.controller.close_defect_annotation.emit()
        self.model.app_mode = "string_annotation"
        # remark on line above: in close defect annotation app mode is set to
        # "data_visualization". Nothing guarantees that the subsequent line
        # is executed after the app mode was set to "data_visualization".

    @Slot()
    def export_string_annotation(self):
        self.controller.export_string_annotation.emit()

    @Slot()
    def close_string_annotation(self):
        self.controller.close_string_annotation.emit()
        self.model.app_mode = "data_visualization"

    @Slot()
    def show_child_window(self, which):
        if which == "analysis":
            if not self.model.dataset_is_open:
                return
            if which not in self.child_windows:
                self.child_windows[which] = AnalysisView(self.model, self.controller, self)
            self.controller.analysis_controller.reset()
            self.child_windows[which].show()

        elif which == "analysis_details":
            if self.model.meta is None:
                return
            if which not in self.child_windows:
                self.child_windows[which] = AnalysisDetailsView(self.model, self.controller, self)
            self.child_windows[which].show()

    def about(self):
        gh = "LukasBommes/Dataset-Viewer"
        about_text = "Dataset Viewer for PV-Mapper<br><br>" \
            + "Author: Lukas Bommes<br>" \
            + "Organization: Helmholtz Institute Erlangen-Nürnberg for Renewable Energy (HI ERN)<br>" \
            + "GitHub: " \
            + "<a href='https://github.com/{gh}'>{gh}</a><br>".format(gh=gh)
        QMessageBox.about(
            self,
            "About Dateset Viewer for PV-Mapper",
            about_text
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
    export_string_annotation = Signal()
    close_string_annotation = Signal()
    mainwindow_close_requested = Signal(object)
    dataset_close_requested = Signal()
    redraw_map = Signal()

    def __init__(self, model):
        super().__init__()
        self.model = model

    def reset(self):
        self.model.dataset_dir = None
        self.model.data = None
        self.model.meta = None
        self.model.patch_meta = None
        self.model.track_ids = None
        self.model.app_mode = None
        self.model.source_names = None
        self.model.dataset_is_open = False
        self.model.selected_source = None
        self.model.selected_column = None
        self.model.track_id = None
        self.model.dataset_stats = None

    @Slot(str)
    def open_dataset(self, dataset_dir):
        self.model.dataset_dir = dataset_dir
        self.model.patch_meta = pickle.load(open(os.path.join(
            self.model.dataset_dir, "patches", "meta.pkl"), "rb"))
        self.update_source_names()
        self.load_source("Module Layout")
        self.update_track_ids()
        self.update_dataset_stats()
        self.model.dataset_is_open = True
        self.model.app_mode = "data_visualization"

    @Slot()
    def close_dataset_request(self):
        if self.model.app_mode == "defect_annotation":
            self.dataset_close_requested.emit()
        #elif self.model.app_mode == "string_annotation":
        #    pass
        else:
            self.close_dataset()

    @Slot()
    def close_dataset(self):
        self.reset()

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
        try:
            source_names.remove("Sun Filter")  # ignore sun_filter output in analysis
        except ValueError:
            pass
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

    @Slot(int)
    def set_selected_column(self, value):
        # first update map value range then set selected column
        columns_names = self.get_column_names()
        try:
            column = columns_names[value]
        except IndexError:
            min_val = -5
            max_val = 5
        else:
            data_column = self.get_column(column)
            if len(data_column) == 0:
                min_val = -5
                max_val = 5
            else:
                min_val = min(data_column.values())
                max_val = max(data_column.values())
        self.model.map_model.min_val = min_val
        self.model.map_model.max_val = max_val
        # set selected column
        self.model.selected_column = value

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

    def update_dataset_stats(self):
        if self.model.dataset_dir is None:
            return

        # num modules
        num_modules = 0
        for feature in self.model.data["features"]:
            geometry = feature["geometry"]["type"]
            if geometry == "Polygon":
                num_modules += 1

        # num patches
        num_patches = 0
        for _, _, files in os.walk(os.path.join(self.model.dataset_dir, "patches_final", "radiometric")):
            num_patches += len(files)

        # flight duration
        timestamps = []
        with open(os.path.join(self.model.dataset_dir, "splitted", "timestamps.csv"), newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvreader:
                timestamps.append(datetime.datetime.fromisoformat(*row))                
        dt = (timestamps[-1] - timestamps[0]).total_seconds()
        hours, remainder = divmod(dt, 3600)
        minutes, seconds = divmod(remainder, 60)
        flight_duration = "{:02d}:{:02d}:{:0.3f}".format(int(hours), int(minutes), seconds)

        # trajectory length
        pose_graph = pickle.load(open(os.path.join(self.model.dataset_dir, "mapping", "pose_graph.pkl"), "rb"))
        positions = []
        for node_id, data in pose_graph.nodes(data=True):
            pose = data["pose"][3:].reshape(3, 1)
            positions.append(pose)
        trajectory_length = 0
        for i in range(1, len(positions)):
            trajectory_length += np.linalg.norm(positions[i] - positions[i-1])

        stats = {
            "num_modules": num_modules,
            "num_patches": num_patches,
            "flight_duration": flight_duration,
            "trajectory_length": trajectory_length,
        }
        self.model.dataset_stats = stats



class MainModel(QObject):
    dataset_opened = Signal()
    dataset_closed = Signal()
    source_names_changed = Signal(object)
    selected_source_changed = Signal(str)
    selected_column_changed = Signal(int)
    track_id_changed = Signal(str, str)
    meta_changed = Signal()
    dataset_stats_changed = Signal(object)
    app_mode_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.dataset_dir = None
        self.data = None
        self._meta = None
        self.patch_meta = None
        self.track_ids = None
        self._app_mode = None # "None", "data_visualization", "defect_annotation", "string_annotation"
        self._source_names = None
        self._dataset_is_open = False
        self._selected_source = None
        self._selected_column = None
        self._track_id = None
        self._dataset_stats = None

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, value):
        self._meta = value
        self.meta_changed.emit()

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
        track_id_prev = self._track_id
        self._track_id = value
        self.track_id_changed.emit(track_id_prev, value)

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

    @property
    def dataset_stats(self):
        return self._dataset_stats

    @dataset_stats.setter
    def dataset_stats(self, value):
        self._dataset_stats = value
        self.dataset_stats_changed.emit(value)