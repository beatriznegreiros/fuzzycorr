import plotter
from pathlib import Path

current_dir = Path.cwd()
rast_path = str(current_dir) + '/rasters/' + 'vali_hydro_FT_manual_2013_clipped.tif'
rasterfuzzy = plotter.RasterDataPlotter(rast_path)

path_fig = str(current_dir) + '/results/' + 'vali_hydro_FT_manual_2013_clipped.jpg'

# Bounds for categories
bounds = [-3, -2.5, -2, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

list_colors = ['darkred', 'sienna', 'chocolate', 'sandybrown', 'gold', 'yellow',
               'greenyellow', 'lime', 'lightseagreen', 'deepskyblue', 'royalblue', 'navy']
rasterfuzzy.plot_raster(path_fig, bounds, list_colors)

