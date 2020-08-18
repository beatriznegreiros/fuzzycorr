from pathlib import Path
import mapoperator as mo
import pandas as pd
import fuzzyevaluation as fuzz

# ---------------Data Pre-processing---------------------------------
# ------------------------INPUT--------------------------------------
#  Raw data input path
list_files = ['vali_aPC_MAP_2013',
              'vali_hydro_FT_manual_2013',
              'vali_Hydro_FT-2D_MAP_2013',
              'vali_meas_2013']

# Parameters
attribute = 'dz'
interpol_method = 'linear'

# Polygon of area of interest
polyname = 'polygon_salzach'

#  Raster Resolution: Change as appropriate
#  NOTE: Fuzzy Analysis has unique resolution
res = 20

# Projection
crs = 'EPSG:4326'
nodatavalue = -9999

# Corners of raster
ulc = (4571800, 5308230)
lrc = (4575200, 5302100)

# -----------------------------------------------------------------------

# Create directories if not existent
current_dir = Path.cwd()
Path(current_dir / 'shapefiles').mkdir(exist_ok=True)
Path(current_dir / 'rasters').mkdir(exist_ok=True)

poly_path = str(current_dir / 'shapefiles') + '/' + polyname + '.shp'

for file in list_files:
    # Path management
    path_file = str(current_dir / 'raw_data') + '/' + file + '.csv'
    name_file = file + '_res' + str(res)
    raster_file = str(current_dir / 'rasters') + '/' + file + '_res20.tif'

    # Instanciating object of SpatialField
    map_file = mo.SpatialField(name_file, pd.read_csv(path_file, skip_blank_lines=True), attribute=attribute, crs=crs, nodatavalue=nodatavalue, res=res, ulc=ulc, lrc=lrc)

    # Normalize points to a grid-ed array
    array_ = map_file.norm_array(method=interpol_method)

    # Write raster
    map_file.array2raster(array_, raster_file, save_ascii=False)

    # Clip raster
    clip_raster = str(current_dir / 'rasters') + '/' + file + '_res20_clipped' + '.tif'
    #  map_file.create_polygon(poly_path, alpha=0.01)
    map_file.clip_raster(poly_path, raster_file, clip_raster)
