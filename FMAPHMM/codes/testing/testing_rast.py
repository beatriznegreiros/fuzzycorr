from osgeo import gdal, osr
import numpy as np

def save_raster(path, band_count, bands, srs, gt, format='GTiff', dtype = gdal.GDT_Float32):
    cols,rows = bands.shape
    # Initialize driver & create file
    driver = gdal.GetDriverByName(format)
    dataset_out = driver.Create(path, cols, rows, 1, dtype)
    dataset_out.SetGeoTransform(gt)
    dataset_out.SetProjection(srs)
    # Write file to disk
    dataset_out.GetRasterBand(1).WriteArray(bands)
    dataset_out = None

epsg = 4326

gt = [0,1,0,0,0,-1]

srs = osr.SpatialReference()
srs.ImportFromEPSG(epsg)
srs = srs.ExportToWkt()

destination = 'C:/Users/beatr/PycharmProjects/myFirstPythonCode/raster_Map_A.tif'

array = np.arange(0, 25).reshape(5,5)

save_raster(destination,1,array,srs,gt)