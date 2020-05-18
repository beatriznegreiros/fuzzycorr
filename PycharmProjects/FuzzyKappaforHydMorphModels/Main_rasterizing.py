import pandas as pd
import fiona; fiona.supported_drivers
import geo_operator

# Importing raw data into dataframe
data_A = pd.read_csv("hexagon_experiment.csv", skip_blank_lines=True)
data_B = pd.read_csv("hexagon_simulation.csv", skip_blank_lines=True)


# Create shapefile from dataframe
outname = "map_A.shp"
outname2 = "map_B.shp"
geo_operator.data_to_shape(data_A, outname)
geo_operator.data_to_shape(data_B, outname2)


# Create Raster from shapefile
x_res = 0.1  # assuming these are the cell sizes
y_res = 0.01111  # change as appropriate
A_in = "map_A.shp"
A_out = "map_A.tif"
geo_operator.shape_to_raster(x_res, y_res, A_in, A_out)

B_in = "map_B.shp"
B_out = "map_B.tif"
geo_operator.shape_to_raster(0.2, 0.01111, B_in, B_out)

