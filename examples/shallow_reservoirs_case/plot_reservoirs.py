import plotter
from pathlib import Path
from matplotlib import cm

current_dir = Path.cwd()

'''list_rasters = ['diamond_fuzzynum_n4hd2',
                'hexagon_fuzzynum_n4hd2']

# Bounds for categories
bounds = [0, 0.125, 0.250, 0.375, 0.5, 0.625, 0.75, 0.875, 1]

#cmap = 'jet'

list_colors = ['red', 'tomato', 'orange', 'gold', 'yellow', 'greenyellow', 'palegreen', 'lime']

for item in list_rasters:
    rast_path = str(current_dir) + '/results/' + item + '.tif'
    raster = plotter.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/results/' + item + '_plot.png'
    raster.plot_raster(path_fig, bounds, list_colors)'''


list_rasters = ['diamond_exp_01_norm_linear_clipped',
                'diamond_sim_01_norm_linear_clipped',
                'hexagon_exp_01_norm_linear_clipped',
                'hexagon_sim_01_norm_linear_clipped']

cmap = 'jet'

#list_colors = ['red', 'tomato', 'orange', 'gold', 'yellow', 'greenyellow', 'palegreen', 'lime']

vmax = 0.082
vmin = 0.006

for item in list_rasters:
    rast_path = str(current_dir) + '/rasters/' + item + '.tif'
    raster = plotter.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/rasters/' + item + '_plot_clipped.png'
    raster.plot_continuous_raster(path_fig, cmap, vmax, vmin, box='off')