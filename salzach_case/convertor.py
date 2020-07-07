import gdal
from pathlib import Path

dir = Path.cwd()
file = 'vali_meas_2013_res5_clipped'


map_asc = str(dir/'rasters') + '/' + file + '.asc'
map_in = str(dir/'rasters') + '/' + file + '.tif'
gdal.Translate(map_asc, map_in, format='AAIGrid')

