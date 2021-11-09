import os
import numpy as np


def get_immediate_subdirectories(a_dir):
    """Returns the immediate subdirectories of the provided directory."""
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]


def to_celsius(image):
    """Convert raw intensity values of radiometric image to Celsius scale."""
    return image*0.04-273.15


def normalize(image, vmin, vmax):
    image[image < vmin] = vmin
    image[image > vmax] = vmax
    image = (image - vmin) / (vmax - vmin)
    image = (255*image).astype(np.uint8)
    return image
