from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon

from src.ui.ui_data_sources import Ui_DataSources


class DataSourcesView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.parent = parent
        self.ui = Ui_DataSources()
        self.ui.setupUi(self)
        # setup icons
        self.ui.pushButtonNewAnalysis.setIcon(QIcon.fromTheme("list-add"))
        self.ui.pushButtonDelete.setIcon(QIcon.fromTheme("list-remove"))

        self.update()
        # connect signals and slots
        self.ui.pushButtonDelete.clicked.connect(self.delete_source)
        self.ui.pushButtonNewAnalysis.clicked.connect(self.parent.show_analysis_module_temperatures)
        self.ui.dataSourcesListWidget.itemClicked.connect(lambda name: self.controller.load_source(name.text()))
        self.ui.dataSourcesListWidget.itemClicked.connect(lambda name: self.ui.pushButtonDelete.setEnabled(name.text() != "Module Layout"))
        self.model.source_names_changed.connect(self.update)
        self.model.dataset_opened.connect(self.update)
        self.model.dataset_opened.connect(lambda: self.ui.pushButtonNewAnalysis.setEnabled(True))
        self.model.dataset_closed.connect(self.update)
        self.model.dataset_closed.connect(lambda: self.ui.pushButtonNewAnalysis.setEnabled(False))

    def delete_source(self):
        selected_name = self.ui.dataSourcesListWidget.currentItem()
        if selected_name is None:
            return
        selected_name = selected_name.text()

        delete_dialog_title = "Delete Data Source"
        delete_dialog_text = ("Are you sure you want to permanetely delete \"{}\"? "
                              "All associated files will be permanentely removed.").format(selected_name)
        delete_dialog = QMessageBox(
            QMessageBox.Question, 
            delete_dialog_title, 
            delete_dialog_text, 
            QMessageBox.Yes|QMessageBox.No)
        
        if delete_dialog.exec() == QMessageBox.Yes:
            self.controller.delete_source(selected_name)
    
    @Slot()
    def update(self):
        self.ui.dataSourcesListWidget.clear()
        if self.model.dataset_is_open:
            self.ui.dataSourcesListWidget.addItems(self.model.source_names)
            if self.model.selected_source == "Module Layout":
                self.ui.dataSourcesListWidget.setCurrentRow(0)