import datetime
from PySide6.QtCore import QThread, Slot, Signal, QObject

from src.analysis.temperatures import AnalysisModuleTemperaturesWorker


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