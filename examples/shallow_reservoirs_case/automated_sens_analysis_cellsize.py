from pathlib import Path
import prepro as mo
import fuzzycomp as fuzz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dir = Path.cwd()

#  Raster input
data_to_compare = ['diamond_experiment', 'diamond_simulation']
attribute = 'dz'
crs = 'EPSG:4326'
nodatavalue = -9999
interpol_method = 'linear'

# Comparison steup

abs_n = 0.4
abs_hd = 0.2


for res in np.array([0.05, 0.1, 0.2]):
    for data_item in data_to_compare:
        print('performingg')
        raw_data = str(dir / 'raw_data') + '/' + data_item + '.csv'
        _map = mo.PreProFuzzy(pd.read_csv(raw_data, skip_blank_lines=True), attribute=attribute, crs=crs,
                              nodatavalue=nodatavalue, res=res)
        _array = _map.norm_array(method=interpol_method)
        raster_path = str(dir / "rasters") + "/automated_sens_analysis_cellsize/" + data_item + ".tif"
        _map.array2raster(_array, raster_path)
        clipped_raster = str(dir / "rasters") + '/automated_sens_analysis_cellsize/' + data_item + "_clipped.tif"
        path_poly = str(dir / "shapefiles") + "/" + 'polygon_diamond' + ".shp"
        _map.clip_raster(path_poly, raster_path, clipped_raster)
    n = int(abs_n/res)
    hd = int(abs_hd/res)
    map_A_in = str(dir / "rasters") + '/automated_sens_analysis_cellsize/' + "diamond_experiment_clipped.tif"
    map_B_in = str(dir / "rasters") + '/automated_sens_analysis_cellsize/' + "diamond_simulation_clipped.tif"
    compareAB = fuzz.FuzzyComparison(map_A_in, map_B_in, n, hd)
    comparison_name = 'diamond_fuzzynumerical_res'
    save_dir = str(dir / "results") + '/automated_sens_analysis_cellsize/'
    global_simil = compareAB.fuzzy_numerical(comparison_name, save_dir=save_dir, map_of_comparison=False)
    _ = plt.plot(global_simil, res, markersize=12)
    print('performing')
    plt.show()
plt.xlabel(xlabel='Cell size [m]')
plt.ylabel(ylabel='Sfuzzy [-]')
#plt.show()





