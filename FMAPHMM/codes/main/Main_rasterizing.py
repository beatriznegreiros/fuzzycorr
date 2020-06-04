import pandas as pd
import fiona;fiona.supported_drivers
import mapoperator as mo
import gdal
from pathlib import Path

current_dir = Path.cwd().parent.parent
Path(current_dir / "shapefiles").mkdir(exist_ok=True)
Path(current_dir / "rasters").mkdir(exist_ok=True)

# --------------------------INPUT DATA--------------------------
# 1. Input:
#  1.1 Raw Data:
path_A = current_dir / "raw_data/hexagon_experiment.csv"
path_B = current_dir / "raw_data/hexagon_simulation.csv"

#  1.2 Raster Resolution: Change as appropriate
#  NOTE: For the Fuzzy Analysis choose one unique resolution
x_res_A = 0.2
y_res_A = 0.2
x_res_B = 0.2
y_res_B = 0.2
# --------------------------------------------------------------

# 2. Shapefiles Paths
shape_A = str(current_dir / "shapefiles/map_A.shp")
shape_B = str(current_dir / "shapefiles/map_B.shp")

# 3. Raster
#  3.1 Raster paths: tif format (enter file path and file name ending with *.tif)
raster_A = str(current_dir / "rasters/map_A.tif")
raster_B = str(current_dir / "rasters/map_B.tif")

#  3.2 Raster paths: ascii format (enter file path and file name ending with *.asc)
raster_A_asc = str(current_dir / "rasters/map_A.asc")
raster_B_asc = str(current_dir / "rasters/map_B.asc")

# 4. Create shapefile from dataframe
mo.data_to_shape(path_A, shape_A)
mo.data_to_shape(path_B, shape_B)

# 5. Create Raster from shapefile
mo.shape_to_raster(x_res_A, y_res_A, shape_A, raster_A)
mo.shape_to_raster(x_res_B, y_res_B, shape_B, raster_B)

gdal.Translate(raster_B_asc, raster_B, format='AAIGrid')
gdal.Translate(raster_A_asc, raster_A, format='AAIGrid')
