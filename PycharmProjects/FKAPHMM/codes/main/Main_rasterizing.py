import pandas as pd
import fiona; fiona.supported_drivers
import geo_operator
import gdal

# 1. Input: Raw Data
path_A = r"C:/Users/beatr/PycharmProjects/FKAPHMM/raw_data/hexagon_experiment.csv"
path_B = r"C:/Users/beatr/PycharmProjects/FKAPHMM/raw_data/hexagon_simulation.csv"

# 2. Input: Shapefiles Paths
shape_A = r"C:/Users/beatr/PycharmProjects/FKAPHMM/shapefiles/map_A.shp"
shape_B = r"C:/Users/beatr/PycharmProjects/FKAPHMM/shapefiles/map_B.shp"

# 3. Input: Raster
#  3.1 Raster paths: tif format (enter file path and file name ending with *.tif)
raster_A = r"C:/Users/beatr/PycharmProjects/FKAPHMM/rasters/map_A.tif"
raster_B = r"C:/Users/beatr/PycharmProjects/FKAPHMM/rasters/map_B.tif"

#  3.2 Raster paths: ascii format (enter file path and file name ending with *.asc)
raster_A_asc = r"C:/Users/beatr/PycharmProjects/FKAPHMM/rasters/map_A.asc"
raster_B_asc = r"C:/Users/beatr/PycharmProjects/FKAPHMM/rasters/map_B.asc"

#  3.2 Raster resolution
x_res_A = 0.1  # assuming these are the cell sizes
y_res_A = 0.1  # change as appropriate
x_res_B = 0.1  # assuming these are the cell sizes
y_res_B = 0.1  # change as appropriate

# 4. Importing raw data into dataframe
data_A = pd.read_csv(path_A, skip_blank_lines=True)
data_B = pd.read_csv(path_B, skip_blank_lines=True)
data_A.dropna(how='any', inplace=True, axis=0)
data_B.dropna(how='any', inplace=True, axis=0)

# 5. Create shapefile from dataframe
geo_operator.data_to_shape(data_A, shape_A)
geo_operator.data_to_shape(data_B, shape_B)

# 6. Create Raster from shapefile
geo_operator.shape_to_raster(x_res_A, y_res_A, shape_A, raster_A)
geo_operator.shape_to_raster(x_res_B, y_res_B, shape_B, raster_B)

gdal.Translate(raster_B_asc, raster_B, format='AAIGrid')
gdal.Translate(raster_A_asc, raster_A, format='AAIGrid')
