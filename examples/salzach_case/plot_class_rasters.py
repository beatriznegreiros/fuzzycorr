import plotter
from pathlib import Path
from matplotlib import cm

current_dir = Path.cwd()

list_rasters = ['vali_Hydro_FT-2D_MAP_2013_clipped_class_nbreaks',
                'vali_aPC_MAP_2013_clipped_class_nbreaks',
                'vali_meas_2013_clipped_class_nbreaks',
                'vali_hydro_FT_manual_2013_clipped_class_nbreaks']

# Bounds for categories
labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

#list_colors = ['greenyellow', 'lime', 'lightseagreen', 'deepskyblue', 'royalblue', 'navy']

cmap = cm.get_cmap('jet', 12)

for item in list_rasters:
    rast_path = str(current_dir) + '/rasters/' + item + '.tif'
    raster = plotter.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/rasters/' + item + '_plot_window.png'
    raster.plot_categorical_w_window(path_fig, labels, cmap=cmap, xy=(100, 200), width=170, height=270)
