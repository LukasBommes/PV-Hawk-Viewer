import os
import json

from PySide6.QtWidgets import QWidget, QCheckBox, QSpacerItem, QSizePolicy, \
    QMessageBox, QFileDialog
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
        self.model.track_id_changed.connect(self.enable_disable)
        self.model.track_id_changed.connect(self.update_checkbox_states)
        self.model.annotation_editor_model.annotation_data_changed.connect(self.update_checkbox_states)

        # if anything wants to close the window, ask user if he wants to save unsaved changes
        self.controller.save_defect_annotation.connect(self.controller.annotation_editor_controller.save_annotation_file)


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
                checkbox.setEnabled(False)
                self.ui.scrollAreaWidgetContents.layout().addWidget(checkbox)
                self.ui.checkboxes.append(checkbox)
            self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.ui.scrollAreaWidgetContents.layout().addItem(self.verticalSpacer)

    @Slot()
    def enable_disable(self):
        if self.model.track_id is None:
            for checkbox in self.ui.checkboxes:
                checkbox.setEnabled(False)
            return
        for checkbox in self.ui.checkboxes:
                checkbox.setEnabled(True)

    @Slot()
    def update_checkbox_states(self):
        """Update checkboxes based on annotation state"""
        # clear checkboxes if dataset is closed
        if self.model.annotation_editor_model.annotation_data is None:
            for checkbox in self.ui.checkboxes:
                checkbox.setChecked(False)
            return

        track_id = self.model.track_id
        if track_id is None:
            for checkbox in self.ui.checkboxes:
                checkbox.setChecked(False)
            return

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

        msg = QMessageBox()
        msg.setWindowTitle("Save changes?")
        msg.setText("Do you want to save unchanged changes to the defect annotation?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
        answer = msg.exec() 
        if answer == QMessageBox.Yes:
            print("Saving defect annotation to file")
            file_name, _ = QFileDialog.getSaveFileName(
                None, "Save Defect Annotation", "", "", "JSON Files (*.json)")
            # make sure filename has JSON extension
            if len(file_name) > 0:
                file_name = ".".join([os.path.splitext(file_name)[0], "json"])

                if self.model.annotation_editor_model.annotation_data is not None:
                    print("Saving to ", file_name)
                    annotation_data_json = annotation_data_to_json(self.model.annotation_editor_model.annotation_data)
                    #json.dump(annotation_data_json, open(file_name, "w"))
                    print(annotation_data_json)

        elif answer == QMessageBox.No:
            print("Discarding defect annotation")
            self.discard_annotation()

        elif answer == QMessageBox.Cancel:
            print("Doing nothing")
            pass

    @Slot()
    def load_annotation_file(self):
        # TODO:
        # - open file dialog to select annotation file
        # - load from file and update annotation data model (should update checkboxes)
        pass

    @Slot()
    def discard_annotation(self):
        # TODO:
        # - dialog: ask if changes should be discarded?
        # -clear annotation data
        # - also call when changes were made and are about to be lost when proceeding
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