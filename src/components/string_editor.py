import os
import json
import copy

from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog
from PySide6.QtCore import Slot, Signal, QObject
from PySide6.QtGui import QIcon

from src.ui.ui_string_editor import Ui_StringEditor


class StringEditorView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.ui = Ui_StringEditor()
        self.ui.setupUi(self)
        self.parent = parent
        # setup icons
        self.ui.pushButtonNewString.setIcon(QIcon.fromTheme("list-add"))
        self.ui.pushButtonDeleteString.setIcon(QIcon.fromTheme("list-remove"))
        self.disable()

        # connect signals and slots
        self.ui.pushButtonNewString.clicked.connect(self.new_string)
        self.ui.pushButtonCancelString.clicked.connect(self.cancel_string)
        self.ui.pushButtonConfirmString.clicked.connect(self.confirm_string)
        self.ui.pushButtonStartDrawing.clicked.connect(self.start_drawing)
        self.ui.pushButtonPauseDrawing.clicked.connect(self.pause_drawing)
        self.ui.pushButtonEndDrawing.clicked.connect(self.end_drawing)
        self.ui.pushButtonDeleteString.clicked.connect(self.controller.string_editor_controller.delete_string)
        self.ui.lineEditTrackerID.textChanged.connect(lambda value: setattr(self.model.string_editor_model, 'tracker_id', value))
        self.model.string_editor_model.tracker_id_changed.connect(self.ui.lineEditTrackerID.setText)
        self.ui.lineEditArrayID.textChanged.connect(lambda value: setattr(self.model.string_editor_model, 'array_id', value))
        self.model.string_editor_model.array_id_changed.connect(self.ui.lineEditArrayID.setText)
        self.ui.lineEditInverterID.textChanged.connect(lambda value: setattr(self.model.string_editor_model, 'inverter_id', value))
        self.model.string_editor_model.inverter_id_changed.connect(self.ui.lineEditInverterID.setText)
        self.ui.lineEditStringID.textChanged.connect(lambda value: setattr(self.model.string_editor_model, 'string_id', value))
        self.model.string_editor_model.string_id_changed.connect(self.ui.lineEditStringID.setText)
        self.model.string_editor_model.drawing_paused_changed.connect(self.drawing_paused_changed)
        self.controller.string_editor_controller.show_validation_error.connect(self.show_validation_error)
        self.controller.string_editor_controller.confirm_string.connect(self.disable)
        self.controller.export_string_annotation.connect(self.controller.string_editor_controller.export_string_annotation)
        self.model.string_editor_model.selected_string_id_changed.connect(self.selected_string_id_changed)
        self.model.string_editor_model.temporary_string_data_changed.connect(self.temporary_string_data_changed)
        self.model.dataset_opened.connect(self.controller.string_editor_controller.set_default_values)
        self.model.dataset_opened.connect(lambda: self.ui.pushButtonNewString.setEnabled(True))
        self.model.dataset_closed.connect(self.close_string_annotation)
        self.controller.close_string_annotation.connect(self.close_string_annotation)

    def disable(self):
        self.ui.pushButtonStartDrawing.setEnabled(False)
        self.ui.pushButtonPauseDrawing.setEnabled(False)
        self.ui.pushButtonEndDrawing.setEnabled(False)
        self.ui.pushButtonCancelString.setEnabled(False)
        self.ui.pushButtonConfirmString.setEnabled(False)
        self.ui.pushButtonDeleteString.setEnabled(False)
        self.ui.lineEditTrackerID.setEnabled(False)
        self.ui.lineEditArrayID.setEnabled(False)
        self.ui.lineEditInverterID.setEnabled(False)
        self.ui.lineEditStringID.setEnabled(False)

    def start_drawing(self):
        self.controller.string_editor_controller.drawing_started.emit()
        self.ui.pushButtonStartDrawing.setEnabled(False)
        self.ui.pushButtonPauseDrawing.setEnabled(True)
        self.ui.pushButtonEndDrawing.setEnabled(True)

    def pause_drawing(self):
        self.model.string_editor_model.drawing_paused = not self.model.string_editor_model.drawing_paused

    def end_drawing(self):
        self.controller.string_editor_controller.drawing_ended.emit()

    def new_string(self):
        self.ui.pushButtonNewString.setEnabled(False)
        self.controller.string_editor_controller.reset_temp_string_data()
        self.controller.string_editor_controller.new_string.emit()
        self.ui.pushButtonStartDrawing.setEnabled(True)
        self.ui.pushButtonPauseDrawing.setEnabled(False)
        self.ui.pushButtonEndDrawing.setEnabled(False)
        self.ui.pushButtonCancelString.setEnabled(True)
    
    def cancel_string(self):
        self.controller.string_editor_controller.reset_temp_string_data()
        self.controller.string_editor_controller.cancel_string.emit()
        self.ui.pushButtonNewString.setEnabled(True)
        self.disable()

    def confirm_string(self):
        self.controller.string_editor_controller.update_string_annotation_data()

    @Slot()
    def temporary_string_data_changed(self):
        temporary_string_data = self.model.string_editor_model.temporary_string_data
        if temporary_string_data is None:
            self.disable()
            self.ui.pushButtonNewString.setEnabled(True)
            return
        if len(temporary_string_data["modules"]) == 0:
            self.disable()
            self.ui.pushButtonNewString.setEnabled(True)
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("No modules selected. Please click on the map to select modules after clicking \"Start Drawing\".")
            msg.setIcon(QMessageBox.Critical)
            msg.exec()
            return
        self.ui.pushButtonStartDrawing.setEnabled(False)
        self.ui.pushButtonPauseDrawing.setEnabled(False)
        self.ui.pushButtonEndDrawing.setEnabled(False)
        self.ui.pushButtonConfirmString.setEnabled(True)
        self.ui.lineEditTrackerID.setEnabled(True)
        self.ui.lineEditArrayID.setEnabled(True)
        self.ui.lineEditInverterID.setEnabled(True)
        self.ui.lineEditStringID.setEnabled(True)

    @Slot()
    def selected_string_id_changed(self):
        if self.model.string_editor_model.selected_string_id is not None:
            self.ui.pushButtonDeleteString.setEnabled(True)
        else:
            self.ui.pushButtonDeleteString.setEnabled(False)

    @Slot()
    def drawing_paused_changed(self):
        if self.model.string_editor_model.drawing_paused:
            self.ui.pushButtonPauseDrawing.setText("Continue")
        else:
            self.ui.pushButtonPauseDrawing.setText("Pause")

    @Slot(str)
    def show_validation_error(self, text):
        print("validation error")
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.exec()

    @Slot()
    def close_string_annotation(self):
        self.controller.string_editor_controller.reset_temp_string_data()
        self.controller.string_editor_controller.reset_string_annotation_data
        self.disable()



class StringEditorController(QObject):
    new_string = Signal()
    confirm_string = Signal()
    cancel_string = Signal()
    show_validation_error = Signal(str)
    selected_string_id_changed = Signal(str, str)
    drawing_started = Signal()
    drawing_paused_changed = Signal(bool)
    drawing_ended = Signal()
    string_annotation_data_changed = Signal()

    def __init__(self, model):
        super().__init__()
        self.model = model
        # connect signals and slots
        self.model.dataset_opened.connect(self.load_annotation_file)
        self.model.string_editor_model.selected_string_id_changed.connect(self.selected_string_id_changed)
        self.model.string_editor_model.string_annotation_data_changed.connect(self.string_annotation_data_changed)
        self.model.string_editor_model.drawing_paused_changed.connect(self.drawing_paused_changed)

    def set_default_values(self):
        self.model.string_editor_model.tracker_id = "00"
        self.model.string_editor_model.array_id = "00"
        self.model.string_editor_model.inverter_id = "00"
        self.model.string_editor_model.string_id = "00"

    @Slot()
    def reset_temp_string_data(self):
        self.cancel_string.emit()
        self.model.string_editor_model.selected_string_id = None
        self.model.string_editor_model.temporary_string_data = None
        self.model.string_editor_model.drawing_paused = False

    @Slot()
    def reset_string_annotation_data(self):
        self.model.string_editor_model.string_annotation_data = None

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

    def delete_string(self):
        selected_string_id = self.model.string_editor_model.selected_string_id
        if selected_string_id is None:
            return
        data = copy.deepcopy(self.model.string_editor_model.string_annotation_data)
        print(data)
        try:
            del data["string_data"][selected_string_id]
            
            for i in range(len(data["plant_id_track_id_mapping"])-1, -1, -1):  # iterate backwards
                plant_id, track_id = data["plant_id_track_id_mapping"][i]
                string_id = "_".join(str.split(plant_id, "_")[:-1])
                print(string_id, selected_string_id)
                if string_id == selected_string_id:
                    del data["plant_id_track_id_mapping"][i]

            print("Deleted string annotation data for string {}".format(selected_string_id))
        except KeyError:
            print("Failed to delete string annotation data for string {}".format(selected_string_id))
        else:
            self.model.string_editor_model.string_annotation_data = data
            self.save_annotation_file()
        self.model.string_editor_model.selected_string_id = None

    def save_annotation_file(self):
        print("Saving string annotation to file")
        if not self.model.dataset_is_open:
            return
        data = self.model.string_editor_model.string_annotation_data
        if data is None:
            return
        save_dir = os.path.join(self.model.dataset_dir, "annotations")
        os.makedirs(save_dir, exist_ok=True)
        json.dump(data, open(os.path.join(save_dir, "string_anotation.json"), "w"))

    @Slot()
    def load_annotation_file(self):
        print("Loading string annotation from file")
        if not self.model.dataset_is_open:
            return
        save_dir = os.path.join(self.model.dataset_dir, "annotations")
        try:
            data = json.load(open(os.path.join(save_dir, "string_anotation.json"), "r"))
        except FileNotFoundError:
            pass
        else:
            self.model.string_editor_model.string_annotation_data = data

    @Slot()
    def export_string_annotation(self):
        """Export current string annotation data to a user selected file."""
        file_name, _ = QFileDialog.getSaveFileName(
            None, "Export String Annotation", "", "", "JSON Files (*.json)")
        if file_name == "":
            return
        
        # make sure filename has JSON extension
        file_name = ".".join([os.path.splitext(file_name)[0], "json"])

        data = self.model.string_editor_model.string_annotation_data
        if data is None:
            return
        
        print("Exporting string annotation to ", file_name)
        json.dump(data, open(file_name, "w"))

    @Slot(str)
    def set_selected_string_id(self, selected_string_id):
        self.model.string_editor_model.selected_string_id = json.loads(selected_string_id)

    @Slot(result=str)
    def get_string_annotation_data(self):
        """Retrieve string annotation data from model and send to JS backend."""
        if not self.model.dataset_is_open:
            return json.dumps(None)

        string_annotation_data = self.model.string_editor_model.string_annotation_data
        if string_annotation_data is None:
            return json.dumps(None)

        return json.dumps(string_annotation_data)

    @Slot(str)
    def set_temporary_string_annotation_data(self, temporary_string_data):
        """Insert current string annotation into string annotation data."""
        temporary_string_data = json.loads(temporary_string_data)
        self.model.string_editor_model.temporary_string_data = temporary_string_data

    def update_string_annotation_data(self):
        ret = self.validate_string_id()
        if ret:
            temporary_string_data = self.model.string_editor_model.temporary_string_data
            modules = temporary_string_data["modules"]
            points = temporary_string_data["points"]
            paused = temporary_string_data["paused"]
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

            # insert data of current string (e.g. points, contained modules)
            data["string_data"][string_id] = {
                "track_ids": [module["track_id"] for module in modules],
                "points": points,
                "paused": paused
            }

            # update plant_id / track_id mapping
            for module_id, module in enumerate(modules):
                plant_id = "{}_{:02d}".format(string_id, module_id)
                data["plant_id_track_id_mapping"].append((plant_id, module["track_id"]))

            self.model.string_editor_model.string_annotation_data = data
            self.model.string_editor_model.temporary_string_data = None
            self.reset_temp_string_data()
            self.save_annotation_file()
            self.confirm_string.emit()



class StringEditorModel(QObject):
    tracker_id_changed = Signal(str)
    array_id_changed = Signal(str)
    inverter_id_changed = Signal(str)
    string_id_changed = Signal(str)
    selected_string_id_changed = Signal(str, str)
    drawing_paused_changed = Signal(bool)
    temporary_string_data_changed = Signal()
    string_annotation_data_changed = Signal()

    def __init__(self):
        super().__init__()
        self._tracker_id = ""
        self._array_id = ""
        self._inverter_id = ""
        self._string_id = ""
        self._selected_string_id = None
        self._drawing_paused = False
        self._temporary_string_data = None
        self._string_annotation_data = None  # string data of entire plant

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
    def selected_string_id(self):
        return self._selected_string_id

    @selected_string_id.setter
    def selected_string_id(self, value):
        selected_string_id_prev = self._selected_string_id
        self._selected_string_id = value
        self.selected_string_id_changed.emit(selected_string_id_prev, value)

    @property
    def drawing_paused(self):
        return self._drawing_paused

    @drawing_paused.setter
    def drawing_paused(self, value):
        self._drawing_paused = value
        self.drawing_paused_changed.emit(value)

    @property
    def string_annotation_data(self):
        return self._string_annotation_data

    @string_annotation_data.setter
    def string_annotation_data(self, value):
        self._string_annotation_data = value
        self.string_annotation_data_changed.emit()

    @property
    def temporary_string_data(self):
        return self._temporary_string_data

    @temporary_string_data.setter
    def temporary_string_data(self, value):
        self._temporary_string_data = value
        self.temporary_string_data_changed.emit()
        
       
        