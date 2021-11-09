import os
import json

from PySide6.QtWidgets import QWidget, QCheckBox, QSpacerItem, QSizePolicy

from src.ui.ui_annotation_editor import Ui_AnnotationEditor


class AnnotationEditorView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.ui = Ui_AnnotationEditor()
        self.ui.setupUi(self)
        self.loadDefectsScheme()
        # TODO: connect signals and slots

    def loadDefectsScheme(self):
        try:
            defects_scheme = json.load(open(os.path.join("resources", "defect_schema.json"), "r"))
        except FileNotFoundError:
            pass
        else:
            for defect in defects_scheme:
                checkbox = QCheckBox("{} - {}".format(defect["name"], defect["description"]))
                checkbox.setToolTip(", ".join(defect["examples"]))
                self.ui.scrollAreaWidgetContents.layout().addWidget(checkbox)
            self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.ui.scrollAreaWidgetContents.layout().addItem(self.verticalSpacer)