import json
import copy

from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Slot, Signal, QObject

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
        self.map_backend = MapBackend(model, controller)
        parent.channel.registerObject("string_editor_map_backend", self.map_backend)

        self.disable()

        # connect signals and slots
        # TODO: handle opening and closing of dataset, e.g. set defautl values, reset string annotation data
        self.ui.pushButtonNewString.clicked.connect(self.new_string)
        self.ui.pushButtonCancelString.clicked.connect(self.cancel_string)
        self.ui.pushButtonConfirmString.clicked.connect(self.confirm_string)
        self.controller.string_editor_controller.show_validation_error.connect(self.show_validation_error)
        self.controller.string_editor_controller.confirm_string.connect(self.disable)
        self.controller.string_editor_controller.confirm_string.connect(self.controller.string_editor_controller.reset_temp_string_data)

        self.ui.pushButtonStartDrawing.clicked.connect(self.start_drawing)
        self.ui.pushButtonEndDrawing.clicked.connect(self.end_drawing)
        self.ui.checkBoxReverseDirection.stateChanged.connect(lambda value: setattr(self.model.string_editor_model, 'reverse_direction', value))
        self.model.string_editor_model.reverse_direction_changed.connect(self.ui.checkBoxReverseDirection.setChecked)
        self.ui.lineEditTrackerID.textChanged.connect(lambda value: setattr(self.model.string_editor_model, 'tracker_id', value))
        self.model.string_editor_model.tracker_id_changed.connect(self.ui.lineEditTrackerID.setText)
        self.ui.lineEditArrayID.textChanged.connect(lambda value: setattr(self.model.string_editor_model, 'array_id', value))
        self.model.string_editor_model.array_id_changed.connect(self.ui.lineEditArrayID.setText)
        self.ui.lineEditInverterID.textChanged.connect(lambda value: setattr(self.model.string_editor_model, 'inverter_id', value))
        self.model.string_editor_model.inverter_id_changed.connect(self.ui.lineEditInverterID.setText)
        self.ui.lineEditStringID.textChanged.connect(lambda value: setattr(self.model.string_editor_model, 'string_id', value))
        self.model.string_editor_model.string_id_changed.connect(self.ui.lineEditStringID.setText)

        # set default values
        # TODO: remove this and connect to dataset open/close handlers
        self.controller.string_editor_controller.set_default_values()

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
        self.ui.pushButtonStartDrawing.setEnabled(True)
        self.ui.pushButtonEndDrawing.setEnabled(False)
        self.ui.pushButtonCancelString.setEnabled(True)
        self.ui.pushButtonConfirmString.setEnabled(True)
        self.ui.lineEditTrackerID.setEnabled(True)
        self.ui.lineEditArrayID.setEnabled(True)
        self.ui.lineEditInverterID.setEnabled(True)
        self.ui.lineEditStringID.setEnabled(True)
        self.ui.checkBoxReverseDirection.setEnabled(True)

    def start_drawing(self):
        self.model.string_editor_model.drawing_string = True
        self.ui.pushButtonStartDrawing.setEnabled(False)
        self.ui.pushButtonEndDrawing.setEnabled(True)

    def end_drawing(self):
        self.model.string_editor_model.drawing_string = False
        self.ui.pushButtonStartDrawing.setEnabled(True)
        self.ui.pushButtonEndDrawing.setEnabled(False)

    def new_string(self):
        self.controller.string_editor_controller.reset_temp_string_data()
        self.controller.string_editor_controller.new_string.emit()
        self.enable()
    
    def cancel_string(self):
        self.controller.string_editor_controller.reset_temp_string_data()
        self.controller.string_editor_controller.cancel_string.emit()
        self.disable()

    def confirm_string(self):
        self.controller.string_editor_controller.update_string_annotation_data()

    @Slot(str)
    def show_validation_error(self, text):
        print("validation error")
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.exec()



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

        # connect signals and slots
        self.model.string_editor_model.drawing_string_changed.connect(self.drawing_string_changed)
        self.controller.string_editor_controller.new_string.connect(self.new_string)
        self.controller.string_editor_controller.cancel_string.connect(self.cancel_string)
        self.controller.string_editor_controller.confirm_string.connect(self.confirm_string)
        self.model.string_editor_model.string_annotation_data_changed.connect(self.string_annotation_data_changed)

    @Slot(result=str)
    def get_string_annotation_data(self):
        """Retrieve string annotation data from model."""
        if not self.model.dataset_is_open:
            return json.dumps(None)

        string_annotation_data = self.model.string_editor_model.string_annotation_data
        if string_annotation_data is None:
            return json.dumps(None)

        return json.dumps(string_annotation_data)

    @Slot(str)
    def update_string_annotation_data(self, current_string_data):
        """Insert current string annotation into string annotation data."""
        #print("current_string_data", json.loads(current_string_data))
        current_string_data = json.loads(current_string_data)
        modules = current_string_data["modules"]
        polyline = current_string_data["polyline"]
        string_id = "{}_{}_{}_{}".format(
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



class StringEditorController(QObject):
    new_string = Signal()
    confirm_string = Signal()
    cancel_string = Signal()
    show_validation_error = Signal(str)

    def __init__(self, model):
        super().__init__()
        self.model = model

    def set_default_values(self):
        self.model.string_editor_model.tracker_id = "00"
        self.model.string_editor_model.array_id = "00"
        self.model.string_editor_model.inverter_id = "00"
        self.model.string_editor_model.string_id = "00"

    @Slot()
    def reset_temp_string_data(self):
        self.model.string_editor_model.reverse_direction = False
        self.model.string_editor_model.drawing_string = False

    def is_valid(self, value):
        return isinstance(value, str) and value.isalnum() and (len(value) == 2 or len(value) == 3)

    def validate_string_id(self):
        # check if individual IDs are valid
        def error_msg(text):
            return "{} is invalid. Provide a 2-digit or 3-digit alphanumeric value.".format(text)

        if not self.is_valid(self.model.string_editor_model.tracker_id):
            self.show_validation_error.emit(error_msg("Tracker ID"))
            return False
        if not self.is_valid(self.model.string_editor_model.array_id):
            self.show_validation_error.emit(error_msg("Array ID"))
            return False
        if not self.is_valid(self.model.string_editor_model.inverter_id):
            self.show_validation_error.emit(error_msg("Inverter ID"))
            return False
        if not self.is_valid(self.model.string_editor_model.string_id):
            self.show_validation_error.emit(error_msg("String ID"))
            return False

        # check if a string with this id exists already
        string_id = "{}_{}_{}_{}".format(
            self.model.string_editor_model.tracker_id,
            self.model.string_editor_model.array_id,
            self.model.string_editor_model.inverter_id,
            self.model.string_editor_model.string_id,
        )
        if ((self.model.string_editor_model.string_annotation_data is not None) and
             string_id in self.model.string_editor_model.string_annotation_data["string_data"]):
            self.show_validation_error.emit("A string with this ID exists already.")
            return False

        return True

    def update_string_annotation_data(self):
        ret = self.validate_string_id()
        if ret:
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
        
       
        