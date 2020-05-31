import numpy as np
from collections.abc import Iterable  # used in the flatten function
import os, sys, glob, time  # remove irrelevant
import rasterio as rio
from pathlib import Path
from scipy import stats


def raster_to_np(map_in):
    with rio.open(map_in) as src:
        raster_np = src.read(1, masked=True)
    return raster_np


if __name__ == '__main__':
    current_dir = Path.cwd().parent.parent

    # INPUT: Raster input path
    map_A_in = str(current_dir / "rasters/map_A.tif")
    map_B_in = str(current_dir / "rasters/map_B.tif")

    data_array_physical = raster_to_np(
        map_A_in)  # change to 2D array data (e.g., physical model output for terrain change)
    data_array_numerical = raster_to_np(map_B_in)  # change to 2D array data (e.g., numerical model output for
    # terrain change)

    corr = stats.pearsonr(data_array_numerical.flatten(), data_array_physical.flatten())
    print("The pearson correlation is:", corr[0])
