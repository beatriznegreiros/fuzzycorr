import pandas as pd
import fiona; fiona.supported_drivers
import geo_operator
import gdal

# Input Data
x_res_A = 0.1  # assuming these are the cell sizes
y_res_A = 0.1  # change as appropriate
x_res_B = 0.1  # assuming these are the cell sizes
y_res_B = 0.1  # change as appropriate
shape_A = r"C:/Users/beatr/PycharmProjects/FKAPHMM/map_A.shp"
shape_B = r"C:/Users/beatr/PycharmProjects/FKAPHMM/map_B.shp"
raster_A = r"C:/Users/beatr/PycharmProjects/FKAPHMM/map_A.tif"
raster_B = r"C:/Users/beatr/PycharmProjects/FKAPHMM/map_B.tif"
raster_A_asc = r"C:/Users/beatr/PycharmProjects/FKAPHMM/map_A.asc"
raster_B_asc = r"C:/Users/beatr/PycharmProjects/FKAPHMM/map_B.asc"


# Importing raw data into dataframe
data_A = pd.read_csv("hexagon_experiment.csv", skip_blank_lines=True)
data_B = pd.read_csv("hexagon_simulation.csv", skip_blank_lines=True)
data_A.dropna(how='any', inplace=True, axis=0)
data_B.dropna(how='any', inplace=True, axis=0)

# Create shapefile from dataframe
geo_operator.data_to_shape(data_A, shape_A)
geo_operator.data_to_shape(data_B, shape_B)

# Create Raster from shapefile
geo_operator.shape_to_raster(x_res_A, y_res_A, shape_A, raster_A)
geo_operator.shape_to_raster(x_res_B, y_res_B, shape_B, raster_B)

gdal.Translate(raster_B_asc, raster_B, format='AAIGrid')
gdal.Translate(raster_A_asc, raster_A, format='AAIGrid')
