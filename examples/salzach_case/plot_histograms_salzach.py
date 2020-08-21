import plotter
from pathlib import Path

current_dir = Path.cwd()

# Input data

'''list_rasters = ['vali_Hydro_FT-2D_MAP_2013_clipped',
                'vali_aPC_MAP_2013_clipped',
                'vali_meas_2013_clipped',
                'vali_hydro_FT_manual_2013_clipped']'''

list_rasters = ['vali_Hydro_FT-2D_MAP_2013',
                'vali_aPC_MAP_2013',
                'vali_meas_2013',
                'vali_hydro_FT_manual_2013']


for raster in list_rasters:
    path_raster = str(current_dir) + '/raw_data/' + raster + '.csv'
    histA = plotter.DataPlotter(path_raster)
    outA = str(current_dir) + '/analysis/' + 'hist_rawdata_' + raster + '.png'
    histA.make_hist('Bed level change [m]', 'Frequencies', outputpath=outA)
