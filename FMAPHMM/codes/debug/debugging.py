import geopandas
import ogr
import gdal
import matplotlib.pyplot as plt


def data_to_shape(data, outputname):
    # Create the dictionary with new label names and then rename for standardization
    new_names = {data.columns[0]: 'x', data.columns[1]: 'y', data.columns[2]: 'dz'}
    data = data.rename(columns=new_names)

    # Create geodataframe from the dataframe
    gdf = geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy(data.x, data.y))
    gdf = gdf.drop(['x', 'y'], axis=1)  # exclude columns of labels x and y


    # Saving the shapefile
    gdf.to_file(filename=outputname, encoding='utf-8')


def shape_to_raster(x_res, y_res, _in, _out):
    # Open Shapefile and get layer
    source_ds = ogr.Open(_in)
    source_layer = source_ds.GetLayer()
    x_min, x_max, y_min, y_max = source_layer.GetExtent()

    # Set NoDataValue
    nodata_value = -9999

    # 4. Create Target - TIFF
    cols = int((x_max - x_min) / x_res)
    rows = int((y_max - y_min) / y_res)
    _raster = gdal.GetDriverByName('GTiff').Create(_out, cols, rows, 1, gdal.GDT_Float32)
    _raster.SetGeoTransform((x_min, x_res, 0, y_max, 0, -y_res))
    _band = _raster.GetRasterBand(1)
    _band.SetNoDataValue(nodata_value)

    # Rasterize
    gdal.RasterizeLayer(_raster, [1], source_layer, options=['ATTRIBUTE=dz'])


import pandas as pd


# Importing raw data into dataframe
data_A = pd.read_csv("hexagon_experiment.csv")
data_B = pd.read_csv("hexagon_simulation.csv")

data_A.dropna(how='any', inplace=True, axis=0)
data_B.dropna(how='any', inplace=True, axis=0)


data_to_shape(data_B, "map_B.shp")

B_in = r"C:/Users/beatr/PycharmProjects/myFirstPythonCode/map_B.shp"
B_out = r"C:/Users/beatr/PycharmProjects/myFirstPythonCode/map_B.tif"
shape_to_raster(0.2, 0.01111, B_in, B_out)

df = geopandas.GeoDataFrame.from_file('map_B.shp')
df.plot()
print(type(df))
figure = "figmapb"
plt.savefig(figure, dpi=600)
print(df)

plt.clf()

dfa = geopandas.GeoDataFrame.from_file('map_A.shp')
dfa.plot()
print(type(dfa))
figure = "figmapa"
plt.savefig(figure, dpi=600)
print(dfa)