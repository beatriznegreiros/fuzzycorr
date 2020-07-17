from pathlib import Path
import plotter

list_files = ['cali_apc_vs_mea_comp',
              'cali_hydroman_vs_mea_comp',
              'vali_apc_vs_mea_comp',
              'vali_hydroman_vs_mea_comp',
              'cali_apc_vs_hydroman_comp',
              'vali_apc_vs_hydroman_comp',
              'cali_apc_vs_meas_comp_test_neigh0']

list_titles = ['aPC surrogate model (Calibration)',
               'Manually calibrated model (Calibration)',
               'aPC surrogate model (Validation)',
               'Manually calibrated model (Validation)',
               'aPC surrogate against manually calibrated model (Calibration)',
               'aPC surrogate against manually calibrated model (Validation)',
               'aPC surrogate model (Calibration) crispy comparison']

legendx = 'Fuzzy Similarity [-]'
legendy = 'Frequency'

current_dir = Path.cwd()
i = 0
Path(current_dir / 'analysis').mkdir(exist_ok=True)

for file in list_files:
    path_raster = str(current_dir / 'rasters') + '/' + file + '.asc'
    outputpath = str(current_dir / 'analysis') + '/' + 'hist_' + file + '.png'
    raster = plotter.RasterDataPlotter(file, path_raster)
    raster.make_hist(legendx, legendy, list_titles[i], fontsize=15, outputpath=outputpath)
    i += 1
