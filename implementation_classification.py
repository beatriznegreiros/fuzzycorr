try:
    import mapoperator as mo
    from pathlib import Path
    import numpy as np
    import gdal
except:
    print('ModuleNotFoundError: Missing fundamental packages (required: pathlib, numpy, gdal).')

# ---------------------INPUT------------------------------------------
d = 0.013  # in cm
n_classes = 6

# Measured Data:
raster_A = "diamond_map_A_res0.1_norm"

# Simulated Data:
raster_B = "diamond_map_B_res0.1_norm"

# Selected output names for the classified rasters
name_A = "diamond_A_res0.1_norm_class"
name_B = "diamond_B_res0.1_norm_class"
# --------------------------------------------------------------------

dir = Path.cwd()
Path(dir / "rasters").mkdir(exist_ok=True)

if '.' not in raster_A[-4:]:
    raster_A += '.tif'
map_A_in = str(dir / "rasters") + "/" + raster_A

if '.' not in raster_B[-4:]:
    raster_B += '.tif'
map_B_in = str(dir / "rasters/") + "/" + raster_B

# Classification based on d84
# Bins to classify the data Legend: HE (High Erosion), HIE (High Intermediate Erosion), IE (Intermediate Erosion),
# LIE (Low Intermediate Erosion), LE (Low Erosion), Static,  LD (Low Deposition), LID (Low Intermediate Deposition),
# ID (Intermediate Deposition), HID (High Intermediate Deposition), HD (High Deposition).
'''class_bins = [-100 * d, -20 * d, -10 * d, -5 * d, -2 * d, -0.5 * d, 0.5 * d, 2 * d, 5 * d, 10 * d, 20 * d,
              np.iinfo(np.int32).max]
'''

# Import raster as np array
array_A = mo.MapArray(name_A, map_A_in)
array_B = mo.MapArray(name_B, map_B_in)

# Classify the array and save the output file as .tif raster
nb_classes = array_A.nb_classes(n_classes)  # Extract the optimized intervals for the map A
array_A.categorize_raster(nb_classes, dir)
array_B.categorize_raster(nb_classes, dir)
