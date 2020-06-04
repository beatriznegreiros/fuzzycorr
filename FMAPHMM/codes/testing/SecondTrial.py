import pandas as pd
import geopandas
import gdal
import matplotlib.pyplot as plt
from shapely import wkt
import fiona; fiona.supported_drivers
import ogr
import geo_operator

# importing raw data into dataframe
data_A = pd.read_csv("hexagon_experiment.csv")
data_B = pd.read_csv("hexagon_simulation.csv")

# Create the dictionary with old and new names
new_names = {data_A.columns[0]: 'x', data_A.columns[1]: 'y', data_A.columns[2]: 'dz'}
data_A = data_A.rename(columns=new_names)
print(data_A.head())

# creating geodataframe from the dataframe
gdf = geopandas.GeoDataFrame(data_A, geometry=geopandas.points_from_xy(data_A.x, data_A.y))
gdf = gdf.drop(['x', 'y'], axis=1) #  dropping the labels x and y
print(gdf.head())

ax = gdf.plot()
gdf.plot(ax=ax, color='red')
plt.show()

gdf.to_file("map_A.shp")


# 1. Define pixel_size and NoData value of new raster
NoData_value = -9999
x_res = 0.1  # assuming these are the cell sizes
y_res = 0.01111  # change as appropriate
pixel_size = 1

# 2. Filenames for in- and output
_in = r"C:/Users/beatr/PycharmProjects/myFirstPythonCode/map_A.shp"
_out = r"C:/Users/beatr/PycharmProjects/myFirstPythonCode/map_A_3.tif"

# 3. Open Shapefile
source_ds = ogr.Open(_in)
source_layer = source_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()
print(x_min, x_max, y_min, y_max)

# 4. Create Target - TIFF
cols = int((x_max - x_min)/x_res)
rows = int((y_max - y_min)/y_res)

_raster = gdal.GetDriverByName('GTiff').Create(_out, cols, rows, 1, gdal.GDT_Float32)
_raster.SetGeoTransform((x_min, x_res, 0, y_max, 0, -y_res))
_band = _raster.GetRasterBand(1)
_band.SetNoDataValue(NoData_value)

# 5. Rasterize
gdal.RasterizeLayer(_raster, [1], source_layer, options=['ATTRIBUTE=dz'])

