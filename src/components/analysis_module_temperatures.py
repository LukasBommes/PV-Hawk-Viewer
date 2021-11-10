
import datetime

from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt, Slot, QThread, Slot, Signal, QObject

from src.ui.ui_analysis_module_temperatures import Ui_ModuleTemperatures
from src.analysis.temperatures import AnalysisModuleTemperaturesWorker


class AnalysisModuleTemperaturesView(QWidget):
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
        self.ui.pushButtonCompute.clicked.connect(self.controller.analysis_module_temperatures_controller.compute)
        self.ui.pushButtonCancel.clicked.connect(self.controller.analysis_module_temperatures_controller.cancel)
        self.ui.pushButtonOk.clicked.connect(self.close)
        self.model.analysis_module_temperatures_model.name_changed.connect(self.ui.nameLineEdit.setText)
        self.ui.nameLineEdit.textChanged.connect(lambda value: setattr(self.model.analysis_module_temperatures_model, 'name', value))
        self.model.analysis_module_temperatures_model.border_margin_changed.connect(self.ui.truncateWidthSpinBox.setValue)
        self.ui.truncateWidthSpinBox.valueChanged.connect(lambda value: setattr(self.model.analysis_module_temperatures_model, 'border_margin', value))
        self.model.analysis_module_temperatures_model.neighbor_radius_changed.connect(self.ui.neighborRadiusSpinBox.setValue)
        self.ui.neighborRadiusSpinBox.valueChanged.connect(lambda value: setattr(self.model.analysis_module_temperatures_model, 'neighbor_radius', value))
        self.model.analysis_module_temperatures_model.progress_changed.connect(self.ui.progressBar.setValue)
        self.model.analysis_module_temperatures_model.progress_text_changed.connect(self.ui.progressLabel.setText)

        self.controller.analysis_module_temperatures_controller.name_exists.connect(self.show_name_exist_dialog)
        self.model.analysis_module_temperatures_model.status_changed.connect(self.status_changed)

        # set default values
        self.controller.analysis_module_temperatures_controller.reset()

    def reset(self):
        self.ui.pushButtonOk.hide()
        self.ui.pushButtonCompute.show()
        self.ui.pushButtonCancel.setEnabled(False)
        self.ui.pushButtonCompute.setEnabled(True)
        self.ui.truncateWidthSpinBox.setEnabled(True)
        self.ui.neighborRadiusSpinBox.setEnabled(True)

    @Slot(object)
    def status_changed(self, status):
        if status is None:
            self.reset()
        elif status == "started":
            self.ui.pushButtonCancel.setEnabled(True)
            self.ui.pushButtonCompute.setEnabled(False)
            self.ui.truncateWidthSpinBox.setEnabled(False)
            self.ui.neighborRadiusSpinBox.setEnabled(False)
        elif status == "cancelled":
            self.ui.pushButtonCompute.hide()
            self.ui.pushButtonOk.show()
            self.ui.pushButtonCancel.setEnabled(False)
        elif status == "finished":
            self.ui.pushButtonCompute.hide()
            self.ui.pushButtonOk.show()
            self.ui.pushButtonCancel.setEnabled(False)
            self.controller.update_source_names()

    @Slot()
    def show_name_exist_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("An analysis with this name already exists. Please specify a different name.")
        msg.setIcon(QMessageBox.Critical)
        msg.exec()

    def closeEvent(self, event):
        self.controller.analysis_module_temperatures_controller.cancel()
        event.accept()



class AnalysisModuleTemperaturesController(QObject):
    name_exists = Signal()

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.thread = None
        self.worker = None

    @Slot()
    def reset(self):
        print("Resetting AnalysisModuleTemperaturesModel")
        time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        self.model.analysis_module_temperatures_model.name = "Analysis {}".format(time)
        self.model.analysis_module_temperatures_model.border_margin = 5
        self.model.analysis_module_temperatures_model.neighbor_radius = 7
        self.model.analysis_module_temperatures_model.progress = 0
        self.model.analysis_module_temperatures_model.progress_text = ""
        self.model.analysis_module_temperatures_model.status = None

    @Slot()
    def compute(self):
        if not self.model.dataset_is_open:
            return
        
        if self.model.analysis_module_temperatures_model.name in self.model.source_names:
            self.name_exists.emit()
            return

        self.model.analysis_module_temperatures_model.status = "started"
        self.thread = QThread()
        self.worker = AnalysisModuleTemperaturesWorker(
            self.model.dataset_dir, 
            self.model.analysis_module_temperatures_model.name,
            self.model.analysis_module_temperatures_model.border_margin, 
            self.model.analysis_module_temperatures_model.neighbor_radius)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.report_progress)
        self.worker.finished.connect(lambda: setattr(self.model.analysis_module_temperatures_model, 'status', 'finished'))
        self.thread.start()

    @Slot()
    def report_progress(self, progress, cancelled, description=None):
        self.model.analysis_module_temperatures_model.progress = round(progress*100)
        self.model.analysis_module_temperatures_model.progress_text = description

        if cancelled:
            self.model.analysis_module_temperatures_model.status = "cancelled"
            print("Cancelled module temperature analysis")
    
    @Slot()
    def cancel(self):
        if self.thread is not None and self.worker is not None:
            self.worker.is_cancelled = True



class AnalysisModuleTemperaturesModel(QObject):
    name_changed = Signal(str)
    border_margin_changed = Signal(int)
    neighbor_radius_changed = Signal(int)
    progress_changed = Signal(int)
    progress_text_changed = Signal(str)
    status_changed = Signal(object)

    def __init__(self):
        super().__init__()
        self._name = None
        self._border_margin = None
        self._neighbor_radius = None
        self._progress = None
        self._progress_text = None
        self._status = None

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