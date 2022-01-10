import os
import glob
import json
import datetime
from collections import defaultdict
import cv2
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree

from PySide6.QtCore import QObject, Signal

from ..utils.common import get_immediate_subdirectories, to_celsius
from ..utils.geojson import load_geojson, save_geojson, coords_wgs84_to_ltp


def load_modules(file):
    df = load_geojson(open(file, "r"))
    df = df.set_index("track_id")
    df_ltp = coords_wgs84_to_ltp(df)
    df_corners = df_ltp.loc[df_ltp["geometry_type"] == "Polygon"]
    df_centers = df_ltp.loc[df_ltp["geometry_type"] == "Point"]
    return df, df_corners, df_centers

def truncate_patch(patch, margin=0.05):
    """Truncates module edges by margin (percent of width) to remove module frame."""
    width = patch.shape[1]
    margin_px = int(margin*width)
    patch = patch[margin_px:-margin_px, margin_px:-margin_px]
    return patch


def remove_patches_with_sun_reflection(patch_files, sun_reflections):
    """Returns a copy of the patch_files list withput patches that contain a sun reflections as per 'sun_reflections'."""
    patch_files_filtered = []
    for patch_file in patch_files:
        patch_name = os.path.splitext(os.path.basename(patch_file))[0]
        if patch_name not in sun_reflections:
            patch_files_filtered.append(patch_file)
    return patch_files_filtered


def get_patch_temps(patch_files, margin, to_celsius_gain, to_celsius_offset):
    """Returns min, max, mean and median temperatures for each patch of a module."""
    temps = defaultdict(list)
    for patch_file in patch_files:
        patch = cv2.imread(patch_file, cv2.IMREAD_ANYDEPTH)
        if patch is not None:
            patch = truncate_patch(patch, margin)
            temps["min"].append(to_celsius(np.min(patch), to_celsius_gain, to_celsius_offset))
            temps["max"].append(to_celsius(np.max(patch), to_celsius_gain, to_celsius_offset))
            temps["mean"].append(to_celsius(np.mean(patch), to_celsius_gain, to_celsius_offset))
            temps["median"].append(to_celsius(np.median(patch), to_celsius_gain, to_celsius_offset))
    return temps


def mean_over_patches(dataframe, temps):
    """Compute the mean of the module temperatures over all patches of a module."""
    for patch_area_agg in ["min", "max", "mean", "median"]:
        dataframe["{}_temp".format(patch_area_agg)] = pd.Series({track_id: np.mean(t[patch_area_agg]) for track_id, t in temps.items()})


class AnalysisModuleTemperaturesWorker(QObject):
    finished = Signal()
    progress = Signal(float, bool, str)

    def __init__(self, dataset_dir, dataset_version, name, to_celsius_gain, to_celsius_offset, 
            border_margin, neighbour_radius, ignore_sun_reflections, sun_reflections):
        super().__init__()
        self.is_cancelled = False
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.dataset_dir = dataset_dir
        self.dataset_version = dataset_version
        self.name = name
        self.to_celsius_gain = to_celsius_gain
        self.to_celsius_offset = to_celsius_offset
        self.border_margin = 0.01 * border_margin
        self.neighbour_radius = neighbour_radius
        self.ignore_sun_reflections = ignore_sun_reflections
        self.sun_reflections = sun_reflections
        self.progress_last_step = 0.0

    def get_neighbours_median_temp(self, df_centers, neighbour_radius=7, column="mean_of_max_temps"):
        """Returns a list of mean temperatures of the neighbours of each module in `df_centers`.
        The `neighbour_radius` defines the circle radius in which to look for neighbouring modules.
        The `column` specifies which temperature column to use."""
        centers = np.array([[d["coordinates"][0], d["coordinates"][1]] for d in df_centers["geometry"]])
        tree = KDTree(centers)
        neighbor_idxs = tree.query_radius(centers, r=neighbour_radius)
        
        # get mean temperature of neighbors
        neighbour_mean_temps = []
        for row_idx, neighbor_idx in enumerate(neighbor_idxs):
            progress = self.progress_last_step + (row_idx / len(neighbor_idxs)) / 5
            if self.is_cancelled:
                self.progress.emit(progress, True, "Cancelled")
                self.finished.emit()
                return

            neighbor_idx = np.delete(neighbor_idx, np.nonzero(neighbor_idx == row_idx))  # remove the current module from list of neighbors
            mean_temp = df_centers.iloc[neighbor_idx][column].median()
            neighbour_mean_temps.append(mean_temp)

            self.progress.emit(progress, False, "Computing corrected {}...".format(" ".join(column.split("_"))))
        self.progress_last_step = progress
        return neighbour_mean_temps

    def run(self):
        if self.dataset_version == "v1":
            patches_dir = os.path.join(self.dataset_dir, "patches_final", "radiometric")
        elif self.dataset_version == "v2":
            patches_dir = os.path.join(self.dataset_dir, "patches", "radiometric")

        file = os.path.join(self.dataset_dir, "mapping", "module_geolocations_refined.geojson")
        df, df_corners, df_centers = load_modules(file)

        temps = {}
        track_ids = sorted(get_immediate_subdirectories(patches_dir))
        for i, track_id in enumerate(track_ids):
            progress = (i / len(track_ids)) / 5
            if self.is_cancelled:
                self.progress.emit(progress, True, "Cancelled")
                self.finished.emit()
                return

            patch_files = sorted(glob.glob(os.path.join(patches_dir, track_id, "*")))
            if self.ignore_sun_reflections and self.sun_reflections is not None:
                patch_files = remove_patches_with_sun_reflection(patch_files, self.sun_reflections[track_id])
            temps[track_id] = get_patch_temps(patch_files, self.border_margin, self.to_celsius_gain, self.to_celsius_offset)

            self.progress.emit(progress, False, "Computing temperature distribution...")
        self.progress_last_step = progress
                
        mean_over_patches(df_corners, temps)
        mean_over_patches(df_centers, temps)

        for patch_area_agg in ["min", "max", "mean", "median"]:
            column = "{}_temp".format(patch_area_agg)
            neighbour_mean_temps = self.get_neighbours_median_temp(df_centers, neighbour_radius=self.neighbour_radius, column=column)
            if neighbour_mean_temps is None: # cancelled
                return

            df_corners["{}_corrected".format(column)] = df_corners.loc[:, column] - neighbour_mean_temps
            df_centers["{}_corrected".format(column)] = df_centers.loc[:, column] - neighbour_mean_temps

        # merge back into single geodataframe
        df_merged = df_corners.append(df_centers)

        # reuse WGS84 coordinates of original dataframe
        df_merged = df_merged.reset_index()
        df_merged = df_merged.set_index(["track_id", "geometry_type"])
        df = df.reset_index()
        df = df.set_index(["track_id", "geometry_type"])
        df_merged.update(df.loc[:, "geometry"])

        # write results to disk
        self.progress.emit(1, False, "Saving analysis results...")
        save_path = os.path.join(self.dataset_dir, "analyses", self.name)
        save_file = os.path.join(save_path, "results.geojson")
        print("Saving module temperature results in {}".format(save_file))
        os.makedirs(save_path, exist_ok=True)
        save_geojson(df_merged, open(save_file, "w"))

        print("Saving meta json in {}".format(os.path.join(save_path, "meta.json")))
        meta = {
            "type": "module_temperatures",
            "timestamp": self.timestamp,
            "dataset_dir": self.dataset_dir,
            "hyperparameters": {
                "border_margin": self.border_margin,
                "neighbour_radius": self.neighbour_radius,
                "ignore_sun_reflections": self.ignore_sun_reflections
            }
        }
        if self.ignore_sun_reflections and self.sun_reflections is not None:
            meta["hyperparameters"]["sun_reflections"] = self.sun_reflections
        json.dump(meta, open(os.path.join(save_path, "meta.json"), "w"))

        self.progress.emit(1, False, "Done")
        self.finished.emit()

