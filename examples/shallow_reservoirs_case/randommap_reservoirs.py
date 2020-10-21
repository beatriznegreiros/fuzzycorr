import preprocessing as mo
from pathlib import Path
import pandas as pd
import fuzzycomp as fuzz

file = "diamond_experiment"

# Characteristics of the raster
attribute = 'dz'
res = 0.1

# Projection
crs = 'EPSG:4326'
nodatavalue = -9999


current_dir = Path.cwd()
Path(current_dir / 'shapefiles').mkdir(exist_ok=True)
Path(current_dir / 'rasters').mkdir(exist_ok=True)

# Create files path
path_file = str(current_dir / 'raw_data') + '/' + file + '.csv'
random_raster = str(current_dir / 'rasters') + '/' + file + '_01_random.tif'

# Instanciating object of SpatialField
map_file = mo.PreProFuzzy(pd.read_csv(path_file, skip_blank_lines=True), attribute=attribute, crs=crs,
                          nodatavalue=nodatavalue, res=res)

# Create random raster
map_file.random_raster(random_raster, minmax=None)

