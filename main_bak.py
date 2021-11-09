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
    QGridLayout, QFileDialog, QBoxLayout
from PySide6.QtCore import QThread, Qt, Slot, Signal, QUrl, QDir, QObject, \
    QSize
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWebChannel import QWebChannel

from ui_mainwindow import Ui_MainWindow
from ui_source_frame import Ui_SourceFrame
from ui_annotation_editor import Ui_AnnotationEditor
from ui_data_sources import Ui_DataSources
from ui_toolbar_temp_range import Ui_TempRange
from ui_toolbar_colormap_selection import Ui_ColormapSelection
from ui_analysis_module_temperatures import Ui_ModuleTemperatures

from common import get_immediate_subdirectories, to_celsius, normalize
from analysis.temperatures import ModuleTemperaturesWorker
from colormap import get_colors


class Backend(QObject):
    dataset_changed = Signal()
    dataset_closed = Signal()

    def __init__(self, parent=None):
        super(Backend, self).__init__()
        self.parent = parent
        # connect signals and slots
        self.parent.dataset.source_deleted.connect(self.dataset_closed)
        self.parent.dataset.changed.connect(self.dataset_changed)
        self.parent.dataset.closed.connect(self.dataset_closed)

    @Slot(str)
    def printObj(self, obj):
        py_obj = json.loads(obj)
        print(py_obj)

    @Slot(result=str)
    def loadData(self):
        data = []
        colors = {}
        if self.parent.dataset.is_open:
            data = self.parent.dataset.data
            column = "mean_of_max_temps_corrected"
            data_column = self.parent.dataset.get_column(column)
            if len(data_column) > 0:
                colors = get_colors(data_column, cmap="plasma", vmin=-5, vmax=5)
            else:
                default_color = "#ff7800"
                track_ids = list(self.parent.dataset.get_column("track_id").values())
                colors = {track_id: default_color for track_id in track_ids}

        print(data, colors)

        return json.dumps({
            "data": data,
            "colors": colors
        })

    @Slot(str)
    def updateImages(self, track_id):
        self.parent.setTrackId(json.loads(track_id))


class AnnotationEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
                print(defect["name"], defect["description"])
                checkbox = QCheckBox("{} - {}".format(defect["name"], defect["description"]))
                checkbox.setToolTip(", ".join(defect["examples"]))
                self.ui.scrollAreaWidgetContents.layout().addWidget(checkbox)
            self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.ui.scrollAreaWidgetContents.layout().addItem(self.verticalSpacer)


class DataSources(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_DataSources()
        self.ui.setupUi(self)
        self.update()
        # connect signals and slots
        self.ui.pushButtonDelete.clicked.connect(self.delete_source)
        self.ui.pushButtonNewAnalysis.clicked.connect(self.parent.show_analysis_module_temperatures)
        self.ui.dataSourcesListWidget.itemClicked.connect(lambda name: self.parent.dataset.loadSource(name.text()))
        self.ui.dataSourcesListWidget.itemClicked.connect(lambda name: self.ui.pushButtonDelete.setEnabled(name.text() != "Module Layout"))
        self.ui.dataSourcesListWidget.itemSelectionChanged.connect(self.parent.source_frame.reset)
        self.parent.dataset.source_names_updated.connect(self.update)
        self.parent.dataset.opened.connect(self.update)
        self.parent.dataset.closed.connect(self.update)
        

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
            self.parent.dataset.delete_source(selected_name)
    
    @Slot()
    def update(self):
        self.ui.dataSourcesListWidget.clear()
        if self.parent.dataset.is_open:
            self.ui.dataSourcesListWidget.addItems(self.parent.dataset.source_names)
            if self.parent.dataset.selected_source == "Module Layout":
                self.ui.dataSourcesListWidget.setCurrentRow(0)


# class TempRangeWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.parent = parent
#         self.ui = Ui_TempRange()
#         self.ui.setupUi(self)
#         # connect signals and slots
#         self.ui.minTempSpinBox.valueChanged.connect(lambda: self.parent.setMinTemp(self.ui.minTempSpinBox.value()))
#         self.ui.maxTempSpinBox.valueChanged.connect(lambda: self.parent.setMaxTemp(self.ui.maxTempSpinBox.value()))


# class ColormapSelectionWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.parent = parent
#         self.ui = Ui_ColormapSelection()
#         self.ui.setupUi(self)
#         self.ui.comboBox.addItems(["Gray", "Plasma", "Jet"])
#         self.ui.comboBox.setCurrentIndex(0)
#         # connect signals and slots
#         self.ui.comboBox.currentIndexChanged.connect(lambda: self.parent.setColormap(self.ui.comboBox.currentIndex()))


class SourceFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SourceFrame()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.colormapComboBox.addItems(["Gray", "Plasma", "Jet"])
        self.ui.colormapComboBox.setCurrentIndex(0)

        self.ui.minTempSpinBox.setEnabled(False)
        self.ui.maxTempSpinBox.setEnabled(False)
        self.ui.colormapComboBox.setEnabled(False)

        # state
        self.min_temp = self.ui.minTempSpinBox.value()
        self.max_temp = self.ui.maxTempSpinBox.value()
        self.colormap = self.setColormap(self.ui.colormapComboBox.currentIndex())

        # connect signals and slots
        self.ui.minTempSpinBox.valueChanged.connect(self.setMinTemp)
        self.ui.maxTempSpinBox.valueChanged.connect(self.setMaxTemp)
        self.ui.colormapComboBox.currentIndexChanged.connect(self.setColormap)

        self.reset()

    @Slot()
    def reset(self):
        self.pixmap = QPixmap(u"resources/no_image.png")
        w = self.ui.sourceFrameLabel.width()
        h = self.ui.sourceFrameLabel.height()
        self.ui.sourceFrameLabel.setPixmap(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))

    def resizeEvent(self, event):
        w = self.ui.sourceFrameLabel.width()
        h = self.ui.sourceFrameLabel.height()
        self.ui.sourceFrameLabel.setPixmap(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))

    def setMinTemp(self, min_temp):
        self.min_temp = min_temp
        self.updateSourceFrame()
    
    def setMaxTemp(self, max_temp):
        self.max_temp = max_temp
        self.updateSourceFrame()

    def setColormap(self, idx):
        if idx > 0:
            colormaps = {
                0: None,
                1: cv2.COLORMAP_PLASMA,
                2: cv2.COLORMAP_JET
            }
            self.colormap = colormaps[idx]
        else:
            self.colormap = None
        self.updateSourceFrame()

    def updateSourceFrame(self):
        if not self.parent.dataset.is_open:
            return None

        if self.parent.track_id is None:
            return None

        image_files = sorted(glob.glob(os.path.join(
            self.parent.dataset.dataset_dir, "patches_final", "radiometric", self.parent.track_id, "*")))
        image_file = image_files[self.parent.patch_idx]
        source_frame_idx = int(re.findall(r'\d+', os.path.basename(image_file))[0])
        source_frame_file = os.path.join(
            self.parent.dataset.dataset_dir, "splitted", "radiometric", "frame_{:06d}.tiff".format(source_frame_idx))

        # load frame
        source_frame = cv2.imread(source_frame_file, cv2.IMREAD_ANYDEPTH)
        source_frame = to_celsius(source_frame)
        source_frame = normalize(source_frame, vmin=self.min_temp, vmax=self.max_temp)
        source_frame = cv2.cvtColor(source_frame, cv2.COLOR_GRAY2BGR)
        if self.colormap is not None:
            source_frame = cv2.applyColorMap(source_frame, self.colormap)

        # load quadrilateral of module and draw onto frame using opencv
        image_file = str.split(os.path.basename(image_file), ".")[0]
        frame_name = image_file[:12]
        mask_name = image_file[13:]
        quadrilateral = np.array(self.parent.dataset.patch_meta[(self.parent.track_id, frame_name, mask_name)]["quadrilateral"])
        source_frame = cv2.polylines(source_frame, [quadrilateral], isClosed=True, color=(0, 255, 0), thickness=3)

        # update source frame
        source_frame = cv2.cvtColor(source_frame, cv2.COLOR_BGR2RGB)
        height, width, _ = source_frame.shape
        bytesPerLine = 3 * width
        qt_source_frame = QImage(
            source_frame.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.pixmap = QPixmap(qt_source_frame)
        w = self.ui.sourceFrameLabel.width()
        h = self.ui.sourceFrameLabel.height()
        self.ui.sourceFrameLabel.setPixmap(
            self.pixmap.scaled(w, h, Qt.KeepAspectRatio))

    # def updatePatches(self, track_id):
    #
    #     return max_temp_patch_idx


class ModuleTemperatures(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # open in new window
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
        if not self.parent.dataset.is_open:
            return
        
        # check if analysis name is not already used
        name = self.ui.nameLineEdit.text()
        if name in self.parent.dataset.source_names:
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
        self.worker = ModuleTemperaturesWorker(
            self.parent.dataset.dataset_dir, 
            name,
            border_margin, 
            neighbour_radius)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.finished)
        self.worker.finished.connect(self.parent.dataset.update_source_names)
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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dataset = Dataset(self)

        self.registerBackend()

        # setup toolbars
        # self.toolBarTempRange = QToolBar(self)
        # self.addToolBar(Qt.TopToolBarArea, self.toolBarTempRange)
        # self.toolBarTempRange.setEnabled(False)
        # self.tempRangeWidget = TempRangeWidget(self)
        # self.toolBarTempRange.addWidget(self.tempRangeWidget)

        # self.toolBarColormapSelection = QToolBar(self)
        # self.addToolBar(Qt.TopToolBarArea, self.toolBarColormapSelection)
        # self.toolBarColormapSelection.setEnabled(False)
        # self.colormapWidget = ColormapSelectionWidget(self)
        # self.toolBarColormapSelection.addWidget(self.colormapWidget)

        # setup widgets
        self.annotationEditorWidget = QDockWidget(u"Annotation Editor", self)
        self.annotation_editor = AnnotationEditor(self)
        self.annotationEditorWidget.setWidget(self.annotation_editor)
        
        self.sourceFrameWidget = QDockWidget(u"Source Frame", self)
        self.source_frame = SourceFrame(self)
        self.sourceFrameWidget.setWidget(self.source_frame)
        
        self.dataSourcesWidget = QDockWidget(u"Data Sources", self)
        self.data_sources = DataSources(self)
        self.dataSourcesWidget.setWidget(self.data_sources)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.dataSourcesWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.annotationEditorWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sourceFrameWidget)

        # child windows
        self.module_temperatures_window = None

        # state
        self.track_id = None  # currently selected module
        self.patch_idx = None

        # connect signals and slots
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionOpen_Dataset.triggered.connect(self.open_dataset)
        self.ui.actionClose_Dataset.triggered.connect(self.dataset.close)
        self.ui.actionNew_Annotation.triggered.connect(self.new_annotation)
        self.ui.actionLoad_Annotation.triggered.connect(self.load_annotation)
        self.ui.actionSave_Annotation.triggered.connect(self.save_annotation)
        self.ui.actionModule_Temperatures.triggered.connect(self.show_analysis_module_temperatures)
        self.ui.menuView.addAction(self.dataSourcesWidget.toggleViewAction())
        self.ui.menuView.addAction(self.annotationEditorWidget.toggleViewAction())
        self.ui.menuView.addAction(self.sourceFrameWidget.toggleViewAction())
        self.dataset.opened.connect(self.dataset_opened)
        self.dataset.closed.connect(self.dataset_closed)
        
        self.loadMainDocument()

    def registerBackend(self):
        self.backend = Backend(self)
        channel = QWebChannel(self.ui.widget.page())
        self.ui.widget.page().setWebChannel(channel)
        channel.registerObject("backend", self.backend)

    def loadMainDocument(self):
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
            self.dataset.open(dir)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Not a valid PV Mapper Dataset.")
            msg.setIcon(QMessageBox.Critical)
            msg.exec()

    @Slot()
    def dataset_opened(self):
        self.ui.actionClose_Dataset.setEnabled(True)
        self.ui.actionOpen_Dataset.setEnabled(False)
        self.ui.actionModule_Temperatures.setEnabled(True)
        self.data_sources.ui.pushButtonNewAnalysis.setEnabled(True)
        self.source_frame.ui.minTempSpinBox.setEnabled(True)
        self.source_frame.ui.maxTempSpinBox.setEnabled(True)
        self.source_frame.ui.colormapComboBox.setEnabled(True)

    @Slot()
    def dataset_closed(self):
        self.source_frame.reset()
        self.ui.actionClose_Dataset.setEnabled(False)
        self.ui.actionOpen_Dataset.setEnabled(True)        
        self.ui.actionModule_Temperatures.setEnabled(False)
        self.data_sources.ui.pushButtonDelete.setEnabled(False)
        self.source_frame.ui.minTempSpinBox.setEnabled(False)
        self.source_frame.ui.maxTempSpinBox.setEnabled(False)
        self.source_frame.ui.colormapComboBox.setEnabled(False)


    def setTrackId(self, track_id):
        self.track_id = track_id
        self.patch_idx = 0
        self.source_frame.updateSourceFrame()

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
        if not self.dataset.is_open:
            return
        if self.module_temperatures_window is None:
            self.module_temperatures_window = ModuleTemperatures(self)
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


class Dataset(QObject):
    opened = Signal()
    closed = Signal()
    changed = Signal()
    source_deleted = Signal()
    source_names_updated = Signal()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.reset()

    def reset(self):
        self.dataset_dir = None
        self.selected_source = None
        self.source_names = None
        self.data = None
        self.meta = None
        self.patch_meta = None
        self.is_open = False

    def get_column(self, column):
        if self.dataset_dir is None:
            return {}
        column_values = {}
        for feature in self.data["features"]:
            track_id = feature["properties"]["track_id"]
            try:
                val = feature["properties"][column]
                if val is None:
                    val = np.nan
                column_values[track_id] = val
            except KeyError:
                continue
        return column_values

    @Slot()
    def update_source_names(self):
        self.source_names = []
        if self.dataset_dir is not None:
            self.source_names = sorted(get_immediate_subdirectories(
                os.path.join(self.dataset_dir, "analyses")))
        self.source_names.insert(0, "Module Layout")
        self.source_names_updated.emit()

    def delete_source(self, selected_source):
        if self.dataset_dir is None:
            return
        if selected_source is None:
            return
        if selected_source == "Module Layout":
            return
        if selected_source == self.selected_source:
            self.source_deleted.emit()
        rmdir = os.path.join(self.dataset_dir, "analyses", selected_source)
        print("Deleting {}".format(rmdir))
        shutil.rmtree(rmdir, ignore_errors=True)
        self.update_source_names()

    @Slot(str)
    def open(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.patch_meta = pickle.load(open(os.path.join(
            self.dataset_dir, "patches", "meta.pkl"), "rb"))
        self.update_source_names()
        self.loadSource("Module Layout")
        self.is_open = True
        self.opened.emit()

    @Slot()
    def close(self):
        self.reset()
        self.is_open = False
        self.closed.emit()

    @Slot(str)
    def loadSource(self, selected_source):
        print("Updating", selected_source)
        if self.dataset_dir is None:
            return
        if selected_source is None:
            return
        self.selected_source = selected_source

        if selected_source == "Module Layout":
            self.data = json.load(open(os.path.join(
                self.dataset_dir, "mapping", "module_geolocations_refined.geojson"), "r"))
            self.meta = None            
        else:
            self.data = json.load(open(os.path.join(
                self.dataset_dir, "analyses", selected_source, "results.geojson"), "r"))
            self.meta = json.load(open(os.path.join(
                self.dataset_dir, "analyses", selected_source, "meta.json"), "r"))
        self.changed.emit()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())