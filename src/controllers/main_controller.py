import os
import json
import shutil
import pickle
import numpy as np

from PySide6.QtCore import Slot, Signal, QObject

from src.common import get_immediate_subdirectories


class MainController(QObject):
    source_deleted = Signal()

    def __init__(self, model):
        super().__init__()
        self.model = model

    @Slot(str)
    def open_dataset(self, dataset_dir):
        self.model.dataset_dir = dataset_dir
        self.model.patch_meta = pickle.load(open(os.path.join(
            self.model.dataset_dir, "patches", "meta.pkl"), "rb"))
        self.update_source_names()
        self.loadSource("Module Layout")
        self.model.dataset_is_open = True

    @Slot()
    def close_dataset(self):
        self.model.reset()
        self.model.dataset_is_open = False

    @Slot()
    def update_source_names(self):
        source_names = []
        if self.model.dataset_dir is not None:
            source_names = sorted(get_immediate_subdirectories(
                os.path.join(self.model.dataset_dir, "analyses")))
        source_names.insert(0, "Module Layout")
        self.model.source_names = source_names

    @Slot(str)
    def loadSource(self, selected_source):
        print("Updating", selected_source)
        if self.model.dataset_dir is None:
            return
        if selected_source is None:
            return
        if selected_source == "Module Layout":
            self.model.data = json.load(open(os.path.join(
                self.model.dataset_dir, "mapping", "module_geolocations_refined.geojson"), "r"))
            self.model.meta = None            
        else:
            self.model.data = json.load(open(os.path.join(
                self.model.dataset_dir, "analyses", selected_source, "results.geojson"), "r"))
            self.model.meta = json.load(open(os.path.join(
                self.model.dataset_dir, "analyses", selected_source, "meta.json"), "r"))
        self.model.selected_source = selected_source

    @Slot()
    def delete_source(self, selected_source):
        if self.model.dataset_dir is None:
            return
        if selected_source is None:
            return
        if selected_source == "Module Layout":
            return
        if selected_source == self.model.selected_source:
            self.source_deleted.emit()
        rmdir = os.path.join(self.model.dataset_dir, "analyses", selected_source)
        print("Deleting {}".format(rmdir))
        shutil.rmtree(rmdir, ignore_errors=True)
        self.update_source_names()

    @Slot()
    def get_column_names(self):
        if self.model.dataset_dir is None:
            return []
        columns_names = set()
        for feature in self.model.data["features"]:
            columns_names = columns_names | set(feature["properties"].keys())
        columns_names -= set(["track_id"])
        return sorted(list(columns_names))

    @Slot()
    def get_selected_column(self):
        if self.model.selected_column is None:
            return {}
        columns_names = self.get_column_names()
        column = columns_names[self.model.selected_column]
        return self.get_column(column)

    @Slot()
    def get_column(self, column):
        if self.model.dataset_dir is None:
            return {}        
        column_values = {}
        for feature in self.model.data["features"]:
            track_id = feature["properties"]["track_id"]
            try:
                val = feature["properties"][column]
                if val is None:
                    val = np.nan
                column_values[track_id] = val
            except KeyError:
                continue
        return column_values