try:
    import geopandas
    import ogr
    import gdal
    import rasterio as rio
    import numpy as np
    import mapclassify.classifiers as mc
    import pandas as pd
    import math
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


def raster_to_np(map_in, msk=True):
    with rio.open(map_in) as src:
        raster_np = src.read(1, masked=msk)
        global nodatavalue
        nodatavalue = src.nodata  # storing nodatavalue of raster
        global meta
        meta = src.meta.copy()
    return raster_np


def f_similarity(a, b):
    return 1 - (abs(a - b)) / max(abs(a), abs(b))


class MapArray:
    def __init__(self, array):
        self.array = array

    # Method to output class bins based on Natural Breaks
    def nb_classes(self, n_classes):
        # Classification based on Natural Breaks
        breaks = mc.NaturalBreaks(self.array.ravel(), k=n_classes + 1)
        print('The bins were optimized to be:', breaks.bins)
        class_bins = breaks.bins.tolist()
        return class_bins

    def neighbours(self, x, y, n=4, halving_dist=2):
        x_up = max(x - n, 0)
        x_lower = min(x + n + 1, self.array.shape[0])
        y_up = max(y - n, 0)
        y_lower = min(y + n + 1, self.array.shape[1])
        memb = np.zeros((x_lower - x_up, y_lower - y_up), dtype=np.float32)
        i = 0
        for row in range(x_up, x_lower):
            j = 0
            for column in range(y_up, y_lower):
                d = math.sqrt((row - x) ** 2 + (column - y) ** 2)
                memb[i, j] = 2**(-d/halving_dist)
                j += 1
            i += 1
        return memb, self.array[x_up: x_lower, y_up: y_lower]

    def classifier(self, map_out, class_bins):
        # Classify the original image array (digitize makes nodatavalues take the class 0)
        raster_class = np.digitize(self.array, class_bins, right=True)

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
