import os
import glob
import pkg_resources
import cv2

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, \
    QScrollArea
from PySide6.QtCore import Qt, Slot, Signal, QObject, QPoint
from PySide6.QtGui import QPixmap, QImage, QPainter

from ..utils.common import to_celsius, normalize
from ..utils.flow_layout import FlowLayout
from ..analysis.temperatures import truncate_patch



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
        self.model.sun_reflections_changed.connect(self.controller.patches_controller.update_patches)

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

    def overlay_pixmaps(self, p1, p2, padding=3):
        s = p1.size().expandedTo(p2.size())
        result =  QPixmap(s)
        result.fill(Qt.transparent)
        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(QPoint(), p1)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(QPoint(padding, padding), p2)
        painter.end()
        return result

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
            patch = patch.scaled(display_width, display_height)

            tooltip = ("Mean Temp: {:0.2f} °C<br>".format(stats["mean_temp"]) + 
                "Max Temp: {:0.2f} °C<br>".format(stats["max_temp"]) +
                "Size: {} x {} px<br>".format(*stats["shape"]))

            if "sun_reflection" in stats:
                if stats["sun_reflection"]:
                    tooltip += "Sun Reflection: yes"
                    has_sun_reflection_icon = QPixmap(pkg_resources.resource_filename("src.resources", "sun_icon.png"))
                else:
                    tooltip += "Sun Reflection: no"
                    has_sun_reflection_icon = QPixmap(pkg_resources.resource_filename("src.resources", "no_sun_icon.png"))

                # draw sun icon to indicate whether patch has sun reflection
                has_sun_reflection_icon = has_sun_reflection_icon.scaled(16, 16)
                label.setPixmap(self.overlay_pixmaps(patch, has_sun_reflection_icon))
            else:
                tooltip += "Sun Reflection: n.A."
                label.setPixmap(patch)

            label.setToolTip(tooltip)
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

        track_id = self.model.track_id
        if track_id is None:
            self.model.patches_model.patches = None
            return

        # load patches from directory
        image_files = sorted(glob.glob(os.path.join(
            self.model.dataset_dir, "patches_final", "radiometric", track_id, "*")))
        
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

            if self.model.sun_reflections is not None:
                patch_name = os.path.splitext(os.path.basename(image_file))[0]
                stats["sun_reflection"] = (patch_name in self.model.sun_reflections[track_id])

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
