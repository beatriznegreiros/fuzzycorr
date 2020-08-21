try:
    import geopandas
    import ogr
    import gdal
    import rasterio as rio
    import numpy as np
    import pandas as pd
    import alphashape
    import mapclassify.classifiers as mc
    from pathlib import Path
    from pyproj import CRS
    from scipy import interpolate
    from pykrige.ok import OrdinaryKriging
except:
    print('ModuleNotFoundError: Missing fundamental packages (required: geopandas, ogr, gdal, rasterio, numpy, pandas, alphashape, mapclassify, pathlib, pyproj, scipy and pykrige).')


class SpatialField:
    def __init__(self, pd, attribute, crs, nodatavalue, res=None, ulc=(np.nan, np.nan),
                 lrc=(np.nan, np.nan)):
        self.pd = pd
        if not isinstance(attribute, str):
            print("ERROR: attribute must be a string, check the name on your textfile")
        self.crs = CRS(crs)
        self.attribute = attribute
        self.nodatavalue = nodatavalue

        # Standardize the dataframe
        self.pd.dropna(how='any', inplace=True, axis=0)
        # Create the dictionary with new label names and then rename for standardization
        new_names = {self.pd.columns[0]: 'x', self.pd.columns[1]: 'y', self.pd.columns[2]: self.attribute}
        self.pd = self.pd.rename(columns=new_names)

        # Create geodataframe from the dataframe
        gdf = geopandas.GeoDataFrame(self.pd, geometry=geopandas.points_from_xy(self.pd.x, self.pd.y))
        gdf.crs = self.crs
        self.gdf = gdf
        self.x = gdf.geometry.x.values
        self.y = gdf.geometry.y.values
        self.z = gdf[attribute].values

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

    def points_to_grid(self):
        """ Create a grid of new points in the desired resolution to be interpolated
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

    def norm_array(self, method='linear'):
        """ Normalizes the raw data in equally sparsed points depending on the selected resolution
        :return: interpolated and normalized array with selected resolution
        see more at https://github.com/rosskush/skspatial
        """
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

        out_array = interpolate.griddata((x1, y1), newarr.ravel(), (xx, yy), method=method, fill_value=self.nodatavalue)

        return out_array

    def plain_raster(self, shapefile, raster_file, res):
        """ Converts shapefile(.shp) to rasters(.tif) without normalizing
        :param shapefile: string, filename with path of the input shapefile (*.shp)
        :param raster_file: stirng, filename with path of the output raster (*.tif)
        :param res: float, resolution of the cell
        :return: no output, saves the raster in the default directory
        """
        if '.' not in shapefile[-4:]:
            shapefile += '.shp'

        if '.' not in raster_file[-4:]:
            raster_file += '.tif'
        source_ds = ogr.Open(shapefile)
        source_layer = source_ds.GetLayer()
        x_min, x_max, y_min, y_max = source_layer.GetExtent()

        # Create Target - TIFF
        cols = int((x_max - x_min) / res)
        rows = int((y_max - y_min) / res)
        _raster = gdal.GetDriverByName('GTiff').Create(raster_file, cols, rows, 1, gdal.GDT_Float32)
        _raster.SetGeoTransform((x_min, res, 0, y_max, 0, res))
        _band = _raster.GetRasterBand(1)
        _band.SetNoDataValue(self.nodatavalue)

        # Rasterize
        gdal.RasterizeLayer(_raster, [1], source_layer, options=['ATTRIBUTE=' + self.attribute])

    def array2raster(self, array, raster_file, save_ascii=True):
        """ Saves a raster using interpolation
        :param raster_file: string, path to save the rasterfile
        :param save_ascii: boolean, true to save also an ascii raster
        :return: no output, saves the raster with the selected filename
        """
        if '.' not in raster_file[-4:]:
            raster_file += '.tif'

        self.transform = rio.transform.from_origin(self.xmin, self.ymax, self.res, self.res)
        new_dataset = rio.open(raster_file, 'w', driver='GTiff',
                               height=array.shape[0], width=array.shape[1], count=1, dtype=array.dtype,
                               crs=self.crs, transform=self.transform, nodata=self.nodatavalue)
        print(np.shape(array))
        new_dataset.write(array, 1)
        new_dataset.close()

        if save_ascii:
            map_asc = str(Path(raster_file[0:-4] + '.asc'))
            gdal.Translate(map_asc, raster_file, format='AAIGrid')

        return new_dataset

    def ok_2D(self, n_closest_points=None, variogram_model='linear', verbose=False,
              coordinates_type='geographic', backend='vectorized'):  # Ordinary Kriging

        # Credit to 'https://github.com/bsmurphy/PyKrige'

        OK = OrdinaryKriging(self.x, self.y, self.z, variogram_model=variogram_model, verbose=verbose,
                             enable_plotting=False, coordinates_type=coordinates_type)
        x, y = np.arange(0, self.ncol), np.arange(0, self.nrow)

        xpts = np.arange(self.xmin + self.res / 2, self.xmax + self.res / 2, self.res)
        ypts = np.arange(self.ymin + self.res / 2, self.ymax + self.res / 2, self.res)
        ypts = ypts[::-1]

        xp, yp = [], []
        for yi in ypts:
            for xi in xpts:
                xp.append(xi)
                yp.append(yi)

        if n_closest_points is not None:
            backend = 'loop'

        # krige_array, ss = OK.execute('points', x, y, n_closest_points=n_closest_points,backend=backend)
        krige_array, ss = OK.execute('points', xp, yp, n_closest_points=n_closest_points, backend=backend)

        krige_array = np.reshape(krige_array, (self.nrow, self.ncol))
        # print(krige_array.shape)

        return krige_array

    def create_polygon(self, shape_polygon, alpha=np.nan):
        """ Creates a polygon surrounding a cloud of shapepoints
        :param shape_polygon: string, path to save the shapefile
        :param alpha: float, excentricity of the alphashape (polygon) to be created
        :return: no output, saves the polygon (*.shp) with the selected filename
        """
        if np.isfinite(alpha):
            try:
                polygon = alphashape.alphashape(self.gdf, alpha)
            except FileNotFoundError as e:
                print(e)
        else:
            try:
                polygon = alphashape.alphashape(self.gdf)
            except FileNotFoundError as e:
                print(e)
            else:
                polygon.crs = self.crs
                polygon.to_file(shape_polygon)

    def clip_raster(self, polygon, in_raster, out_raster):
        """ Clips a raster based on the given polygon
            :param polygon: string, file with path of the polygon (*.shp)
            :param in_raster: string, file and path of the input raster (*.tif)
            :param in_raster: string, file and path of the output raster (*.tif)
            :return: no output, saves the raster (*.tif) with the selected filename
        """

        gdal.Warp(out_raster, in_raster, cutlineDSName=polygon)


class MapArray:
    def __init__(self, raster):
        self.raster = raster

        with rio.open(self.raster) as src:
            raster_np = src.read(1, masked=True)
            self.nodatavalue = src.nodata  # storing nodatavalue of raster
            self.meta = src.meta.copy()
        self.array = raster_np

    def nb_classes(self, n_classes):
        """ Class bins based on the Natural Breaks method
            :param n_classes: integer, number of classes
            :return: list, optimized bins
        """
        # Classification based on Natural Breaks
        breaks = mc.NaturalBreaks(self.array.ravel(), k=n_classes + 1)
        print('The bins were optimized to:', breaks.bins)
        class_bins = breaks.bins.tolist()
        return class_bins

    # todo:
    # def equal_intervals(self, n_classes):

    def categorize_raster(self, class_bins, map_out, save_ascii=True):
        """ Classifies the raster according to the classification bins
        :param project_dir: path of the project directory
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
            with rio.open(map_out, 'w', **self.meta) as outf:
                outf.write(raster_ma_fi.astype(rio.float64), 1)
        else:
            raise TypeError("Error filling NoDataValue to raster file")

        if save_ascii:
            map_asc = str(Path(map_out[0:-4] + '.asc'))
            gdal.Translate(map_asc, map_out, format='AAIGrid')
