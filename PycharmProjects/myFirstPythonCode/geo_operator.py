import geopandas
import ogr
import gdal


def data_to_shape(data, outputname):
    # Create the dictionary with new label names and then rename for standardization
    new_names = {data.columns[0]: 'x', data.columns[1]: 'y', data.columns[2]: 'dz'}
    data = data.rename(columns=new_names)

    # Create geodataframe from the dataframe
    gdf = geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy(data.x, data.y))
    gdf = gdf.drop(['x', 'y'], axis=1)  # exclude columns of labels x and y

    # Saving the shapefile
    gdf.to_file(outputname)


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

