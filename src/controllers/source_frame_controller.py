import os
import glob
import re
import cv2
import numpy as np

from PySide6.QtCore import Slot, QObject
from PySide6.QtGui import QPixmap, QImage

from src.common import to_celsius, normalize


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