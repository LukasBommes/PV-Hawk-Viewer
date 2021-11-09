from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QPixmap

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
            value = QPixmap(u"src/resources/no_image.png")
        self._frame = value
        self.frame_changed.emit(value)