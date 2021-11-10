from PySide6.QtCore import Signal, QObject


class MapModel(QObject):
    min_temp_changed = Signal(int)
    max_temp_changed = Signal(int)
    colormap_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self._min_temp = None
        self._max_temp = None
        self._colormap = None
    
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