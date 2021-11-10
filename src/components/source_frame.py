import os
import glob
import re
import cv2
import numpy as np

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Slot, Signal, QObject
from PySide6.QtGui import QPixmap, QImage

from src.ui.ui_source_frame import Ui_SourceFrame
from src.common import to_celsius, normalize


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



class SourceFrameController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    @Slot()
    def update_source_frame(self):
        if not self.model.dataset_is_open:
            return None

        if self.model.track_id is None:
            return None

        image_files = sorted(glob.glob(os.path.join(
            self.model.dataset_dir, "patches_final", "radiometric", self.model.track_id, "*")))
        image_file = image_files[self.model.patch_idx]
        source_frame_idx = int(re.findall(r'\d+', os.path.basename(image_file))[0])
        source_frame_file = os.path.join(
            self.model.dataset_dir, "splitted", "radiometric", "frame_{:06d}.tiff".format(source_frame_idx))

        # load frame
        source_frame = cv2.imread(source_frame_file, cv2.IMREAD_ANYDEPTH)
        source_frame = to_celsius(source_frame)
        source_frame = normalize(source_frame, vmin=self.model.source_frame_model.min_temp, vmax=self.model.source_frame_model.max_temp)
        source_frame = cv2.cvtColor(source_frame, cv2.COLOR_GRAY2BGR)
        if self.model.source_frame_model.colormap > 0:
            colormaps = {
                1: cv2.COLORMAP_PLASMA,
                2: cv2.COLORMAP_JET
            }
            colormap = colormaps[self.model.source_frame_model.colormap]
            source_frame = cv2.applyColorMap(source_frame, colormap)

        # load quadrilateral of module and draw onto frame using opencv
        image_file = str.split(os.path.basename(image_file), ".")[0]
        frame_name = image_file[:12]
        mask_name = image_file[13:]
        quadrilateral = np.array(self.model.patch_meta[(self.model.track_id, frame_name, mask_name)]["quadrilateral"])
        source_frame = cv2.polylines(source_frame, [quadrilateral], isClosed=True, color=(0, 255, 0), thickness=3)

        # update source frame
        source_frame = cv2.cvtColor(source_frame, cv2.COLOR_BGR2RGB)
        height, width, _ = source_frame.shape
        bytesPerLine = 3 * width
        qt_source_frame = QImage(
            source_frame.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.model.source_frame_model.frame = QPixmap(qt_source_frame)



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