import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, to_hex


def get_colors(data_column, cmap="plasma", vmin=None, vmax=None):
    # get colors form colormap
    colormap = plt.get_cmap(cmap, 256)
    norm = Normalize(vmin, vmax)
    values = np.array(list(data_column.values()))
    colors = colormap(norm(values))

    # convert to hex
    hex_colors = {}
    for track_id, color in zip(data_column.keys(), colors):
        hex_colors[track_id] = to_hex(color)

    return hex_colors