from PySide6.QtCore import Signal, QObject


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