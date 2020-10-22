import preprocessing as pp
import pandas as pd
from pathlib import Path

# ------------------------INPUT--------------------------------------
#  Raw data input path
raw_data = "diamond_simulation.csv"
name_map = "diamond_sim_02_norm_linear"
attribute = 'dz'

#  Raster Resolution: Change as appropriate
#  NOTE: Fuzzy Analysis has unique resolution
res = 0.2

# Projection
crs = 'EPSG:4326'
nodatavalue = -9999
interpol_method = 'linear'

#  In case a polygon file is necessary
dir = Path.cwd()
path_poly = str(dir/ 'shapefiles') + '/polygon_diamond.shp'
# -----------------------------------------------------------------------

# Creates directories if not existent
Path(dir / "shapefiles").mkdir(exist_ok=True)
Path(dir / "rasters").mkdir(exist_ok=True)
if '.' not in raw_data[-4:]:
    raw_data += '.csv'
path_A = str(dir / "raw_data/") + "/" + raw_data

#  Instanciates object of the class
_map = pp.PreProFuzzy(pd.read_csv(path_A, skip_blank_lines=True), attribute=attribute, crs=crs,
                      nodatavalue=nodatavalue, res=res)

#  Creates a normalized and gridded array
_array = _map.norm_array(method=interpol_method)

#  Saves raster
raster_path = str(dir / "rasters") + "/" + name_map + ".tif"
_map.array2raster(_array, raster_path)

#  Creates polygon, clips and saves a raster with it
#_map.create_polygon(path_poly, alpha=0.15)
clipped_raster = str(dir / "rasters") + '/' + name_map + "_clipped.tif"
_map.clip_raster(path_poly, raster_path, clipped_raster)
