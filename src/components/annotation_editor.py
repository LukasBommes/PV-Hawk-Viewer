import os
import json

from PySide6.QtWidgets import QWidget, QCheckBox, QSpacerItem, QSizePolicy
from PySide6.QtCore import Slot, Signal, QObject

from src.ui.ui_annotation_editor import Ui_AnnotationEditor


class AnnotationEditorView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.ui = Ui_AnnotationEditor()
        self.ui.setupUi(self)
        self.loadDefectsScheme()
        # connect signals and slots
        self.model.dataset_opened.connect(self.controller.annotation_editor_controller.set_annotation_data)
        self.model.dataset_closed.connect(self.controller.annotation_editor_controller.reset_annotation_data)

        self.model.track_id_changed.connect(self.update_checkbox_states)
        self.model.annotation_editor_model.annotation_data_changed.connect(self.update_checkbox_states)


    def loadDefectsScheme(self):
        try:
            defects_scheme = json.load(open(os.path.join("src", "resources", "defect_schema.json"), "r"))
        except FileNotFoundError:
            pass
        else:
            self.ui.checkboxes = []
            for defect in defects_scheme:
                checkbox = QCheckBox("{} - {}".format(defect["name"], defect["description"]))
                checkbox.setObjectName(u"defect_checkbox_{}".format(defect["name"]))
                checkbox.setToolTip(", ".join(defect["examples"]))
                checkbox.stateChanged.connect(self.controller.annotation_editor_controller.update_annotation_data)
                self.ui.scrollAreaWidgetContents.layout().addWidget(checkbox)
                self.ui.checkboxes.append(checkbox)
            self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.ui.scrollAreaWidgetContents.layout().addItem(self.verticalSpacer)

    @Slot()
    def update_checkbox_states(self):
        """Update checkboxes based on annotation state"""
        # TODO: reset all boxes when dataset is closed, etc.
        track_id = self.model.track_id
        if not self.model.dataset_is_open:
            return
        if self.model.annotation_editor_model.annotation_data is None:
            return
        if track_id is None:
            return

        print("Updating checkboxes based on state ", self.ui.checkboxes)
        defects = self.model.annotation_editor_model.annotation_data[track_id]
        for checkbox in self.ui.checkboxes:
            checkbox_name = checkbox.objectName()
            defect = checkbox_name[16:]
            if defect in defects:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)



class AnnotationEditorController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    @Slot()
    def set_annotation_data(self):
        self.model.annotation_editor_model.annotation_data = {track_id: [] for track_id in self.model.track_ids}

    @Slot()
    def reset_annotation_data(self):
        self.model.annotation_editor_model.annotation_data = None

    @Slot()
    def update_annotation_data(self, value):
        track_id = self.model.track_id
        print("Updating annotation data ", self.model.dataset_is_open, self.model.track_id, (self.model.annotation_editor_model.annotation_data is None))
        if not self.model.dataset_is_open:
            return
        if self.model.annotation_editor_model.annotation_data is None:
            return
        if track_id is None:
            return

        checkbox = self.sender()
        checkbox_name = checkbox.objectName()
        checked = value != 0
        defect = checkbox_name[16:]
        print(checked)

        # update model
        if checked:
            print("checked: ", checkbox_name)
            if defect not in self.model.annotation_editor_model.annotation_data[track_id]:
                self.model.annotation_editor_model.annotation_data[track_id].append(defect)
                self.model.annotation_editor_model.annotation_data_changed.emit()  # won't be fired automatically inside model because we only change an internal value

        elif not checked:
            print("unchecked: ", checkbox_name)
            if defect in self.model.annotation_editor_model.annotation_data[track_id]:
                self.model.annotation_editor_model.annotation_data[track_id].remove(defect)
                self.model.annotation_editor_model.annotation_data_changed.emit()

        self.print_annotation_data()

    @Slot()
    def save_annotation_file(self):
        # TODO:
        # - dialog: ask if changes should be changed?
        # - save annotation data to disk (different format)
        pass

    @Slot()
    def load_annotation_file(self):
        # TODO:
        # - open file dialog to select annotation file
        # - load from file and update annotation data model (should update checkboxes)
        pass

    # for debugging
    def print_annotation_data(self):
        for track_id, defects in self.model.annotation_editor_model.annotation_data.items():
            if len(defects) > 0:
                print(track_id, defects)



class AnnotationEditorModel(QObject):
    annotation_data_changed = Signal()

    def __init__(self):
        super().__init__()
        self._annotation_data = None
    
    @property
    def annotation_data(self):
        return self._annotation_data

    @annotation_data.setter
    def annotation_data(self, value):
        self._annotation_data = value
        self.annotation_data_changed.emit()