
import datetime

from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt, Slot, QThread, Slot, Signal, QObject

from src.ui.ui_analysis import Ui_Analysis
from src.analysis.temperatures import AnalysisModuleTemperaturesWorker
from src.analysis.sun_filter import AnalysisSunFilterWorker


class AnalysisView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # open in new window
        self.model = model
        self.controller = controller
        self.parent = parent
        self.ui = Ui_Analysis()
        self.ui.setupUi(self)
        self.reset()
        # connect signals and slots
        self.model.dataset_closed.connect(self.close)
        self.ui.pushButtonCompute.clicked.connect(self.controller.analysis_controller.compute)
        self.ui.pushButtonCancel.clicked.connect(self.controller.analysis_controller.cancel)
        self.ui.pushButtonOk.clicked.connect(self.close)
        self.model.analysis_model.name_changed.connect(self.ui.nameLineEdit.setText)
        self.ui.nameLineEdit.textChanged.connect(lambda value: setattr(self.model.analysis_model, 'name', value))
        self.model.analysis_model.progress_changed.connect(self.ui.progressBar.setValue)
        self.model.analysis_model.progress_text_changed.connect(self.ui.progressLabel.setText)
        self.controller.analysis_controller.name_exists.connect(self.show_name_exist_dialog)
        self.model.analysis_model.status_changed.connect(self.status_changed)
        self.ui.tabWidget.currentChanged.connect(self.tabChanged)
        self.model.analysis_model.active_tab_widget_changed.connect(self.ui.tabWidget.setCurrentWidget)
        self.model.analysis_model.active_tab_widget_changed.connect(self.active_tab_widget_changed)

        # module temperatures
        self.model.analysis_model.module_temperatures.border_margin_changed.connect(self.ui.spinBoxTruncateWidth.setValue)
        self.ui.spinBoxTruncateWidth.valueChanged.connect(lambda value: setattr(self.model.analysis_model.module_temperatures, 'border_margin', value))
        self.model.analysis_model.module_temperatures.neighbor_radius_changed.connect(self.ui.spinBoxNeighborRadius.setValue)
        self.ui.spinBoxNeighborRadius.valueChanged.connect(lambda value: setattr(self.model.analysis_model.module_temperatures, 'neighbor_radius', value))
        self.model.analysis_model.module_temperatures.ignore_sun_reflections_changed.connect(self.ui.checkBoxIgnoreSunReflections.setChecked)
        self.ui.checkBoxIgnoreSunReflections.stateChanged.connect(lambda value: setattr(self.model.analysis_model.module_temperatures, 'ignore_sun_reflections', bool(value)))
        
        # sun filter
        self.model.analysis_model.sun_filter.threshold_temp_changed.connect(self.ui.spinBoxThresholdTemp.setValue)
        self.ui.spinBoxThresholdTemp.valueChanged.connect(lambda value: setattr(self.model.analysis_model.sun_filter, 'threshold_temp', value))
        self.model.analysis_model.sun_filter.threshold_loc_changed.connect(self.ui.spinBoxThresholdLoc.setValue)
        self.ui.spinBoxThresholdLoc.valueChanged.connect(lambda value: setattr(self.model.analysis_model.sun_filter, 'threshold_loc', value))
        self.model.analysis_model.sun_filter.threshold_changepoint_changed.connect(self.ui.spinBoxThresholdChangepoint.setValue)
        self.ui.spinBoxThresholdChangepoint.valueChanged.connect(lambda value: setattr(self.model.analysis_model.sun_filter, 'threshold_changepoint', value))
        self.model.analysis_model.sun_filter.segment_length_threshold_changed.connect(self.ui.spinBoxSegmentLengthThreshold.setValue)
        self.ui.spinBoxSegmentLengthThreshold.valueChanged.connect(lambda value: setattr(self.model.analysis_model.sun_filter, 'segment_length_threshold', value))

        # set default values
        self.controller.analysis_controller.reset()
        self.model.analysis_model.active_tab_widget = self.ui.tabSunFilter

    def reset(self):
        self.ui.pushButtonOk.hide()
        self.ui.pushButtonCompute.show()
        self.ui.pushButtonCancel.setEnabled(False)
        self.ui.pushButtonCompute.setEnabled(True)
        self.ui.spinBoxTruncateWidth.setEnabled(True)
        self.ui.spinBoxNeighborRadius.setEnabled(True)
        self.ui.spinBoxThresholdTemp.setEnabled(True)
        self.ui.spinBoxThresholdLoc.setEnabled(True)
        self.ui.spinBoxThresholdChangepoint.setEnabled(True)
        self.ui.spinBoxSegmentLengthThreshold.setEnabled(True)
        self.enable_disable_sun_reflections()

    @Slot(int)
    def tabChanged(self, idx):
        self.model.analysis_model.active_tab_widget = self.ui.tabWidget.widget(idx) 

    @Slot(object)
    def active_tab_widget_changed(self, widget):
        if widget.objectName() == "tabSunFilter":
            self.model.analysis_model.name = "Sun Filter"
            self.ui.nameLineEdit.setEnabled(False)
        else:
            time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
            self.model.analysis_model.name = "Analysis {}".format(time)
            self.ui.nameLineEdit.setEnabled(True)

    def enable_disable_sun_reflections(self):
        if self.model.sun_reflections is None:
            self.ui.checkBoxIgnoreSunReflections.setEnabled(False)
        else:
            self.ui.checkBoxIgnoreSunReflections.setEnabled(True)

    @Slot(object)
    def status_changed(self, status):
        if status is None:
            self.reset()
        elif status == "started":
            self.ui.pushButtonCancel.setEnabled(True)
            self.ui.pushButtonCompute.setEnabled(False)
            self.ui.spinBoxTruncateWidth.setEnabled(False)
            self.ui.spinBoxNeighborRadius.setEnabled(False)
            self.ui.checkBoxIgnoreSunReflections.setEnabled(False)
            self.ui.spinBoxThresholdTemp.setEnabled(False)
            self.ui.spinBoxThresholdLoc.setEnabled(False)
            self.ui.spinBoxThresholdChangepoint.setEnabled(False)
            self.ui.spinBoxSegmentLengthThreshold.setEnabled(False)
        elif status == "cancelled":
            self.ui.pushButtonCompute.hide()
            self.ui.pushButtonOk.show()
            self.ui.pushButtonCancel.setEnabled(False)
        elif status == "finished":
            self.ui.pushButtonCompute.hide()
            self.ui.pushButtonOk.show()
            self.ui.pushButtonCancel.setEnabled(False)
            self.controller.update_source_names()
            self.controller.load_sun_reflections()

    @Slot()
    def show_name_exist_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("An analysis with this name already exists. Please specify a different name.")
        msg.setIcon(QMessageBox.Critical)
        msg.exec()

    def closeEvent(self, event):
        self.controller.analysis_controller.cancel()
        event.accept()



class AnalysisController(QObject):
    name_exists = Signal()

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.thread = None
        self.worker = None

    @Slot()
    def reset(self):
        self.model.analysis_model.progress = 0
        self.model.analysis_model.progress_text = ""
        self.model.analysis_model.status = None
        # module temperatures
        self.model.analysis_model.module_temperatures.border_margin = 5
        self.model.analysis_model.module_temperatures.neighbor_radius = 7
        self.model.analysis_model.module_temperatures.ignore_sun_reflections = False
        # sun filter
        self.model.analysis_model.sun_filter.threshold_temp = 5.0
        self.model.analysis_model.sun_filter.threshold_loc = 10.0
        self.model.analysis_model.sun_filter.threshold_changepoint = 10.0
        self.model.analysis_model.sun_filter.segment_length_threshold = 0.3

    @Slot()
    def compute(self):
        if not self.model.dataset_is_open:
            return
        
        if self.model.analysis_model.name in self.model.source_names:
            self.name_exists.emit()
            return

        if not self.model.analysis_model.active_tab_widget or self.model.analysis_model.active_tab_widget.objectName() is None:
            return

        self.model.analysis_model.status = "started"
        self.thread = QThread()
        if self.model.analysis_model.active_tab_widget.objectName() == "tabSunFilter":
            self.worker = AnalysisSunFilterWorker(
                self.model.dataset_dir, 
                self.model.analysis_model.name,
                self.model.analysis_model.sun_filter.threshold_temp, 
                self.model.analysis_model.sun_filter.threshold_loc,
                self.model.analysis_model.sun_filter.threshold_changepoint,
                self.model.analysis_model.sun_filter.segment_length_threshold)
        elif self.model.analysis_model.active_tab_widget.objectName() == "tabModuleTemperatures":
            self.worker = AnalysisModuleTemperaturesWorker(
                self.model.dataset_dir, 
                self.model.analysis_model.name,
                self.model.analysis_model.module_temperatures.border_margin, 
                self.model.analysis_model.module_temperatures.neighbor_radius,
                self.model.analysis_model.module_temperatures.ignore_sun_reflections,
                self.model.sun_reflections)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.report_progress)
        self.worker.finished.connect(lambda: setattr(self.model.analysis_model, 'status', 'finished'))
        self.thread.start()

    @Slot()
    def report_progress(self, progress, cancelled, description=None):
        self.model.analysis_model.progress = round(progress*100)
        self.model.analysis_model.progress_text = description

        if cancelled:
            self.model.analysis_model.status = "cancelled"
            print("Cancelled module temperature analysis")
    
    @Slot()
    def cancel(self):
        if self.thread is not None and self.worker is not None:
            self.worker.is_cancelled = True



class AnalysisModel(QObject):
    name_changed = Signal(str)
    progress_changed = Signal(int)
    progress_text_changed = Signal(str)
    status_changed = Signal(object)
    active_tab_widget_changed = Signal(object)    

    def __init__(self):
        super().__init__()
        self._name = None
        self._progress = None
        self._progress_text = None
        self._status = None
        self._active_tab_widget = None        
        self.module_temperatures = AnalysisModuleTemperaturesModel()
        self.sun_filter = AnalysisSunFilterModel()
        
    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.progress_changed.emit(value)

    @property
    def progress_text(self):
        return self._progress_text

    @progress_text.setter
    def progress_text(self, value):
        self._progress_text = value
        self.progress_text_changed.emit(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(value)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.status_changed.emit(value)

    @property
    def active_tab_widget(self):
        return self._active_tab_widget

    @active_tab_widget.setter
    def active_tab_widget(self, value):
        self._active_tab_widget = value
        self.active_tab_widget_changed.emit(value)



class AnalysisModuleTemperaturesModel(QObject):
    border_margin_changed = Signal(int)
    neighbor_radius_changed = Signal(int)
    ignore_sun_reflections_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self._border_margin = None
        self._neighbor_radius = None
        self._ignore_sun_reflections = None

    @property
    def border_margin(self):
        return self._border_margin

    @border_margin.setter
    def border_margin(self, value):
        self._border_margin = value
        self.border_margin_changed.emit(value)

    @property
    def neighbor_radius(self):
        return self._neighbor_radius

    @neighbor_radius.setter
    def neighbor_radius(self, value):
        self._neighbor_radius = value
        self.neighbor_radius_changed.emit(value)

    @property
    def ignore_sun_reflections(self):
        return self._ignore_sun_reflections

    @ignore_sun_reflections.setter
    def ignore_sun_reflections(self, value):
        self._ignore_sun_reflections = value
        self.ignore_sun_reflections_changed.emit(value)



class AnalysisSunFilterModel(QObject):
    threshold_temp_changed = Signal(float)
    threshold_loc_changed = Signal(float)
    threshold_changepoint_changed = Signal(float)
    segment_length_threshold_changed = Signal(float)

    def __init__(self):
        super().__init__()
        self._threshold_temp = None
        self._threshold_loc = None
        self._threshold_changepoint = None
        self._segment_length_threshold = None

    @property
    def threshold_temp(self):
        return self._threshold_temp

    @threshold_temp.setter
    def threshold_temp(self, value):
        self._threshold_temp = value
        self.threshold_temp_changed.emit(value)

    @property
    def threshold_loc(self):
        return self._threshold_loc

    @threshold_loc.setter
    def threshold_loc(self, value):
        self._threshold_loc = value
        self.threshold_loc_changed.emit(value)

    @property
    def threshold_changepoint(self):
        return self._threshold_changepoint

    @threshold_changepoint.setter
    def threshold_changepoint(self, value):
        self._threshold_changepoint = value
        self.threshold_changepoint_changed.emit(value)

    @property
    def segment_length_threshold(self):
        return self._segment_length_threshold

    @segment_length_threshold.setter
    def segment_length_threshold(self, value):
        self._segment_length_threshold = value
        self.segment_length_threshold_changed.emit(value)