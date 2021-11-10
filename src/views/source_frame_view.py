from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Slot

from src.ui.ui_source_frame import Ui_SourceFrame


class SourceFrameView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.ui = Ui_SourceFrame()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.colormapComboBox.addItems(["Gray", "Plasma", "Jet"])
        self.disable()

        # connect signals and slots
        self.model.dataset_opened.connect(self.enable)
        self.model.dataset_closed.connect(self.disable)
        self.model.dataset_closed.connect(setattr(self.model.source_frame_model, 'frame', None))
        self.model.track_id_changed.connect(lambda _: self.controller.source_frame_controller.update_source_frame())

        self.ui.minTempSpinBox.valueChanged.connect(lambda value: setattr(self.model.source_frame_model, 'min_temp', value))
        self.model.source_frame_model.min_temp_changed.connect(self.ui.minTempSpinBox.setValue)
        self.ui.maxTempSpinBox.valueChanged.connect(lambda value: setattr(self.model.source_frame_model, 'max_temp', value))
        self.model.source_frame_model.max_temp_changed.connect(self.ui.maxTempSpinBox.setValue)
        self.ui.colormapComboBox.currentIndexChanged.connect(lambda value: setattr(self.model.source_frame_model, 'colormap', value))
        self.model.source_frame_model.colormap_changed.connect(self.ui.colormapComboBox.setCurrentIndex)
        self.model.source_frame_model.min_temp_changed.connect(lambda _: self.controller.source_frame_controller.update_source_frame())
        self.model.source_frame_model.max_temp_changed.connect(lambda _: self.controller.source_frame_controller.update_source_frame())
        self.model.source_frame_model.colormap_changed.connect(lambda _: self.controller.source_frame_controller.update_source_frame())
        self.model.source_frame_model.frame_changed.connect(self.update_source_frame_label)

        # set default values
        self.model.source_frame_model.min_temp = 30
        self.model.source_frame_model.max_temp = 50
        self.model.source_frame_model.colormap = 0
        self.model.source_frame_model.frame = None

    @Slot(object)
    def update_source_frame_label(self, frame):
        w = self.ui.sourceFrameLabel.width()
        h = self.ui.sourceFrameLabel.height()
        self.ui.sourceFrameLabel.setPixmap(frame.scaled(w, h, Qt.KeepAspectRatio))

    def resizeEvent(self, event):
        self.update_source_frame_label(self.model.source_frame_model.frame)

    def disable(self):
        self.ui.minTempSpinBox.setEnabled(False)
        self.ui.maxTempSpinBox.setEnabled(False)
        self.ui.colormapComboBox.setEnabled(False)

    def enable(self):
        self.ui.minTempSpinBox.setEnabled(True)
        self.ui.maxTempSpinBox.setEnabled(True)
        self.ui.colormapComboBox.setEnabled(True)

    # def updatePatches(self, track_id):
    #
    #     return max_temp_patch_idx