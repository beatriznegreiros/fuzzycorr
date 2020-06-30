import gdal
from pathlib import Path

dir = Path.cwd()

map_in = str(dir / "rasters") + "/" + "diamond_map_A_res01_norm" + ".tif"
map_asc = str(dir / "rasters") + "/" + "diamond_map_A_res01_norm" + ".asc"
gdal.Translate(map_in, map_asc, format='AAIGrid')

map_in = str(dir / "rasters") + "/" + "diamond_map_B_res01_norm" + ".tif"
map_asc = str(dir / "rasters") + "/" + "diamond_map_B_res01_norm" + ".asc"
gdal.Translate(map_in, map_asc, format='AAIGrid')