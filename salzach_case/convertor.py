import gdal
from pathlib import Path

dir = Path.cwd()
map_asc = str(dir/'rasters') + '/vali_aPC_MAP_norm_clipped.asc'
map_in = str(dir/'rasters') + '/vali_aPC_MAP_norm_clipped.tif'

gdal.Translate(map_asc, map_in, format='AAIGrid')
