try:
    import matplotlib.pyplot as plt
    import mapoperator as mo
    from pathlib import Path
    import numpy as np
    import gdal
except:
    print('ModuleNotFoundError: Missing fundamental packages (required: pathlib, numpy, gdal).')

# ---------------------INPUT------------------------------------------
# Data:
list_files = ['vali_Hydro_FT-2D_MAP_2013_clipped',
              'vali_meas_2013_clipped',
              'vali_aPC_MAP_2013_clipped',
              'vali_hydro_FT_manual_2013_clipped']

# Selected output names for the classified rasters
name_A = "hexagon_exp_005_class"
name_B = "hexagon_sim_005_class"

nb_classes = [-3.6, -3.0, -2.4, -1.8, -1.2, -0.6, 0.0, 0.0, 0.6, 1.2, 1.8, 2.4, 3.0]
# --------------------------------------------------------------------

dir = Path.cwd()
Path(dir / "rasters").mkdir(exist_ok=True)

# Classification based on d84
# Bins to classify the data Legend: HE (High Erosion), HIE (High Intermediate Erosion), IE (Intermediate Erosion),
# LIE (Low Intermediate Erosion), LE (Low Erosion), Static,  LD (Low Deposition), LID (Low Intermediate Deposition),
# ID (Intermediate Deposition), HID (High Intermediate Deposition), HD (High Deposition).
# class_bins = [-100 * d, 50 * d, 100 * d, 200 * d, 500 * d, np.iinfo(np.int32).max]


# Classify the array and save the output file as .tif raster
for file in list_files:
    array_ = mo.MapArray(str(dir/'rasters') + '/' + file + '.tif')
    map_output = (str(dir/'rasters') + '/' + file + '_class.tif')
    array_.categorize_raster(nb_classes, map_output)

