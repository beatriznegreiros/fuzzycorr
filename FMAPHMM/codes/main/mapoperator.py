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
    from pyproj import CRS
    from scipy import interpolate
    from rasterio.transform import from_origin
except:
    print('ModuleNotFoundError: Missing fundamental packages (required: geopandas, ogr, gdal, rasterio, numpy, '
          'mapclassify, pandas, pathlib).')

current_dir = Path.cwd().parent.parent
Path(current_dir / "shapefiles").mkdir(exist_ok=True)
Path(current_dir / "rasters").mkdir(exist_ok=True)


class SpatialField:
    def __init__(self, name_dataset, pd, attribute, crs):
        self.pd = pd
        self.name = name_dataset
        self.shapefile = str(current_dir / "shapefiles") + "/" + self.name + ".shp"
        self.raster = str(current_dir / "rasters") + "/" + self.name + ".tif"
        self.normraster = str(current_dir / "rasters") + "/" + self.name + "_norm.tif"
        self.crs = crs
        self.attribute = attribute

        # Standardize the dataframe
        self.pd.dropna(how='any', inplace=True, axis=0)

        # Create the dictionary with new label names and then rename for standardization
        new_names = {self.pd.columns[0]: 'x', self.pd.columns[1]: 'y', self.pd.columns[2]: self.attribute}
        self.pd = self.pd.rename(columns=new_names)

        # Create geodataframe from the dataframe
        gdf = geopandas.GeoDataFrame(self.pd, geometry=geopandas.points_from_xy(self.pd.x, self.pd.y))
        gdf.crs = CRS(self.crs)
        self.gdf = gdf
        self.x = gdf.geometry.x.values
        self.y = gdf.geometry.y.values
        self.z = gdf[attribute].values

    def points_to_grid(self):
        """

        :return: array of size nrow, ncol

        http://chris35wills.github.io/gridding_data/
        """
        hrange = ((self.ymin, self.ymax),
                  (self.xmin, self.xmax))  # any points outside of this will be condisdered outliers and not used

        zi, yi, xi = np.histogram2d(self.y, self.x, bins=(int(self.nrow), int(self.ncol)), weights=self.z, normed=False,
                                    range=hrange)
        counts, _, _ = np.histogram2d(self.y, self.x, bins=(int(self.nrow), int(self.ncol)), range=hrange)
        np.seterr(divide='ignore', invalid='ignore')  # we're dividing by zero but it's no big deal
        zi = np.divide(zi, counts)
        np.seterr(divide=None, invalid=None)  # we'll set it back now
        zi = np.ma.masked_invalid(zi)
        array = np.flipud(np.array(zi))

        return array

    def norm_array(self, res=None, ulc=(np.nan, np.nan), lrc=(np.nan, np.nan), method='linear'):
        """

        :return: interpolated and normalized array with selected resolution

        https://github.com/rosskush/skspatial
        """
        if np.isfinite(ulc[0]) and np.isfinite(lrc[0]):
            self.xmax = lrc[0]
            self.xmin = ulc[0]
            self.ymax = ulc[1]
            self.ymin = lrc[1]
        else:
            self.xmax = self.gdf.geometry.x.max()
            self.xmin = self.gdf.geometry.x.min()
            self.ymax = self.gdf.geometry.y.max()
            self.ymin = self.gdf.geometry.y.min()

        self.extent = (self.xmin, self.xmax, self.ymin, self.ymax)

        if np.isfinite(res):
            self.res = res
        else:
            # if res not passed, then res will be the distance between xmin and xmax / 1000
            self.res = (self.xmax - self.xmin) / 1000

        self.ncol = int(np.ceil((self.xmax - self.xmin) / self.res))  # delx
        self.nrow = int(np.ceil((self.ymax - self.ymin) / self.res))  # dely

        array = self.points_to_grid()
        x = np.arange(0, self.ncol)
        y = np.arange(0, self.nrow)
        # mask invalid values
        array = np.ma.masked_invalid(array)
        xx, yy = np.meshgrid(x, y)
        # get only the valid values
        x1 = xx[~array.mask]
        y1 = yy[~array.mask]
        newarr = array[~array.mask]
        GD1 = interpolate.griddata((x1, y1), newarr.ravel(), (xx, yy), method=method, fill_value=np.nan)

        return GD1

    def shape(self):
        self.gdf.to_file(self.shapefile)

    def plain_raster(self, res, nodatavalue=np.nan):
        """ Converts shapefile to rasters (.tif)

        :param nodatavalue:
        :param normalize_data:
        :param use_template:
        :param x_res: float, resolution of the cell in x
        :param y_res: float, resolution of the cell in y
        :param shapefile: string, path of the shapefile to be converted
        :param _out: string, path of the raster to be saved (.tif)
        :return: no output, saves the raster in the default directory
        """
        self.shape()
        source_ds = ogr.Open(self.shapefile)
        source_layer = source_ds.GetLayer()
        x_min, x_max, y_min, y_max = source_layer.GetExtent()

        # Create Target - TIFF
        cols = int((x_max - x_min) / res)
        rows = int((y_max - y_min) / res)
        _raster = gdal.GetDriverByName('GTiff').Create(self.raster, cols, rows, 1, gdal.GDT_Float32)
        _raster.SetGeoTransform((x_min, res, 0, y_max, 0, res))
        _band = _raster.GetRasterBand(1)
        _band.SetNoDataValue(nodatavalue)

        # Rasterize
        gdal.RasterizeLayer(_raster, [1], source_layer, options=['ATTRIBUTE=' + self.attribute])

    def norm_raster(self, nodatavalue=np.nan, res=None, ulc=(np.nan, np.nan), lrc=(np.nan, np.nan), method='linear'):
        array = self.norm_array(res=res, ulc=ulc, lrc=lrc, method=method)
        transform = from_origin(self.xmin, self.ymax, self.res, self.res)
        new_dataset = rio.open(self.normraster, 'w', driver='GTiff',
                                    height=array.shape[0], width=array.shape[1], count=1, dtype=array.dtype,
                                    crs=self.crs, transform=transform, nodata=nodatavalue)
        new_dataset.write(array, 1)
        new_dataset.close()

        return new_dataset

'''    def data_to_raster(self, x_res, y_res, nodatavalue=-9999, asc_format=True):
        """ Generates raster and shapefile from .csv data
        NOTE: data must contain 3 columns [x,y, attribute]

        :param path: string, path of the .csv file
        :param name: string, name of the file to be output
        :param x_res: float, resolution in x of the raster
        :param y_res: float, resolution in y of the raster
        :return: no return, saves shapefile and raster in default directory
        """

        raster_asc = str(current_dir / "rasters") + "/" + self.name + ".asc"

        # Create shapefile from dataframe
        self.data_to_shape()

        # Create Raster from shapefile
        self.shape_to_raster(x_res, y_res, nodatavalue=nodatavalue)

        if asc_format:
            # Converts raster to .asc format
            gdal.Translate(raster_asc, self.raster, format='AAIGrid') '''


class MapArray:
    def __init__(self, raster):
        self.raster = raster

        with rio.open(self.raster) as src:
            raster_np = src.read(1, masked=True)
            self.nodatavalue = src.nodata  # storing nodatavalue of raster
            self.meta = src.meta.copy()
        self.array = raster_np

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
        raster_ma_fi = np.ma.filled(raster_ma, fill_value=self.nodatavalue)

        if raster_ma_fi.min() == self.nodatavalue:
            with rio.open(map_out, 'w', **self.nodatavalue) as outf:
                outf.write(raster_ma_fi.astype(rio.float32), 1)
        else:
            raise TypeError("Error filling NoDataValue to raster file")


