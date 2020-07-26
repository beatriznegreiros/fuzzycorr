import plotter
from pathlib import Path
from matplotlib import cm

current_dir = Path.cwd()

list_rasters = ['vali_Hydro_FT-2D_MAP_2013_clipped',
                'vali_aPC_MAP_2013_clipped',
                'vali_meas_2013_clipped',
                'vali_hydro_FT_manual_2013_clipped']

# Bounds for categories
bounds = [-3, -2.5, -2, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

list_colors = ['darkred', 'sienna', 'chocolate', 'sandybrown', 'gold', 'yellow',
 'greenyellow', 'lime', 'lightseagreen', 'deepskyblue', 'royalblue', 'navy']

for item in list_rasters:
    rast_path = str(current_dir) + '/rasters/' + item + '.tif'
    raster = plotter.RasterDataPlotter(rast_path)
    box_savename = str(current_dir) + '/rasters/' + item + '.jpg'
    path_fig = str(current_dir) + '/rasters/' + item + '_cut2.jpg'
    raster.plot_raster(path_fig, bounds, list_colors=list_colors, xy=(0, 0), width=120, height=140, box_name=box_savename)



'''list_comparisons = ['vali_surrogate_meas_fuzzynum_n8hd4',
                    'vali_hydrostoch_meas_fuzzynum_n8hd4',
                    'vali_hydroman_meas_fuzzynum_n8hd4']

bounds = [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
cmap = cm.get_cmap('viridis', 7)

for item in list_comparisons:
    rast_path = str(current_dir) + '/results/fuzzy_numerical/' + item + '.tif'
    rasterfuzzy = plotter.RasterDataPlotter(rast_path)
    box_savename = str(current_dir) + '/results/figures/' + item + '.jpg'
    path_fig = str(current_dir) + '/results/figures/' + item + '_cut2.jpg'
    rasterfuzzy.plot_comparison_raster(path_fig, bounds, cmap=cmap, xy=(0, 0), width=120, height=140, box_name=box_savename)'''
