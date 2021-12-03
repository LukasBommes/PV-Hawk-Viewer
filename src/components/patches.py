import os
import glob
import cv2

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, \
    QScrollArea
from PySide6.QtCore import Qt, Slot, Signal, QObject, QRect
from PySide6.QtGui import QPixmap, QImage

from src.common import to_celsius, normalize
from src.analysis.temperatures import truncate_patch
from src.flow_layout import FlowLayout



class PatchesView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.parent = parent
        self.build_ui()
        # connect signals and slots
        self.model.track_id_changed.connect(lambda _: self.controller.patches_controller.update_patches())
        self.model.patches_model.patches_changed.connect(self.update_patches_labels)
        self.model.source_frame_model.min_temp_changed.connect(lambda _: self.controller.patches_controller.update_patches())
        self.model.source_frame_model.max_temp_changed.connect(lambda _: self.controller.patches_controller.update_patches())
        self.model.source_frame_model.colormap_changed.connect(lambda _: self.controller.patches_controller.update_patches())
        self.controller.source_deleted.connect(lambda: setattr(self.model.patches_model, 'patches', None))

        # set default values
        self.model.patches_model.patches = None

    def build_ui(self):
        self.grid_layout = QGridLayout(self)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.inner = QWidget(self.scrollArea)
        self.inner.setLayout(FlowLayout())
        self.scrollArea.setWidget(self.inner)
        self.grid_layout.addWidget(self.scrollArea, 0, 0, 1, 1)        

    def clear_patches(self):
        while self.inner.layout().count():
            child = self.inner.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    @Slot(object)
    def update_patches_labels(self, patches):
        self.clear_patches()
        if patches is None:
            self.clear_patches()
            return
        images, statistics = patches     
        for patch, stats in zip(images, statistics):
            # convert to QPixmap
            height, width, _ = patch.shape
            bytesPerLine = 3 * width
            patch = QPixmap(QImage(
                patch.data, width, height, bytesPerLine, QImage.Format_RGB888))
            display_width = 100
            display_height = 160
            label = QLabel(self)
            label.setPixmap(patch.scaled(display_width, display_height))
            label.setToolTip(                
                "Mean Temp: {:0.2f} °C<br>".format(stats["mean_temp"]) + 
                "Max Temp: {:0.2f} °C<br>".format(stats["max_temp"]) +
                "Size: {} x {} px".format(*stats["shape"])
                )
            self.inner.layout().addWidget(label)



class PatchesController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    @Slot()
    def update_patches(self):
        if not self.model.dataset_is_open:
            self.model.patches_model.patches = None
            return

        if self.model.track_id is None:
            self.model.patches_model.patches = None
            return

        # load patches from directory
        image_files = sorted(glob.glob(os.path.join(
            self.model.dataset_dir, "patches_final", "radiometric", self.model.track_id, "*")))
        
        images = []
        statistics = []
        for image_file in image_files:
            image = cv2.imread(image_file, cv2.IMREAD_ANYDEPTH)
            image = to_celsius(image)
            image_cropped = truncate_patch(image, margin=0.05)
            stats = {
                "max_temp": image_cropped.max(),
                "mean_temp": image_cropped.mean(),
                "shape": image.shape[:2]
            }
            image = normalize(image, vmin=self.model.source_frame_model.min_temp, vmax=self.model.source_frame_model.max_temp)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            if self.model.source_frame_model.colormap > 0:
                colormaps = {
                    1: cv2.COLORMAP_PLASMA,
                    2: cv2.COLORMAP_JET
                }
                colormap = colormaps[self.model.source_frame_model.colormap]
                image = cv2.applyColorMap(image, colormap)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            images.append(image)
            statistics.append(stats)
        
        self.model.patches_model.patches = (images, statistics)



class PatchesModel(QObject):
    patches_changed = Signal(object)

    def __init__(self):
        super().__init__()
        self._patches = None
    
    @property
    def patches(self):
        return self._patches

    @patches.setter
    def patches(self, value):
        self._patches = value
        self.patches_changed.emit(value)
