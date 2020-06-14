import skspatial as sk
import mapoperator as mo
import geopandas as gpd
from pathlib import Path

# ----------------------INPUT---------------------------------
current_dir = Path.cwd().parent.parent

path_A = str(current_dir / "raw_data/hexagon_experiment.csv")
path_B = str(current_dir / "raw_data/hexagon_simulation.csv")

name_map_A = "map_A_testing"
name_map_B = "map_B_testing"

res = 0.2
# ------------------------------------------------------------

# code
shape_A = str(current_dir / "shapefiles") + "/" + name_map_A + ".shp"
shape_B = str(current_dir / "shapefiles") + "/" + name_map_B + ".shp"

raster_A = str(current_dir / "rasters") + "/" + name_map_A + ".tif"
raster_B = str(current_dir / "rasters") + "/" + name_map_B + ".tif"

mo.data_to_shape(path_A, shape_A)
mo.data_to_shape(path_B, shape_B)

gdf = gpd.read_file(shape_A)
ml_A = sk.interp2d(gdf, 'attribute', res=res)
array = ml_A.interpolate_2D(method='linear')
ml_A.write_raster(array, raster_A)

gdf = gpd.read_file(shape_B)
ml_B = sk.interp2d(gdf, 'attribute', res=res)
array = ml_B.interpolate_2D(method='linear')
ml_B.write_raster(array, raster_B)


