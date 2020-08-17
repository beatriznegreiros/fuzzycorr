import plotter
from pathlib import Path
from matplotlib import cm

current_dir = Path.cwd()
legendx = 'Fuzzy Similarity [-]'
legendy = 'Frequency'

'''list_rasters = ['vali_Hydro_FT-2D_MAP_2013_clipped',
                'vali_aPC_MAP_2013_clipped',
                'vali_meas_2013_clipped',
                'vali_hydro_FT_manual_2013_clipped']'''

'''list_rasters = ['vali_hydroman_meas_fuzzynum_n8hd4',
                'vali_hydrostoch_meas_fuzzynum_n8hd4',
                'vali_surrogate_meas_fuzzynum_n8hd4']'''

'''list_rasters = ['vali_Hydro_FT-2D_MAP_2013_clipped_class_nbreaks',
                'vali_aPC_MAP_2013_clipped_class_nbreaks',
                'vali_meas_2013_clipped_class_nbreaks',
                'vali_hydro_FT_manual_2013_clipped_class_nbreaks']'''

list_rasters = ['vali_hydroman_meas_fuzzykappa_n8hd4',
                'vali_hydrostoch_meas_fuzzykappa_n8hd4',
                'vali_surrogate_meas_fuzzykappa_n8hd4'
                ]



# Bounds for categories
# bounds = [-3, -2.5, -2, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
#bounds = [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
bounds = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
#list_colors = ['red', 'tomato', 'orange', 'yellow', 'greenyellow', 'lime']
list_colors = ['red', 'tomato', 'orange', 'yellow', 'greenyellow']
# list_colors = ['darkred', 'sienna', 'chocolate', 'sandybrown', 'gold', 'yellow', 'greenyellow', 'lime', 'lightseagreen', 'deepskyblue', 'royalblue', 'navy']
#legend = ['nodata', 'try1', 'try1', 'try1', 'try1', 'try1', 'try1', 'try1', 'try1', 'try1', 'try1', 'try1', 'try1']

'''for item in list_rasters:
    rast_path = str(current_dir) + '/rasters/' + item + '.tif'
    raster = plotter.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/rasters/' + item + '.png'
    raster.plot_categorical_raster(path_fig, legend, xy=(0, 0), width=120, height=140)'''


#bounds = [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
#list_colors = ['red', 'tomato', 'orange', 'yellow', 'greenyellow', 'lime']

#cmap = cm.get_cmap('inferno', 7)


for item in list_rasters:
    rast_path = str(current_dir) + '/results/fuzzykappa/' + item + '.asc'
    rasterfuzzy = plotter.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/results/figures/' + item + '_whole.png'
    rasterfuzzy.plot_raster(path_fig, bounds, list_colors=list_colors)

# xy=(290, 600), width=100, height=140
# xy=(560, 1086), width=120, height=140
