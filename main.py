import sys
import os
import re
import glob
import json
import pickle
import cv2
import numpy as np

from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, \
    QDockWidget, QMessageBox, QCheckBox, QSpacerItem, QSizePolicy, QLabel, \
    QGridLayout, QFileDialog
from PySide6.QtCore import QThread, Qt, Slot, Signal, QUrl, QDir, QObject, \
    QSize, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtWebChannel import QWebChannel

from ui_mainwindow import Ui_MainWindow
from ui_annotation_editor import Ui_AnnotationEditor
from ui_analysis_results import Ui_AnalysisResults
from ui_toolbar_temp_range import Ui_TempRange
from ui_toolbar_colormap_selection import Ui_ColormapSelection
from ui_analysis_module_temperatures import Ui_ModuleTemperatures

from common import get_immediate_subdirectories, to_celsius, normalize
from analysis.temperatures import ModuleTemperaturesWorker


class Backend(QObject):
    openDatasetSignal = Signal()
    closeDatasetSignal = Signal()

    def __init__(self, parent=None):
        super(Backend, self).__init__()
        self.parent = parent

    @Slot(str)
    def printObj(self, obj):
        py_obj = json.loads(obj)
        print(py_obj)

    @Slot(result=str)
    def loadModules(self):
        if self.parent.dataset_dir is None:
            return json.dumps([])
        else:
            # module_file = os.path.join(
            #     self.parent.dataset_dir, "mapping", "module_geolocations_refined.geojson")
            #module_file = os.path.join(
            #    self.parent.dataset_dir, "temperatures", "module_temperatures.geojson")
            #modules = json.load(open(module_file, "r"))
            return json.dumps(self.parent.analysis_data.modules)

    # @Slot(result=str)
    # def loadAnalysisData(self):
    #     if self.parent.dataset_dir is None:
    #         return json.dumps([])
    #     else:
            
    #         return json.dumps(modules)

    @Slot(str)
    def updateImages(self, track_id):
        self.parent.setTrackId(json.loads(track_id))


class AnnotationEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AnnotationEditor()
        self.ui.setupUi(self)
        self.loadDefectsScheme()
        self.connectSignalsSlots()

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

    def connectSignalsSlots(self):
        pass


class SourceFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gridLayout = QGridLayout(self)
        self.label = QLabel(self)
        self.label.setMinimumSize(QSize(50, 50))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.reset()

    def reset(self):
        self.pixmap = QPixmap(u"resources/no_image.png")
        w = self.label.width()
        h = self.label.height()
        self.label.setPixmap(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))

    def resizeEvent(self, event):
        w = self.label.width()
        h = self.label.height()
        self.label.setPixmap(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))


class AnalysisResults(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_AnalysisResults()
        self.ui.setupUi(self)
        self.update()
        self.connectSignalsSlots()        

    def connectSignalsSlots(self):
        pass

    def update(self):
        self.analysis_results_model = AnalysisResultsTableModel(self.parent)
        self.ui.analysisResultsTableView.setModel(self.analysis_results_model)


class AnalysisResultsTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self)
        self.parent = parent
        self.load_data()

    def load_data(self):
        self.analysis_files = []
        self.analysis_types = []
        if self.parent.dataset_dir is not None:
            self.analysis_files = sorted(get_immediate_subdirectories(
                os.path.join(self.parent.dataset_dir, "analyses")))
            for analysis_file in self.analysis_files:
                meta = json.load(open(os.path.join(self.parent.dataset_dir, "analyses", analysis_file, "meta.json"), "r"))
                analysis_type = meta["type"]
                self.analysis_types.append(analysis_type)

        self.column_count = 2
        self.row_count = len(self.analysis_files)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Name", "Type")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if column == 0:
                #date = self.input_dates[row].toPython()
                #return str(date)[:-3]
                return str(self.analysis_files[row])
            elif column == 1:
                #magnitude = self.input_magnitudes[row]
                #return f"{magnitude:.2f}"
                return str(self.analysis_types[row])
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignLeft
        return None


class TempRangeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_TempRange()
        self.ui.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.ui.minTempSpinBox.valueChanged.connect(lambda: self.parent.setMinTemp(self.ui.minTempSpinBox.value()))
        self.ui.maxTempSpinBox.valueChanged.connect(lambda: self.parent.setMaxTemp(self.ui.maxTempSpinBox.value()))


class ColormapSelectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_ColormapSelection()
        self.ui.setupUi(self)
        self.ui.comboBox.addItems(["Gray", "Plasma", "Jet"])
        self.ui.comboBox.setCurrentIndex(0)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.ui.comboBox.currentIndexChanged.connect(lambda: self.parent.setColormap(self.ui.comboBox.currentIndex()))


class ModuleTemperatures(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # open in new window
        self.parent = parent
        self.ui = Ui_ModuleTemperatures()
        self.ui.setupUi(self)
        self.reset()
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
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

    @Slot()
    def reportProgress(self, progress, cancelled, description=None):
        progress = round(progress*100)
        self.ui.progressBar.setValue(progress)
        if cancelled:
            self.ui.progressLabel.setText(description)
            self.ui.pushButtonCompute.hide()
            self.ui.pushButtonOk.show()
            self.ui.pushButtonCancel.setEnabled(False)
        else:
            self.ui.progressLabel.setText(description)
                
    @Slot()
    def compute(self):
        if self.parent.dataset_dir is None:
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
            self.parent.dataset_dir, border_margin, neighbour_radius)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.finished)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()

    @Slot()
    def finished(self):
        self.ui.progressLabel.setText("Done")
        self.ui.pushButtonCompute.hide()
        self.ui.pushButtonOk.show()
        self.ui.pushButtonCancel.setEnabled(False)
        # update analysis result files list
        self.parent.analysis_results.update()

    @Slot()
    def cancel(self):
        if self.thread is not None:
            self.worker.is_cancelled = True


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dataset_dir = None
        self.analysis_data = None

        # setup toolbars
        self.toolBarTempRange = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBarTempRange)
        self.toolBarTempRange.setEnabled(False)
        self.tempRangeWidget = TempRangeWidget(self)
        self.toolBarTempRange.addWidget(self.tempRangeWidget)

        self.toolBarColormapSelection = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBarColormapSelection)
        self.toolBarColormapSelection.setEnabled(False)
        self.dataSelectionWidget = ColormapSelectionWidget(self)
        self.toolBarColormapSelection.addWidget(self.dataSelectionWidget)

        # setup widgets
        self.analysisResultsWidget = QDockWidget(u"Analysis Results", self)
        self.analysis_results = AnalysisResults(self)
        self.analysisResultsWidget.setWidget(self.analysis_results)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.analysisResultsWidget)

        self.annotationEditorWidget = QDockWidget(u"Annotation Editor", self)
        self.annotation_editor = AnnotationEditor(self)
        self.annotationEditorWidget.setWidget(self.annotation_editor)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.annotationEditorWidget)

        self.sourceFrameWidget = QDockWidget(u"Source Frame", self)
        self.source_frame = SourceFrame(self)
        self.sourceFrameWidget.setWidget(self.source_frame)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sourceFrameWidget)

        # child windows
        self.module_temperatures_window = None

        # state
        self.min_temp = self.tempRangeWidget.ui.minTempSpinBox.value()
        self.max_temp = self.tempRangeWidget.ui.maxTempSpinBox.value()
        self.colormap = self.setColormap(self.dataSelectionWidget.ui.comboBox.currentIndex())
        self.track_id = None  # currently selected module
        self.patch_idx = None

        self.connectSignalsSlots()
        self.registerBackend()
        self.loadMainDocument()

    def connectSignalsSlots(self):
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionOpen_Dataset.triggered.connect(self.open_dataset)
        self.ui.actionClose_Dataset.triggered.connect(self.close_dataset)
        self.ui.actionNew_Annotation.triggered.connect(self.new_annotation)
        self.ui.actionLoad_Annotation.triggered.connect(self.load_annotation)
        self.ui.actionSave_Annotation.triggered.connect(self.save_annotation)
        self.ui.actionModule_Temperatures.triggered.connect(self.show_analysis_module_temperatures)
        self.ui.menuView.addAction(self.analysisResultsWidget.toggleViewAction())
        self.ui.menuView.addAction(self.annotationEditorWidget.toggleViewAction())
        self.ui.menuView.addAction(self.sourceFrameWidget.toggleViewAction())

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
            self.dataset_dir = dir
            # load dataset
            self.analysis_data = AnalysisData(self.dataset_dir)
            self.backend.openDatasetSignal.emit()
            # update analysis result files list
            self.analysis_results.update()
            # activate close dialog and toolbar
            self.ui.actionClose_Dataset.setEnabled(True)
            self.ui.actionOpen_Dataset.setEnabled(False)
            self.toolBarTempRange.setEnabled(True)
            self.toolBarColormapSelection.setEnabled(True)
            self.ui.actionModule_Temperatures.setEnabled(True)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Not a valid PV Mapper Dataset.")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    @Slot()
    def close_dataset(self):
        self.dataset_dir = None
        self.analysis_data = None
        self.backend.closeDatasetSignal.emit()
        # remove source frame and patches
        self.source_frame.reset()
        # update analysis result files list
        self.analysis_results.update()
        # deactivate close dialog and toolbar
        self.ui.actionClose_Dataset.setEnabled(False)
        self.ui.actionOpen_Dataset.setEnabled(True)
        self.toolBarTempRange.setEnabled(False)
        self.toolBarColormapSelection.setEnabled(False)
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

    def setTrackId(self, track_id):
        self.track_id = track_id
        self.patch_idx = 0
        self.updateSourceFrame()

    def updateSourceFrame(self):
        if self.dataset_dir is None:
            return None

        if self.track_id is None:
            return None

        image_files = sorted(glob.glob(os.path.join(
            self.dataset_dir, "patches_final", "radiometric", self.track_id, "*")))
        image_file = image_files[self.patch_idx]
        source_frame_idx = int(re.findall(r'\d+', os.path.basename(image_file))[0])
        source_frame_file = os.path.join(
            self.dataset_dir, "splitted", "radiometric", "frame_{:06d}.tiff".format(source_frame_idx))

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
        quadrilateral = np.array(self.analysis_data.patch_meta[(self.track_id, frame_name, mask_name)]["quadrilateral"])
        source_frame = cv2.polylines(source_frame, [quadrilateral], isClosed=True, color=(0, 255, 0), thickness=3)

        # update source frame
        source_frame = cv2.cvtColor(source_frame, cv2.COLOR_BGR2RGB)
        height, width, _ = source_frame.shape
        bytesPerLine = 3 * width
        qt_source_frame = QImage(
            source_frame.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.source_frame.pixmap = QPixmap(qt_source_frame)
        w = self.source_frame.label.width()
        h = self.source_frame.label.height()
        self.source_frame.label.setPixmap(
            self.source_frame.pixmap.scaled(w, h, Qt.KeepAspectRatio))

    # def updatePatches(self, track_id):
    #
    #     return max_temp_patch_idx


class AnalysisData:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

        # load data
        if self.dataset_dir is not None:
            self.patch_meta = pickle.load(open(os.path.join(
                self.dataset_dir, "patches", "meta.pkl"), "rb"))

            # module coordinates
            self.modules = json.load(open(os.path.join(
                self.dataset_dir, "mapping", "module_geolocations_refined.geojson"), "r"))

            # load other available analysis data
            os.makedirs(os.path.join(self.dataset_dir, "analyses"), exist_ok=True)
            self.analyses = sorted(get_immediate_subdirectories(os.path.join(self.dataset_dir, "analyses")))
            print(self.analyses)

    # def load(self):
    #     pass

    # def save(self):
    #     pass

    # def compute_column_ranges(self):
    #     pass



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
