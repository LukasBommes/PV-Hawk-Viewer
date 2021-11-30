import json
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QComboBox
from PySide6.QtCore import Slot, Signal, QObject

from src.colormap import get_colors
from src.ui.ui_toolbar_data_range import Ui_DataRange
from src.ui.ui_toolbar_colormap_selection import Ui_ColormapSelection


class MapView(QObject):
    dataset_changed = Signal(bool)  # signals for notification of Javascript
    dataset_closed = Signal()
    annotation_data_changed = Signal()
    track_id_changed = Signal(str, str)

    def __init__(self, model, controller, parent=None):
        super(MapView, self).__init__()
        self.model = model
        self.controller = controller
        self.parent = parent
        # connect signals and slots
        self.controller.source_deleted.connect(self.dataset_closed)
        self.model.dataset_closed.connect(self.dataset_closed)
        self.model.dataset_opened.connect(lambda: self.dataset_changed.emit(True))
        self.model.selected_source_changed.connect(lambda: self.dataset_changed.emit(True))
        self.model.selected_column_changed.connect(lambda: self.dataset_changed.emit(False))
        self.model.map_model.colormap_changed.connect(lambda: self.dataset_changed.emit(False))

        # signal for explicitly redrawing themap
        self.controller.redraw_map.connect(lambda: self.dataset_changed.emit(False))

        # defect annotation editor
        self.model.annotation_editor_model.annotation_data_changed.connect(self.annotation_data_changed)
        self.model.track_id_changed.connect(self.track_id_changed)

        self.current_map_data = None

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
                colors = get_colors(
                    data_column, 
                    cmap=self.model.map_model.colormap, 
                    vmin=self.model.map_model.min_val, 
                    vmax=self.model.map_model.max_val
                )
            else:
                default_color = "#ff7800"
                colors = {track_id: default_color for track_id in self.model.track_ids}
        map_data = {
            "data": data,
            "colors": colors
        }
        if map_data != self.current_map_data:
            print("Data changed, redrawing")
            self.current_map_data = map_data
            return json.dumps(map_data)
        else:
            print("Data has not changed, not redrawing")
            return json.dumps(None)

    @Slot(str)
    def set_track_id(self, track_id):
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

        cmap = matplotlib.cm.get_cmap(self.model.map_model.colormap, 256)
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



class DataRangeView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.parent = parent
        self.ui = Ui_DataRange()
        self.ui.setupUi(self)
        self.disable()
        # connect signals and slots
        self.model.map_model.min_val_changed.connect(self.ui.minValSpinBox.setValue)
        self.model.map_model.max_val_changed.connect(self.ui.maxValSpinBox.setValue)
        self.ui.minValSpinBox.editingFinished.connect(self.set_min_val)
        self.ui.maxValSpinBox.editingFinished.connect(self.set_max_val)
        self.model.selected_source_changed.connect(self.enable)
        self.model.dataset_closed.connect(self.disable)

        # set default values
        self.model.map_model.min_val = -5
        self.model.map_model.max_val = 5

    @Slot()
    def set_min_val(self):
        value = self.ui.minValSpinBox.value()
        if value < self.model.map_model.max_val:
            self.model.map_model.min_val = value
            self.controller.redraw_map.emit()
        else:
            self.ui.minValSpinBox.setValue(self.model.map_model.min_val)

    @Slot()
    def set_max_val(self):
        value = self.ui.maxValSpinBox.value()
        if value > self.model.map_model.min_val:
            self.model.map_model.max_val = value
            self.controller.redraw_map.emit()
        else:
            self.ui.maxValSpinBox.setValue(self.model.map_model.max_val)

    def enable(self):
        if self.model.selected_source is None:
            self.disable()
        elif self.model.selected_source == "Module Layout":
            self.disable()
        else:
            self.ui.minValSpinBox.setEnabled(True)
            self.ui.maxValSpinBox.setEnabled(True)

    def disable(self):
        self.ui.minValSpinBox.setEnabled(False)
        self.ui.maxValSpinBox.setEnabled(False)



class ColormapSelectionView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.parent = parent
        self.ui = Ui_ColormapSelection()
        self.ui.setupUi(self)
        self.disable()        
        self.ui.colormapComboBox.addItems(self.model.map_model.colormaps)
        # connect signals and slots
        self.ui.colormapComboBox.currentIndexChanged.connect(lambda value: setattr(self.model.map_model, 'colormap', value))
        self.model.map_model.colormap_changed.connect(self.ui.colormapComboBox.setCurrentIndex)
        self.model.selected_source_changed.connect(self.enable)
        self.model.dataset_closed.connect(self.disable)
        # set default values
        self.model.map_model.colormap = 0

    def enable(self):
        if self.model.selected_source is None:
            self.disable()
        elif self.model.selected_source == "Module Layout":
            self.disable()
        else:
            self.ui.colormapComboBox.setEnabled(True)

    def disable(self):
        self.ui.colormapComboBox.setEnabled(False)



class DataColumnSelectionView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.parent = parent
        self.build_ui()
        
        # connect signals and slots
        self.model.dataset_opened.connect(lambda: self.comboBox.setEnabled(True))
        self.model.dataset_opened.connect(self.update_options)
        self.model.dataset_closed.connect(lambda: self.comboBox.setEnabled(False))
        self.model.dataset_closed.connect(self.update_options)
        self.model.selected_source_changed.connect(self.update_options)
        self.comboBox.currentIndexChanged.connect(self.controller.set_selected_column)
        self.model.selected_column_changed.connect(self.comboBox.setCurrentIndex)

        self.update_options()

    def build_ui(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setText("Data Column")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setFixedWidth(150)
        self.comboBox.setEnabled(False)
        self.horizontalLayout.addWidget(self.comboBox)

    @Slot()
    def update_options(self):
        self.comboBox.clear()
        if self.model.selected_source is None:
            self.comboBox.setEnabled(False)
        elif self.model.selected_source == "Module Layout":
            self.comboBox.setEnabled(False)
        else:
            self.comboBox.setEnabled(True)
            data_columns = self.controller.get_column_names()
            self.comboBox.addItems(data_columns)  # probably causes currentIndexChanged to be fired



class MapModel(QObject):
    min_val_changed = Signal(int)
    max_val_changed = Signal(int)
    colormap_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self._min_val = None
        self._max_val = None
        self._colormap = None
        self._colormaps = sorted(plt.colormaps(), key=lambda x: str.lower(x))
    
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
        #cmap = list(self._colormaps.values())[value]
        cmap = self._colormaps[value]
        self._colormap = cmap
        self.colormap_changed.emit(value)

    @property
    def colormaps(self):
        return self._colormaps