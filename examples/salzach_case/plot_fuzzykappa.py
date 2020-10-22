import plotter
from pathlib import Path
from matplotlib import cm

current_dir = Path.cwd()

list_rasters = ['vali_hydroman_meas_fuzzykappa',
                'vali_hydrostoch_meas_fuzzykappa',
                'vali_surrogate_meas_fuzzykappa',
                ]
vmax = 1.0
vmin = 0.0
cmap = 'inferno'

for item in list_rasters:
    rast_path = str(current_dir) + '/results/fuzzykappa/most_updated/' + item + '.asc'
    raster = plotter.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/results/fuzzykappa/most_updated/' + item + '_plot.png'
    raster.plot_continuous_raster(path_fig, vmax=vmax, vmin=vmin, cmap=cmap)
