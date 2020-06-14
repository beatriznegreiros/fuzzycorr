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
    print('ModuleNotFoundError: Missing fundamental packages (required: geopandas, ogr, gdal, rasterio, numpy, '
          'mapclassify, pandas, pathlib).')

current_dir = Path.cwd().parent.parent
Path(current_dir / "shapefiles").mkdir(exist_ok=True)
Path(current_dir / "rasters").mkdir(exist_ok=True)


def data_to_shape(path_data, outputfile):
    """ Routine to convert .csv to shapefile

    :param path_data: string, path of the csv file to be converted to shapefile
    :param outputfile: string, path of the output shapefile
    :return: no output, saves the shapefile in the default directory
    """
    # Importing raw data into a dataframe
    path_data = pd.read_csv(path_data, skip_blank_lines=True)
    path_data.dropna(how='any', inplace=True, axis=0)

    # Create the dictionary with new label names and then rename for standardization
    new_names = {path_data.columns[0]: 'x', path_data.columns[1]: 'y', path_data.columns[2]: 'attribute'}
    path_data = path_data.rename(columns=new_names)

    # Create geodataframe from the dataframe
    gdf = geopandas.GeoDataFrame(path_data, geometry=geopandas.points_from_xy(path_data.x, path_data.y))

    # TODO: Step for resampling and interpolation

    gdf = gdf.drop(['x', 'y'], axis=1)  # exclude columns of labels x and y

    # Saving the shapefile
    gdf.to_file(outputfile)


def template_raster(shape_A, shape_B):
    source_layer_A = ogr.Open(shape_A).GetLayer()
    x_min_A, x_max_A, y_min_A, y_max_A = source_layer_A.GetExtent()

    source_layer_B = ogr.Open(shape_B).GetLayer()
    x_min_B, x_max_B, y_min_B, y_max_B = source_layer_B.GetExtent()

    x_min = min(x_min_A, x_min_B)
    y_min = min(y_min_A, y_min_B)
    x_max = max(x_max_A, x_max_B)
    y_max = max(y_max_A, y_max_B)

    return x_min, x_max, y_min, y_max


def shape_to_raster(x_res, y_res, shapefile, _out):
    """ Converts shapfile to rasters (.tif)

    :param use_template:
    :param x_res: float, resolution of the cell in x
    :param y_res: float, resolution of the cell in y
    :param shapefile: string, path of the shapefile to be converted
    :param _out: string, path of the raster to be saved (.tif)
    :return: no output, saves the raster in the default directory
    """
    source_ds = ogr.Open(shapefile)
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
    gdal.RasterizeLayer(_raster, [1], source_layer, options=['ATTRIBUTE=attribute'])


def raster_to_np(map_in, msk=True):
    """ Reads a raster (.tif) as numpy array

    :param map_in: string, path of the raster to be read (.tif)
    :param msk: boolean, masked or not?
    :return: masked (or not) ndarray, the 2d numpy array
    """
    with rio.open(map_in) as src:
        raster_np = src.read(1, masked=msk)
        global nodatavalue
        global meta
        nodatavalue = src.nodata  # storing nodatavalue of raster
        meta = src.meta.copy()
    return raster_np


def data_to_raster(path, name, x_res, y_res):
    """ Generates raster and shapefile from .csv data
    NOTE: data must contain 3 columns [x,y, attribute]

    :param path: string, path of the .csv file
    :param name: string, name of the file to be output
    :param x_res: float, resolution in x of the raster
    :param y_res: float, resolution in y of the raster
    :return: no return, saves shapefile and raster in default directory
    """
    if '.' not in path[-4:]:
        path += '.csv'

    # Shapefiles Paths
    shape = str(current_dir / "shapefiles") + "/" + name + ".shp"

    # Rasters
    raster = str(current_dir / "rasters") + "/" + name + ".tif"
    raster_asc = str(current_dir / "rasters") + "/" + name + ".asc"

    # Create shapefile from dataframe
    data_to_shape(path, shape)

    # Create Raster from shapefile
    shape_to_raster(x_res, y_res, shape, raster)

    # Converts raster to .asc format
    gdal.Translate(raster_asc, raster, format='AAIGrid')


class MapArray:
    def __init__(self, array):
        self.array = array

    def nb_classes(self, n_classes):
        """ Class bins based on Natural Breaks

        :param n_classes: integer, number of classes
        :return: list, optimized bins
        """
        # Classification based on Natural Breaks
        breaks = mc.NaturalBreaks(self.array.ravel(), k=n_classes + 1)
        print('The bins were optimized to:', breaks.bins)
        class_bins = breaks.bins.tolist()
        return class_bins

    def neighbours(self, x, y, n=4, halving_dist=2):
        """ Takes the neighbours and their memberships

        :param x: int, cell in x
        :param y: int, cell in y
        :param n: int, 'radius' of neighbourhood
        :param halving_dist: int, halving distance of the distance decay function
        :return: ndarray (float) membership of the neighbours, ndarray (float) neighbours' cells
        """
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
                memb[i, j] = 2 ** (-d / halving_dist)
                j += 1
            i += 1
        return memb, self.array[x_up: x_lower, y_up: y_lower]

    def classifier(self, map_out, class_bins):
        """ Classifies the raster according to the classification bins

        :param map_out: string, path of the classified map to be generated
        :param class_bins: list
        :return: no return, saves the classified raster in the chosen directory
        """
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
