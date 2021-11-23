import json
import copy

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot, Signal, QObject
from PySide6.QtWebChannel import QWebChannel

from src.ui.ui_string_editor import Ui_StringEditor


class StringEditorView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.ui = Ui_StringEditor()
        self.ui.setupUi(self)
        self.parent = parent

        # register map backend
        self.map_backend = MapBackend(model, controller, parent=self)
        parent.channel.registerObject("string_editor_map_backend", self.map_backend)

        self.disable()

        # connect signals and slots
        self.ui.pushButtonNewString.clicked.connect(self.new_string)
        self.ui.pushButtonCancelString.clicked.connect(self.cancel_string)
        self.ui.pushButtonConfirmString.clicked.connect(self.confirm_string)
        self.ui.pushButtonStartDrawing.clicked.connect(lambda: setattr(self.model.string_editor_model, 'drawing_string', True))
        self.ui.pushButtonEndDrawing.clicked.connect(lambda: setattr(self.model.string_editor_model, 'drawing_string', False))
        self.model.string_editor_model.drawing_string_changed.connect(
            lambda value: self.ui.pushButtonStartDrawing.setEnabled(not self.model.string_editor_model.drawing_string))
        self.model.string_editor_model.drawing_string_changed.connect(
            lambda value: self.ui.pushButtonEndDrawing.setEnabled(self.model.string_editor_model.drawing_string))

        self.ui.checkBoxReverseDirection.stateChanged.connect(lambda value: setattr(self.model.string_editor_model, 'reverse_direction', value))
        self.model.string_editor_model.reverse_direction_changed.connect(self.ui.checkBoxReverseDirection.setChecked)
        self.ui.lineEditTrackerID.textChanged.connect(self.controller.string_editor_controller.set_tracker_id)
        self.model.string_editor_model.tracker_id_changed.connect(self.ui.lineEditTrackerID.setText)
        self.ui.lineEditArrayID.textChanged.connect(self.controller.string_editor_controller.set_array_id)
        self.model.string_editor_model.array_id_changed.connect(self.ui.lineEditArrayID.setText)
        self.ui.lineEditInverterID.textChanged.connect(self.controller.string_editor_controller.set_inverter_id)
        self.model.string_editor_model.inverter_id_changed.connect(self.ui.lineEditInverterID.setText)
        self.ui.lineEditStringID.textChanged.connect(self.controller.string_editor_controller.set_string_id)
        self.model.string_editor_model.string_id_changed.connect(self.ui.lineEditStringID.setText)


    def disable(self):
        self.ui.pushButtonStartDrawing.setEnabled(False)
        self.ui.pushButtonEndDrawing.setEnabled(False)
        self.ui.pushButtonCancelString.setEnabled(False)
        self.ui.pushButtonConfirmString.setEnabled(False)
        self.ui.lineEditTrackerID.setEnabled(False)
        self.ui.lineEditArrayID.setEnabled(False)
        self.ui.lineEditInverterID.setEnabled(False)
        self.ui.lineEditStringID.setEnabled(False)
        self.ui.checkBoxReverseDirection.setEnabled(False)

    def enable(self):
        self.ui.pushButtonStartDrawing.setEnabled(not self.model.string_editor_model.drawing_string)
        self.ui.pushButtonEndDrawing.setEnabled(self.model.string_editor_model.drawing_string)
        self.ui.pushButtonCancelString.setEnabled(True)
        self.ui.pushButtonConfirmString.setEnabled(True)
        self.ui.lineEditTrackerID.setEnabled(True)
        self.ui.lineEditArrayID.setEnabled(True)
        self.ui.lineEditInverterID.setEnabled(True)
        self.ui.lineEditStringID.setEnabled(True)
        self.ui.checkBoxReverseDirection.setEnabled(True)

    def new_string(self):
        self.controller.string_editor_controller.reset_temp_string_data()
        self.controller.string_editor_controller.new_string.emit()
        self.enable()
    
    def cancel_string(self):
        self.controller.string_editor_controller.reset_temp_string_data()
        self.controller.string_editor_controller.cancel_string.emit()
        self.disable()

    def confirm_string(self):
        # TODO: 
        # - validate all inputs are available and correct (self.controller.string_editor_controller.validate_temp_string_data)
        # - update the string annotation data by instering the module IDs of the current string in the data structure
        self.controller.string_editor_controller.update_string_annotation_data()
        self.disable()



class MapBackend(QObject):
    drawing_string_changed = Signal(bool)
    new_string = Signal()
    cancel_string = Signal()
    confirm_string = Signal()
    string_annotation_data_changed = Signal()

    def __init__(self, model, controller, parent=None):
        super(MapBackend, self).__init__()
        self.model = model
        self.controller = controller
        self.parent = parent

        self.model.string_editor_model.drawing_string_changed.connect(self.drawing_string_changed)
        self.controller.string_editor_controller.new_string.connect(self.new_string)
        self.controller.string_editor_controller.cancel_string.connect(self.cancel_string)
        self.controller.string_editor_controller.confirm_string.connect(self.confirm_string)

        self.model.string_editor_model.string_annotation_data_changed.connect(self.string_annotation_data_changed)

    @Slot(str)
    def update_string_annotation_data(self, current_string_data):
        """Insert current string annotation into string annotation data."""
        #print("current_string_data", json.loads(current_string_data))
        current_string_data = json.loads(current_string_data)
        modules = current_string_data["modules"]
        polyline = current_string_data["polyline"]
        string_id = "{}_{}_{}".format(
            self.model.string_editor_model.tracker_id,
            self.model.string_editor_model.array_id,
            self.model.string_editor_model.inverter_id,
            self.model.string_editor_model.string_id,
        )

        data = copy.deepcopy(self.model.string_editor_model.string_annotation_data)
        if data is None:
            data = {
                "string_data": {},
                "plant_id_track_id_mapping": []
            }

        # insert data of current string (e.g. polyline, contained modules)
        data["string_data"][string_id] = {
            "track_ids": [module["track_id"] for module in modules],
            "polyline": polyline
        }

        # update plant_id / track_id mapping
        for module_id, module in enumerate(modules):
            plant_id = "{}_{:02d}".format(string_id, module_id)
            data["plant_id_track_id_mapping"].append((plant_id, module["track_id"]))

        self.model.string_editor_model.string_annotation_data = data
        self.controller.string_editor_controller.reset_temp_string_data()



class StringEditorController(QObject):
    new_string = Signal()
    confirm_string = Signal()
    cancel_string = Signal()

    def __init__(self, model):
        super().__init__()
        self.model = model

    def reset_temp_string_data(self):
        self.model.string_editor_model.tracker_id = ""
        self.model.string_editor_model.array_id = ""
        self.model.string_editor_model.inverter_id = ""
        self.model.string_editor_model.string_id = ""
        self.model.string_editor_model.reverse_direction = False
        self.model.string_editor_model.drawing_string = False

    # TODO: validate correct format of IDs (only update state if valid, otherwise show error message)
    def set_tracker_id(self, value):
        self.model.string_editor_model.tracker_id = value

    def set_array_id(self, value):
        self.model.string_editor_model.array_id = value

    def set_inverter_id(self, value):
        self.model.string_editor_model.inverter_id = value

    def set_string_id(self, value):
        self.model.string_editor_model.string_id = value

    def update_string_annotation_data(self):
        self.confirm_string.emit()



class StringEditorModel(QObject):
    tracker_id_changed = Signal(str)
    array_id_changed = Signal(str)
    inverter_id_changed = Signal(str)
    string_id_changed = Signal(str)
    reverse_direction_changed = Signal(bool)
    drawing_string_changed = Signal(bool)
    string_annotation_data_changed = Signal()

    def __init__(self):
        super().__init__()
        self._tracker_id = ""
        self._array_id = ""
        self._inverter_id = ""
        self._string_id = ""
        self._reverse_direction = False
        self._drawing_string = False
        # string data of entire plant
        self._string_annotation_data = None

    @property
    def tracker_id(self):
        return self._tracker_id

    @tracker_id.setter
    def tracker_id(self, value):
        self._tracker_id = value
        self.tracker_id_changed.emit(value)

    @property
    def array_id(self):
        return self._array_id

    @array_id.setter
    def array_id(self, value):
        self._array_id = value
        self.array_id_changed.emit(value)

    @property
    def inverter_id(self):
        return self._inverter_id

    @inverter_id.setter
    def inverter_id(self, value):
        self._inverter_id = value
        self.inverter_id_changed.emit(value)

    @property
    def string_id(self):
        return self._string_id

    @string_id.setter
    def string_id(self, value):
        self._string_id = value
        self.string_id_changed.emit(value)

    @property
    def reverse_direction(self):
        return self._reverse_direction

    @reverse_direction.setter
    def reverse_direction(self, value):
        if value == 0:
            self._reverse_direction = False
            self.reverse_direction_changed.emit(False)
        else:
            self._reverse_direction = True
            self.reverse_direction_changed.emit(True)

    @property
    def drawing_string(self):
        return self._drawing_string

    @drawing_string.setter
    def drawing_string(self, value):
        self._drawing_string = value
        self.drawing_string_changed.emit(value)

    @property
    def string_annotation_data(self):
        return self._string_annotation_data

    @string_annotation_data.setter
    def string_annotation_data(self, value):
        self._string_annotation_data = value
        print(self._string_annotation_data)
        self.string_annotation_data_changed.emit()
        
       
        