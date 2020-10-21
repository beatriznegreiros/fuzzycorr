import visualization
from pathlib import Path
from matplotlib import cm

current_dir = Path.cwd()

list_rasters = ['hexagon_exp_01_class_clipped',
                'hexagon_sim_01_class_clipped',
                'diamond_exp_01_class_clipped',
                'diamond_sim_01_class_clipped']

# Bounds for categories
labels = ['Very Low Depositon', 'Low Deposition', 'Intermediate-low Deposition', 'Intermediate Deposition',
          'Intermediate-elevated Deposition', 'Elevated Deposition']

#list_colors = ['greenyellow', 'lime', 'lightseagreen', 'deepskyblue', 'royalblue', 'navy']

cmap = cm.get_cmap('jet', 6)

for item in list_rasters:
    rast_path = str(current_dir) + '/rasters/' + item + '.tif'
    raster = visualization.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/rasters/' + item + '_plot_clipped.png'
    raster.plot_categorical_raster(path_fig, labels, cmap=cmap)
