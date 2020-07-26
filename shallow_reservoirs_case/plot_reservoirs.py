import plotter
from pathlib import Path
from matplotlib import cm

current_dir = Path.cwd()

list_rasters = ['diamond_exp_01_norm',
                'diamond_sim_01_norm',
                'hexagon_exp_01_norm',
                'hexagon_sim_01_norm']

# Bounds for categories
#bounds = [-3, -2.5, -2, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
#list_colors = ['darkred', 'sienna', 'chocolate', 'sandybrown', 'gold', 'yellow',
#'greenyellow', 'lime', 'lightseagreen', 'deepskyblue', 'royalblue', 'navy']

cmap = 'jet'

for item in list_rasters:
    rast_path = str(current_dir) + '/rasters/' + item + '.tif'
    raster = plotter.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/rasters/' + item + '_plot.png'
    raster.plot_continuous_raster(path_fig, cmap=cmap, vmax=0.1, vmin=0)

'''list_comparisons = ['vali_surrogate_meas_fuzzynum_n8hd4',
                    'vali_hydrostoch_meas_fuzzynum_n8hd4',
                    'vali_hydroman_meas_fuzzynum_n8hd4']

bounds = [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
cmap = cm.get_cmap('viridis', 7)

for item in list_comparisons:
    rast_path = str(current_dir) + '/results/fuzzy_numerical/' + item + '.tif'
    rasterfuzzy = plotter.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/results/figures/' + item + '_2gether.png'
    rasterfuzzy.plot_raster_w_window(path_fig, bounds, cmap=cmap, xy=(0, 0), width=120, height=140)'''