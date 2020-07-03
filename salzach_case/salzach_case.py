from pathlib import Path
import mapoperator as mo
import pandas as pd
import fuzzynumerical as fuzz

# ---------------Data Pre-processing---------------------------------
# ------------------------INPUT--------------------------------------
#  Raw data input path
data_A = 'vali_Hydro_FT-2D_MAP.csv'
data_B = 'vali_aPC_MAP.csv'
attribute = 'dz'

name_map_A = 'vali_Hydro_FT-2D_MAP'
name_map_B = 'vali_aPC_MAP'

# Polygon and raster of area of interest
polyname = 'polygon_salzach'

#  Raster Resolution: Change as appropriate
#  NOTE: Fuzzy Analysis has unique resolution
res = 10

# Projection
crs = 'EPSG:4326'
nodatavalue = -9999

# Corners of raster
ulc = (4571800, 5308230)
lrc = (4575200, 5302100)

# -----------------------------------------------------------------------

# Create directories if not existent
dir = Path.cwd()
Path(dir / 'shapefiles').mkdir(exist_ok=True)
Path(dir / 'rasters').mkdir(exist_ok=True)

if '.' not in data_A[-4:]:
    data_A += '.csv'
path_A = str(dir / 'raw_data') + '/' + data_A

if '.' not in data_B[-4]:
    data_A += '.csv'
path_B = str(dir / 'raw_data') + '/' + data_B

map_A = mo.SpatialField(name_map_A, pd.read_csv(path_A, skip_blank_lines=True), attribute=attribute, crs=crs,
                        project_dir=dir, nodatavalue=nodatavalue)
map_B = mo.SpatialField(name_map_B, pd.read_csv(path_B, skip_blank_lines=True), attribute=attribute, crs=crs,
                        project_dir=dir, nodatavalue=nodatavalue)

# Write rasters of interpolated values
map_A.norm_raster(res, ulc=ulc, lrc=lrc, method='linear')
map_B.norm_raster(res, ulc=ulc, lrc=lrc, method='linear')

# Save shape of point cloud
# map_A.shape()

# Create polygon of interest area for comparison
poly_path = str(dir / 'shapefiles') + '/' + polyname + '.shp'
clip_raster_A = str(dir / 'rasters') + '/' + name_map_A + '_clipped' + '.tif'
clip_raster_B = str(dir / 'rasters') + '/' + name_map_B + '_clipped' + '.tif'

map_A.create_polygon(poly_path, alpha=0.01)
map_A.clip_raster(poly_path, clip_raster_A)
map_B.clip_raster(poly_path, clip_raster_B)

# ---------------Fuzzy map comparison---------------------------------
# ------------------------INPUT--------------------------------------
# Neighborhood definition
'''n = 4  # 'radius' of neighborhood
halving_distance = 2
comparison_name = "Hydro_FT_2010-2013_manual_simil"

# Create directory if not existent
dir = Path.cwd()
Path(dir / "rasters").mkdir(exist_ok=True)
map_A_in = str(dir / "rasters/dz_meas_2010-2013_norm.tif")
map_B_in = str(dir / "rasters/Hydro_FT-2D_manual_2013_norm.tif")'''
# ------------------------------------------------------------------


# Perform fuzzy comparison
'''compareAB = fuzz.FuzzyComparison(map_A_in, map_B_in, dir, n, halving_distance)
global_simil = compareAB.fuzzy_numerical(comparison_name)

# Print global similarity
print('Average fuzzy similarity:', global_simil)'''
