from pathlib import Path
import plotter

list_files = ['diamond_fuzzynum_n4hd2',
              'hexagon_fuzzynum_n4hd2']

legendx = 'Fuzzy Similarity [-]'
legendy = 'Frequency'

current_dir = Path.cwd()

for file in list_files:
    path_raster = str(current_dir / 'results') + '/' + file + '.tif'
    outputpath = str(current_dir / 'analysis') + '/' + 'hist_' + file + '.png'
    raster = plotter.RasterDataPlotter(path_raster)
    raster.make_hist(legendx, legendy, fontsize=17, outputpath=outputpath, figsize=(6, 4), set_xlim=(0.35, 1), set_ylim=(0, 140))
