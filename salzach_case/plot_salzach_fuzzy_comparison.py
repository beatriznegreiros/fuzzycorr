import plotter
from pathlib import Path

current_dir = Path.cwd()
rast_path = str(current_dir) + '/rasters/' + 'vali_aPC_MAP_2013_clipped.tif'
rasterfuzzy = plotter.RasterDataPlotter(rast_path)

path_fig = str(current_dir) + '/rasters/' + 'vali_aPC_MAP_2013_clipped.jpg'
rasterfuzzy.plot_raster(path_fig)
