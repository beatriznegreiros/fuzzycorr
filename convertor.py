import gdal
from pathlib import Path

current_dir = Path.cwd()
list_of_files = ['cali_aPC_MAP_2010_clipped', 'cali_hydro_FT_manual_2010_clipped', 'cali_Hydro_FT-2D_MAP_2010_clipped',
                 'cali_meas_2010_clipped', 'vali_aPC_MAP_2013_clipped', 'vali_hydro_FT_manual_2013_clipped',
                 'vali_Hydro_FT-2D_MAP_2013_clipped',
                 'vali_meas_2013_clipped']

for file in list_of_files:
    map_asc = str(current_dir / 'rasters/res5_cubic') + '/' + file + '.asc'
    map_in = str(current_dir / 'rasters/res5_cubic') + '/' + file + '.tif'
    gdal.Translate(map_asc, map_in, format='AAIGrid')