from PySide6.QtCore import Signal, QObject


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