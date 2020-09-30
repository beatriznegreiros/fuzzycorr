import gdal
from pathlib import Path

list_rasters = ['hexagon_sim_01_class_clipped',
                'hexagon_exp_01_class_clipped',
                'diamond_sim_01_class_clipped',
                'diamond_exp_01_class_clipped']
dir = Path.cwd()

for raster in list_rasters:
    raster_file = str(dir / 'rasters') + '/' + str(raster) + '.tif'
    map_asc = str(dir / 'rasters') + '/' + str(raster) + '.asc'
    gdal.Translate(map_asc, raster_file, format='AAIGrid')
