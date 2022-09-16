import os
import glob
import re
import pkg_resources
import cv2
import numpy as np

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Slot, Signal, QObject
from PySide6.QtGui import QPixmap, QImage

from ..ui.ui_source_frame_rgb import Ui_SourceFrame
from ..utils.common import to_celsius, normalize


class SourceFrameViewRGB(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.ui = Ui_SourceFrame()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.sourceFrameLabel.setGeometry(0, 0, 640, 512)  # initial size
        self.disable()

        # connect signals and slots
        self.model.dataset_opened.connect(self.enable)
        self.model.dataset_closed.connect(self.disable)
        self.model.track_id_changed.connect(lambda _: self.controller.source_frame_controller_rgb.update_source_frame())
        self.model.source_frame_model_rgb.frame_changed.connect(self.update_source_frame_label)
        self.controller.source_deleted.connect(lambda: setattr(self.model.source_frame_model_rgb, 'frame', None))

        # set default values
        self.model.source_frame_model_rgb.frame = None

    @Slot(object)
    def update_source_frame_label(self, frame):
        w = self.ui.sourceFrameLabel.width()
        h = self.ui.sourceFrameLabel.height()
        self.ui.sourceFrameLabel.setPixmap(frame.scaled(w, h, Qt.KeepAspectRatio))

    def resizeEvent(self, event):
        self.update_source_frame_label(self.model.source_frame_model_rgb.frame)

    def disable(self):
        pass

    def enable(self):
        pass



class SourceFrameControllerRGB(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    @Slot()
    def update_source_frame(self):
        if not self.model.dataset_is_open:
            self.model.source_frame_model_rgb.frame = None
            return None

        if self.model.track_id is None:
            self.model.source_frame_model_rgb.frame = None
            return None

        # v1 dataset never has rgb frames, so this widget will only be active for v2 datasets
        #if self.model.dataset_version == "v1":
        #    patches_dir = os.path.join(self.model.dataset_dir, "patches_final", "radiometric")
        #elif self.model.dataset_version == "v2":
        patches_dir = os.path.join(self.model.dataset_dir, "patches", "radiometric")
        image_files = sorted(glob.glob(os.path.join(patches_dir, self.model.track_id, "*")))
        image_file = image_files[0]  # TODO: set based on heuristic, e.g. select patch with maximum temperature (make setting for this in preferences)
        source_frame_idx = int(re.findall(r'\d+', os.path.basename(image_file))[0])
        source_frame_file = os.path.join(
            self.model.dataset_dir, "splitted", "rgb", "frame_{:06d}.jpg".format(source_frame_idx))

        # load frame
        source_frame = cv2.imread(source_frame_file, cv2.IMREAD_COLOR)

        # load quadrilateral of module and draw onto frame using opencv
        if self.model.ir_or_rgb == "rgb":
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

        self.model.source_frame_model_rgb.frame = QPixmap(qt_source_frame)



class SourceFrameModelRGB(QObject):
    frame_changed = Signal(object)

    def __init__(self):
        super().__init__()
        self._frame = None

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value is None:
            value = QPixmap(pkg_resources.resource_filename("src.resources", "no_image.png"))
        self._frame = value
        self.frame_changed.emit(value)