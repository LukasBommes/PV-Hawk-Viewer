import json
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot, Signal, QObject

from src.colormap import get_colors


class MapView(QObject):
    dataset_changed = Signal(bool)  # signals for notification of Javascript
    dataset_closed = Signal()
    annotation_data_changed = Signal()

    def __init__(self, model, controller, parent=None):
        super(MapView, self).__init__()
        self.model = model
        self.controller = controller
        self.parent = parent
        # connect signals and slots
        self.controller.source_deleted.connect(self.dataset_closed)
        self.model.dataset_closed.connect(self.dataset_closed)
        self.model.dataset_opened.connect(lambda: self.dataset_changed.emit(True))
        self.model.selected_column_changed.connect(lambda: self.dataset_changed.emit(False))

        self.model.map_model.min_val_changed.connect(lambda: self.dataset_changed.emit(False))
        self.model.map_model.max_val_changed.connect(lambda: self.dataset_changed.emit(False))
        self.model.map_model.colormap_changed.connect(lambda: self.dataset_changed.emit(False))

        self.model.annotation_editor_model.annotation_data_changed.connect(self.annotation_data_changed)

    @Slot(str)
    def printObj(self, obj):
        """Utility function for printing from javascript"""
        py_obj = json.loads(obj)
        print(py_obj)

    @Slot(result=str)
    def get_data(self):
        self.model.track_id = None
        data = []
        colors = {}
        if self.model.dataset_is_open:
            data = self.model.data
            data_column = self.controller.get_selected_column()
            if len(data_column) > 0:
                # colormaps = {
                #     0: "plasma",
                #     1: "Reds",
                #     2: "viridis"
                # }
                # colormap = colormaps[self.model.map_model.colormap]
                colors = get_colors(data_column, cmap="plasma", vmin=self.model.map_model.min_val, vmax=self.model.map_model.max_val)
            else:
                default_color = "#ff7800"
                colors = {track_id: default_color for track_id in self.model.track_ids}
        return json.dumps({
            "data": data,
            "colors": colors
        })

    @Slot(str)
    def update_images(self, track_id):
        self.model.track_id = json.loads(track_id)

    @Slot(result=str)
    def get_annotation_data(self):
        if not self.model.dataset_is_open:
            return json.dumps(None)

        annotation_data = self.model.annotation_editor_model.annotation_data
        if annotation_data is None:
            return json.dumps(None)

        return json.dumps(annotation_data)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, dpi=96):
        self.fig = Figure(dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.7)
        super(MplCanvas, self).__init__(self.fig)


class ColorbarView(QWidget):
    def __init__(self, model, controller):
        super().__init__()
        self.model = model
        self.controller = controller
        self.widget = MplCanvas()
        self.widget.setFixedHeight(50)
        self.widget.hide()

        # connect signals and slots
        self.model.map_model.min_val_changed.connect(self.update)
        self.model.map_model.max_val_changed.connect(self.update)
        self.model.map_model.colormap_changed.connect(self.update)
        self.model.selected_column_changed.connect(self.update)
        self.model.dataset_opened.connect(self.show)
        self.model.dataset_closed.connect(self.widget.hide)
        self.controller.source_deleted.connect(self.widget.hide)

    def show(self):
        if self.model.meta is None:
            return
        self.widget.show()

    def update(self):
        if self.model.meta is None:
            self.widget.hide()
            return
        
        self.widget.show()    

        cmap = matplotlib.cm.plasma
        norm = matplotlib.colors.Normalize(
            vmin=self.model.map_model.min_val, 
            vmax=self.model.map_model.max_val)

        cbar = self.widget.fig.colorbar(
            matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),
            cax=self.widget.axes,
            orientation='horizontal')

        label = ""
        if self.model.meta["type"] == "module_temperatures":
            label = "Temperatures / °C"
        
        cbar.set_label(label, labelpad=0, fontsize=10)
        cbar.ax.tick_params(labelsize=10, length=2, width=1)
        self.widget.draw()



class MapModel(QObject):
    min_val_changed = Signal(int)
    max_val_changed = Signal(int)
    colormap_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self._min_val = None
        self._max_val = None
        self._colormap = None
    
    @property
    def min_val(self):
        return self._min_val

    @min_val.setter
    def min_val(self, value):
        self._min_val = value
        self.min_val_changed.emit(value)

    @property
    def max_val(self):
        return self._max_val

    @max_val.setter
    def max_val(self, value):
        self._max_val = value
        self.max_val_changed.emit(value)

    @property
    def colormap(self):
        return self._colormap

    @colormap.setter
    def colormap(self, value):
        self._colormap = value
        self.colormap_changed.emit(value)