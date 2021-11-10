from PySide6.QtCore import Slot, QObject


class MapController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model
    