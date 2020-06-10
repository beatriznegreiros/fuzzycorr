from pathlib import Path
from scipy import stats
import mapoperator
import numpy as np


current_dir = Path.cwd().parent.parent
# INPUT: Raster input path
map_A_in = str(current_dir / "rasters/map_A.tif")
map_B_in = str(current_dir / "rasters/map_B.tif")

data_array_physical = mapoperator.raster_to_np(
    map_A_in)  # change to 2D array data (e.g., physical model output for terrain change)
data_array_numerical = mapoperator.raster_to_np(map_B_in)  # change to 2D array data (e.g., numerical model output for
# terrain change)

# Pearson Correlation
corr = stats.pearsonr(data_array_numerical.flatten(), data_array_physical.flatten())
print("The pearson correlation is:", corr[0])

# R²
slope, intercept, r_value, p_value, std_err = stats.linregress(data_array_numerical.flatten(), data_array_physical.flatten())
print("R-squared: %f" % r_value**2)