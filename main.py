import sys
import os
import re
import shutil
import glob
import json
import pickle
import datetime
from collections import defaultdict
import cv2
import numpy as np

from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, \
    QDockWidget, QMessageBox, QCheckBox, QSpacerItem, QSizePolicy, QLabel, \
    QGridLayout, QFileDialog, QBoxLayout, QHBoxLayout, QComboBox
from PySide6.QtCore import QThread, Qt, Slot, Signal, QUrl, QDir, QObject, \
    QSize
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWebChannel import QWebChannel

from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_source_frame import Ui_SourceFrame
from ui.ui_annotation_editor import Ui_AnnotationEditor
from ui.ui_data_sources import Ui_DataSources
from ui.ui_toolbar_temp_range import Ui_TempRange
from ui.ui_toolbar_colormap_selection import Ui_ColormapSelection
from ui.ui_analysis_module_temperatures import Ui_ModuleTemperatures

from common import get_immediate_subdirectories, to_celsius, normalize
from analysis.temperatures import AnalysisModuleTemperaturesWorker
from colormap import get_colors


########################################################################
#
#       Views
#
########################################################################


class MapView(QObject):
    dataset_changed = Signal()  # signals for notification of Javascript
    dataset_closed = Signal()

    def __init__(self, model, controller, parent=None):
        super(MapView, self).__init__()
        self.model = model
        self.controller = controller
        self.parent = parent
        # connect signals and slots
        self.controller.source_deleted.connect(self.dataset_closed)        
        self.model.dataset_closed.connect(self.dataset_closed)
        self.model.selected_source_changed.connect(self.dataset_changed)
        self.model.selected_column_changed.connect(self.dataset_changed)

    @Slot(str)
    def printObj(self, obj):
        py_obj = json.loads(obj)
        print(py_obj)

    @Slot(result=str)
    def loadData(self):
        data = []
        colors = {}
        if self.model.dataset_is_open:
            data = self.model.data
            data_column = self.controller.get_selected_column()
            if len(data_column) > 0:
                # colormaps = {
                #     0: "plasma",
                #     1: "Reds",
                #     2: "viridis"
                # }
                # colormap = colormaps[self.parent.map_model.colormap]
                # colors = get_colors(data_column, cmap=colormap, vmin=self.parent.map_model.min_temp, vmax=self.parent.map_model.max_temp)
                colors = get_colors(data_column, cmap="plasma", vmin=-5, vmax=5)
            else:
                default_color = "#ff7800"
                track_ids = list(self.controller.get_column("track_id").values())
                colors = {track_id: default_color for track_id in track_ids}
        return json.dumps({
            "data": data,
            "colors": colors
        })

    @Slot(str)
    def updateImages(self, track_id):
        self.model.track_id = json.loads(track_id)


class AnnotationEditorView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.ui = Ui_AnnotationEditor()
        self.ui.setupUi(self)
        self.loadDefectsScheme()
        # TODO: connect signals and slots

    def loadDefectsScheme(self):
        try:
            defects_scheme = json.load(open(os.path.join("resources", "defect_schema.json"), "r"))
        except FileNotFoundError:
            pass
        else:
            for defect in defects_scheme:
                checkbox = QCheckBox("{} - {}".format(defect["name"], defect["description"]))
                checkbox.setToolTip(", ".join(defect["examples"]))
                self.ui.scrollAreaWidgetContents.layout().addWidget(checkbox)
            self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.ui.scrollAreaWidgetContents.layout().addItem(self.verticalSpacer)


class DataSourcesView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.parent = parent
        self.ui = Ui_DataSources()
        self.ui.setupUi(self)
        self.update()
        # connect signals and slots
        self.ui.pushButtonDelete.clicked.connect(self.delete_source)
        self.ui.pushButtonNewAnalysis.clicked.connect(self.parent.show_analysis_module_temperatures)
        self.ui.dataSourcesListWidget.itemClicked.connect(lambda name: self.controller.loadSource(name.text()))
        self.ui.dataSourcesListWidget.itemClicked.connect(lambda name: self.ui.pushButtonDelete.setEnabled(name.text() != "Module Layout"))
        self.ui.dataSourcesListWidget.itemSelectionChanged.connect(lambda: setattr(self.model.source_frame_model, 'frame', None))
        self.model.source_names_changed.connect(self.update)
        self.model.dataset_opened.connect(self.update)
        self.model.dataset_opened.connect(lambda: self.ui.pushButtonNewAnalysis.setEnabled(True))
        self.model.dataset_closed.connect(self.update)
        self.model.dataset_closed.connect(lambda: self.ui.pushButtonNewAnalysis.setEnabled(False))

        #self.ui.colormapComboBox.currentIndexChanged.connect(lambda value: setattr(self.model.source_frame_model, 'colormap', value))
        #self.model.source_frame_model.colormap_changed.connect(self.ui.colormapComboBox.setCurrentIndex)
        #self.ui.dataSourcesListWidget.itemClicked.connect(lambda name: self.controller.loadSource(name.text()))
        #self.ui.dataSourcesListWidget.itemSelectionChanged.connect(self.parent.source_frame.reset)

    def delete_source(self):
        selected_name = self.ui.dataSourcesListWidget.currentItem()
        if selected_name is None:
            return
        selected_name = selected_name.text()

        delete_dialog_title = "Delete Data Source"
        delete_dialog_text = ("Are you sure you want to permanetely delete \"{}\"? "
                              "All associated files will be permanentely removed.").format(selected_name)
        delete_dialog = QMessageBox(
            QMessageBox.Question, 
            delete_dialog_title, 
            delete_dialog_text, 
            QMessageBox.Yes|QMessageBox.No)
        
        if delete_dialog.exec() == QMessageBox.Yes:
            self.controller.delete_source(selected_name)
    
    @Slot()
    def update(self):
        self.ui.dataSourcesListWidget.clear()
        if self.model.dataset_is_open:
            self.ui.dataSourcesListWidget.addItems(self.model.source_names)
            if self.model.selected_source == "Module Layout":
                self.ui.dataSourcesListWidget.setCurrentRow(0)


class SourceFrameView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.ui = Ui_SourceFrame()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.colormapComboBox.addItems(["Gray", "Plasma", "Jet"])
        self.disable()

        # connect signals and slots
        self.model.dataset_opened.connect(self.enable)
        self.model.dataset_closed.connect(self.disable)
        self.model.dataset_closed.connect(lambda _: setattr(self.model.source_frame_model, 'frame', None))
        self.model.track_id_changed.connect(lambda _: self.controller.source_frame_controller.update_source_frame())

        self.ui.minTempSpinBox.valueChanged.connect(lambda value: setattr(self.model.source_frame_model, 'min_temp', value))
        self.model.source_frame_model.min_temp_changed.connect(self.ui.minTempSpinBox.setValue)
        self.ui.maxTempSpinBox.valueChanged.connect(lambda value: setattr(self.model.source_frame_model, 'max_temp', value))
        self.model.source_frame_model.max_temp_changed.connect(self.ui.maxTempSpinBox.setValue)
        self.ui.colormapComboBox.currentIndexChanged.connect(lambda value: setattr(self.model.source_frame_model, 'colormap', value))
        self.model.source_frame_model.colormap_changed.connect(self.ui.colormapComboBox.setCurrentIndex)
        self.model.source_frame_model.min_temp_changed.connect(lambda _: self.controller.source_frame_controller.update_source_frame())
        self.model.source_frame_model.max_temp_changed.connect(lambda _: self.controller.source_frame_controller.update_source_frame())
        self.model.source_frame_model.colormap_changed.connect(lambda _: self.controller.source_frame_controller.update_source_frame())
        self.model.source_frame_model.frame_changed.connect(self.update_source_frame_label)

        # set default values
        self.model.source_frame_model.min_temp = 30
        self.model.source_frame_model.max_temp = 50
        self.model.source_frame_model.colormap = 0
        self.model.source_frame_model.frame = None

    @Slot(object)
    def update_source_frame_label(self, frame):
        w = self.ui.sourceFrameLabel.width()
        h = self.ui.sourceFrameLabel.height()
        self.ui.sourceFrameLabel.setPixmap(frame.scaled(w, h, Qt.KeepAspectRatio))

    def resizeEvent(self, event):
        self.update_source_frame_label(self.model.source_frame_model.frame)

    def disable(self):
        self.ui.minTempSpinBox.setEnabled(False)
        self.ui.maxTempSpinBox.setEnabled(False)
        self.ui.colormapComboBox.setEnabled(False)

    def enable(self):
        self.ui.minTempSpinBox.setEnabled(True)
        self.ui.maxTempSpinBox.setEnabled(True)
        self.ui.colormapComboBox.setEnabled(True)

    # def updatePatches(self, track_id):
    #
    #     return max_temp_patch_idx


class AnalysisModuleTemperatures(QWidget):
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
        self.ui.pushButtonCompute.clicked.connect(self.compute)
        self.ui.pushButtonCancel.clicked.connect(self.cancel)
        self.ui.pushButtonOk.clicked.connect(self.close)

    def reset(self):
        self.thread = None
        self.ui.pushButtonOk.hide()
        self.ui.pushButtonCompute.show()
        self.ui.pushButtonCancel.setEnabled(False)
        self.ui.pushButtonCompute.setEnabled(True)
        self.ui.truncateWidthSpinBox.setEnabled(True)
        self.ui.neighborRadiusSpinBox.setEnabled(True)
        self.ui.progressBar.setValue(0)
        self.ui.progressLabel.setText("")
        time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        self.ui.nameLineEdit.setText("Analysis {}".format(time))

    @Slot()
    def reportProgress(self, progress, cancelled, description=None):
        progress = round(progress*100)
        self.ui.progressBar.setValue(progress)
        if cancelled:
            print("Cancelled module temperature analysis")
            self.ui.progressLabel.setText(description)
            self.ui.pushButtonCompute.hide()
            self.ui.pushButtonOk.show()
            self.ui.pushButtonCancel.setEnabled(False)
        else:
            self.ui.progressLabel.setText(description)
                
    @Slot()
    def compute(self):
        if not self.model.dataset_is_open:
            return
        
        # check if analysis name is not already used
        name = self.ui.nameLineEdit.text()
        if name in self.model.source_names:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("An analysis with this name already exists. Please specify a different name.")
            msg.setIcon(QMessageBox.Critical)
            msg.exec()
            return

        self.ui.pushButtonCancel.setEnabled(True)
        self.ui.pushButtonCompute.setEnabled(False)
        self.ui.truncateWidthSpinBox.setEnabled(False)
        self.ui.neighborRadiusSpinBox.setEnabled(False)
        border_margin = self.ui.truncateWidthSpinBox.value()
        neighbour_radius = self.ui.neighborRadiusSpinBox.value()
        
        # start processing
        self.thread = QThread()
        self.worker = AnalysisModuleTemperaturesWorker(
            self.model.dataset_dir, 
            name,
            border_margin, 
            neighbour_radius)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.finished)
        self.worker.finished.connect(self.controller.update_source_names)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()

    @Slot()
    def finished(self):
        self.ui.pushButtonCompute.hide()
        self.ui.pushButtonOk.show()
        self.ui.pushButtonCancel.setEnabled(False)

    def closeEvent(self, event):
        self.cancel()
        event.accept()

    @Slot()
    def cancel(self):
        if self.thread is not None:
            self.worker.is_cancelled = True


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
        index_file = QDir.current().filePath("index.html")
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
            self.module_temperatures_window = AnalysisModuleTemperatures(self.model, self.controller, self)
        self.module_temperatures_window.reset()
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


########################################################################
#
#       Controllers
#
########################################################################


class SourceFrameController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    @Slot()
    def update_source_frame(self):
        if not self.model.dataset_is_open:
            return None

        if self.model.track_id is None:
            return None

        image_files = sorted(glob.glob(os.path.join(
            self.model.dataset_dir, "patches_final", "radiometric", self.model.track_id, "*")))
        image_file = image_files[self.model.patch_idx]
        source_frame_idx = int(re.findall(r'\d+', os.path.basename(image_file))[0])
        source_frame_file = os.path.join(
            self.model.dataset_dir, "splitted", "radiometric", "frame_{:06d}.tiff".format(source_frame_idx))

        # load frame
        source_frame = cv2.imread(source_frame_file, cv2.IMREAD_ANYDEPTH)
        source_frame = to_celsius(source_frame)
        source_frame = normalize(source_frame, vmin=self.model.source_frame_model.min_temp, vmax=self.model.source_frame_model.max_temp)
        source_frame = cv2.cvtColor(source_frame, cv2.COLOR_GRAY2BGR)
        if self.model.source_frame_model.colormap > 0:
            colormaps = {
                1: cv2.COLORMAP_PLASMA,
                2: cv2.COLORMAP_JET
            }
            colormap = colormaps[self.model.source_frame_model.colormap]
            source_frame = cv2.applyColorMap(source_frame, colormap)

        # load quadrilateral of module and draw onto frame using opencv
        image_file = str.split(os.path.basename(image_file), ".")[0]
        frame_name = image_file[:12]
        mask_name = image_file[13:]
        quadrilateral = np.array(self.model.patch_meta[(self.model.track_id, frame_name, mask_name)]["quadrilateral"])
        source_frame = cv2.polylines(source_frame, [quadrilateral], isClosed=True, color=(0, 255, 0), thickness=3)

        # update source frame
        source_frame = cv2.cvtColor(source_frame, cv2.COLOR_BGR2RGB)
        height, width, _ = source_frame.shape
        bytesPerLine = 3 * width
        qt_source_frame = QImage(
            source_frame.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.model.source_frame_model.frame = QPixmap(qt_source_frame)


class MainController(QObject):
    source_deleted = Signal()

    def __init__(self, model):
        super().__init__()
        self.model = model
        # init subordinate controllers
        self.source_frame_controller = SourceFrameController(self.model)

    @Slot(str)
    def open_dataset(self, dataset_dir):
        self.model.dataset_dir = dataset_dir
        self.model.patch_meta = pickle.load(open(os.path.join(
            self.model.dataset_dir, "patches", "meta.pkl"), "rb"))
        self.update_source_names()
        self.loadSource("Module Layout")
        self.model.dataset_is_open = True

    @Slot()
    def close_dataset(self):
        self.model.reset()
        self.model.dataset_is_open = False

    @Slot()
    def update_source_names(self):
        source_names = []
        if self.model.dataset_dir is not None:
            source_names = sorted(get_immediate_subdirectories(
                os.path.join(self.model.dataset_dir, "analyses")))
        source_names.insert(0, "Module Layout")
        self.model.source_names = source_names

    @Slot(str)
    def loadSource(self, selected_source):
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
        column = columns_names[self.model.selected_column]
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


class SourceFrameModel(QObject):
    min_temp_changed = Signal(int)
    max_temp_changed = Signal(int)
    colormap_changed = Signal(int)
    frame_changed = Signal(object)

    def __init__(self):
        super().__init__()
        self._min_temp = None
        self._max_temp = None
        self._colormap = None
        self._frame = None
    
    @property
    def min_temp(self):
        return self._min_temp

    @min_temp.setter
    def min_temp(self, value):
        self._min_temp = value
        self.min_temp_changed.emit(value)

    @property
    def max_temp(self):
        return self._max_temp

    @max_temp.setter
    def max_temp(self, value):
        self._max_temp = value
        self.max_temp_changed.emit(value)

    @property
    def colormap(self):
        return self._colormap

    @colormap.setter
    def colormap(self, value):
        self._colormap = value
        self.colormap_changed.emit(value)

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value is None:
            value = QPixmap(u"resources/no_image.png")
        self._frame = value
        self.frame_changed.emit(value)


class MainModel(QObject):
    dataset_opened = Signal()
    dataset_closed = Signal()
    source_names_changed = Signal(object)
    selected_source_changed = Signal(str)
    selected_column_changed = Signal(int)
    track_id_changed = Signal(str)
    patch_idx_changed = Signal(int)

    def __init__(self):
        super().__init__()
        # init subordinate models
        self.source_frame_model = SourceFrameModel()
        self.reset()

    def reset(self):
        self.dataset_dir = None
        self.data = None
        self.meta = None
        self.patch_meta = None
        self._source_names = None
        self._dataset_is_open = False
        self._selected_source = None
        self._selected_column = None
        self._track_id = None
        self._patch_idx = None

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



class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_model = MainModel()
        self.main_controller = MainController(self.main_model)
        self.main_view = MainView(self.main_model, self.main_controller)
        self.main_view.show()



if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
