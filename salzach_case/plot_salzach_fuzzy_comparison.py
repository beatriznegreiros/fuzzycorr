import plotter
from pathlib import Path

current_dir = Path.cwd()
rast_path = str(current_dir) + '/results/' + 'vali_hydrostoch_meas_simil_n8hd4.tif'
rasterfuzzy = plotter.RasterDataPlotter(rast_path)

path_fig = str(current_dir) + '/results/' + 'vali_hydrostoch_meas_simil_n8hd4.jpg'
rasterfuzzy.plot_raster(path_fig)
