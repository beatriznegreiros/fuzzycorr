import prepro as mo
from pathlib import Path
import pandas as pd

#list_maps = ['diamond_exp_01_class', 'diamond_sim_01_class']
list_maps = ['hexagon_exp_01_class', 'hexagon_sim_01_class']

dir = Path.cwd()
#polygon_path = str(dir / 'shapefiles') + '/polygon_diamond.shp'
polygon_path = str(dir / 'shapefiles') + '/polygon_hexagon.shp'

for item in list_maps:
    path_map_in = str(dir /'rasters') + '/' + item + '.tif'
    path_map_out = str(dir / 'rasters') + '/' + item + '_clipped.tif'
    mo.clip_raster(polygon_path, path_map_in, path_map_out)
