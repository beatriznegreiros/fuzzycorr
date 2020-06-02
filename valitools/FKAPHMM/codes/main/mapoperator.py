try:
    import geopandas
    import ogr
    import gdal
    import rasterio as rio
    import numpy as np
    import mapclassify.classifiers as mc
    import pandas as pd
    from pathlib import Path
except:
    print('ExceptionERROR: Missing fundamental packages (required: geopandas, ogr, gdal, rasterio, numpy, '
          'mapclassify, pandas, pathlib).')


def data_to_shape(data, outputfile):
    # Importing raw data into a dataframe
    data = pd.read_csv(data, skip_blank_lines=True)
    data.dropna(how='any', inplace=True, axis=0)

    # Create the dictionary with new label names and then rename for standardization
    new_names = {data.columns[0]: 'x', data.columns[1]: 'y', data.columns[2]: 'dz'}
    data = data.rename(columns=new_names)

    # Create geodataframe from the dataframe
    gdf = geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy(data.x, data.y))
    gdf = gdf.drop(['x', 'y'], axis=1)  # exclude columns of labels x and y

    # Saving the shapefile
    gdf.to_file(outputfile)


def shape_to_raster(x_res, y_res, _in, _out):
    # Open Shapefile and get layer
    source_ds = ogr.Open(_in)
    source_layer = source_ds.GetLayer()
    x_min, x_max, y_min, y_max = source_layer.GetExtent()

    # Set NoDataValue
    nodatavalue = -9999

    # Create Target - TIFF
    cols = int((x_max - x_min) / x_res)
    rows = int((y_max - y_min) / y_res)
    _raster = gdal.GetDriverByName('GTiff').Create(_out, cols, rows, 1, gdal.GDT_Float32)
    _raster.SetGeoTransform((x_min, x_res, 0, y_max, 0, -y_res))
    _band = _raster.GetRasterBand(1)
    _band.SetNoDataValue(nodatavalue)

    # Rasterize
    gdal.RasterizeLayer(_raster, [1], source_layer, options=['ATTRIBUTE=dz'])


def classifier(map_in, map_out, class_bins):
    # Open and read the raster
    with rio.open(map_in) as src:
        raster = src.read(1, masked=True)
        msk = src.read_masks(1)  # reading map's mask
        nodatavalue = src.nodata  # storing nodatavalue of raster
        meta = src.meta.copy()

    # Classify the original image array (digitize makes nodatavalues take the class 0)
    raster_class = np.digitize(raster, class_bins, right = True)

    # Assigns nodatavalues back to array
    raster_ma = np.ma.masked_where(raster_class == 0,
                                   raster_class,
                                   copy=True)

    # Fill nodatavalues into array
    raster_ma_fi = np.ma.filled(raster_ma, fill_value=nodatavalue)

    if raster_ma_fi.min() == nodatavalue:
        with rio.open(map_out, 'w', **meta) as outf:
            outf.write(raster_ma_fi.astype(rio.float32), 1)
    else:
        raise TypeError("Error filling NoDataValue to raster file")


def raster_to_np(map_in):
    with rio.open(map_in) as src:
        raster_np = src.read(1, masked=True)
    return raster_np


def nb_classes(array, n_classes):
    # Classification based on Natural Breaks
    breaks = mc.NaturalBreaks(array.ravel(), k=n_classes)
    print('The bins were optimized to be:', breaks.bins)
    class_bins = breaks.bins.tolist()
    return class_bins

