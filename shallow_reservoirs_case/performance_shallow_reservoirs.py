from pathlib import Path
import plotter

list_files = ['diamond_comp',
              'hexagon_comp']

list_titles = ['Diamond-shaped model',
               'Hexagon-shaped model']

legendx = 'Fuzzy Similarity [-]'
legendy = 'Frequency'

current_dir = Path.cwd()
i = 0

for file in list_files:
    path_raster = str(current_dir / 'rasters') + '/' + file + '.asc'
    outputpath = str(current_dir / 'analysis') + '/' + 'hist_' + file + '.png'
    raster = plotter.RasterDataPlotter(file, path_raster)
    raster.make_hist(legendx, legendy, list_titles[i], fontsize=17, outputpath=outputpath)
    i += 1
