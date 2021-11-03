import os
import glob
from collections import defaultdict
import cv2
import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.neighbors import KDTree


from common import get_immediate_subdirectories, to_celsius


def truncate_patch(patch, margin=0.05):
    """Truncates module edges by margin (percent of width) to remove module frame."""
    width = patch.shape[1]
    margin_px = int(margin*width)
    patch = patch[margin_px:-margin_px, margin_px:-margin_px]
    return patch


def load_modules_gdf(file):
    gdf = gpd.read_file(file)
    gdf = gdf.set_index("track_id")
    gdf = gdf.to_crs(epsg=3857)
    
    gdf_corners = gdf.loc[gdf.geom_type == "Polygon"]
    gdf_centers = gdf.loc[gdf.geom_type == "Point"]
    return gdf_corners, gdf_centers


def get_patch_temps(patch_files):
    """Returns some temperatures from patches of a module."""
    temps = defaultdict(list)
    for idx, patch_file in enumerate(patch_files):
        patch = cv2.imread(patch_file, cv2.IMREAD_ANYDEPTH)
        if patch is not None:
            patch = truncate_patch(patch)
            temps["min"].append(to_celsius(np.min(patch)))
            temps["max"].append(to_celsius(np.max(patch)))
            temps["mean"].append(to_celsius(np.mean(patch)))
            temps["median"].append(to_celsius(np.median(patch)))
    return temps


def insert_temps(geodataframe, temps):
    """max_of_mean_temps means: compute the mean temperature over all pixels of each patch, and
    pick the patch with the maximum mean temperature for each module"""
    for agg in ["min", "max", "mean", "median"]:  # aggregation over pixels of each patch
        geodataframe["max_of_{}_temps".format(agg)] = pd.Series({track_id: np.max(t[agg]) for track_id, t in temps.items()})
        geodataframe["min_of_{}_temps".format(agg)] = pd.Series({track_id: np.min(t[agg]) for track_id, t in temps.items()})
        geodataframe["mean_of_{}_temps".format(agg)] = pd.Series({track_id: np.mean(t[agg]) for track_id, t in temps.items()})
        geodataframe["median_of_{}_temps".format(agg)] = pd.Series({track_id: np.median(t[agg]) for track_id, t in temps.items()})
        geodataframe["first_of_{}_temps".format(agg)] = pd.Series({track_id: t[agg][0] for track_id, t in temps.items()})


def get_neighbours_median_temp(gdf_centers, neighbour_radius=7, column="mean_of_max_temps"):
    """Returns a list of mean temperatures of the neighbours of each module in `gdf_centers`.
    The `neighbour_radius` defines the circle radius in which to look for neighbouring modules.
    The `column` specifies which temperature column to use."""
    centers = np.array([[d.xy[0][0], d.xy[1][0]] for d in gdf_centers["geometry"]])
    tree = KDTree(centers)
    neighbor_idxs = tree.query_radius(centers, r=neighbour_radius)
    
    # get mean temperature of neighbors
    neighbour_mean_temps = []
    for row_idx, neighbor_idx in enumerate(neighbor_idxs):
        neighbor_idx = np.delete(neighbor_idx, np.nonzero(neighbor_idx == row_idx))  # remove the current module from list of neighbors
        mean_temp = gdf_centers.iloc[neighbor_idx][column].median()
        neighbour_mean_temps.append(mean_temp)
    return neighbour_mean_temps


def compute_temperatures(work_dir, progresBar):
    file = os.path.join(work_dir, "mapping", "module_geolocations_refined.geojson")
    gdf_corners, gdf_centers = load_modules_gdf(file)

    temps = {}
    track_ids = sorted(get_immediate_subdirectories(os.path.join(work_dir, "patches_final", "radiometric")))
    for i, track_id in enumerate(track_ids):
        patch_files = sorted(glob.glob(os.path.join(work_dir, "patches_final", "radiometric", track_id, "*")))
        temps[track_id] = get_patch_temps(patch_files)

        print(i)
        progresBar.setValue(i / len(track_ids))
            
    insert_temps(gdf_corners, temps)
    insert_temps(gdf_centers, temps)


