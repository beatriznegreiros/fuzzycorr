import plotter
from pathlib import Path

current_dir = Path.cwd()
rast_path = str(current_dir/'salzach_case') + '/results/' + 'vali_hydroman_meas_simil_fuzzynum.tif'
rasterfuzzy = plotter.RasterDataPlotter(rast_path)

path_fig = str(current_dir/'salzach_case') + '/results/' + 'vali_hydroman_meas_simil_fuzzynum.jpg'
rasterfuzzy.plot_raster(path_fig)
