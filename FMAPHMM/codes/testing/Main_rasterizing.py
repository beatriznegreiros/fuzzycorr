try:
    import mapoperator as mo
    from pathlib import Path
    import pandas as pd
except:
    print('ExceptionERROR: Missing fundamental packages (required: pathlib, pandas).')

current_dir = Path.cwd().parent.parent

# --------------------------INPUT DATA--------------------------
# 1. Input:
#  1.1 Raw Data:
path_A = str(current_dir / "raw_data/diamond_experiment.csv")
path_B = str(current_dir / "raw_data/diamond_simulation.csv")

attribute = 'dz'

name_map_A = "diamond_map_A_res0.1"
name_map_B = "diamond_map_B_res0.1"

#  1.2 Raster Resolution: Change as appropriate
#  NOTE: Fuzzy Analysis has unique resolution
res = 0.1

# 2. Projection
crs = "EPSG:4326"
# -----------------------------------------------------------------------

path_data = path_A
if '.' not in path_data[-4:]:
    path_data += '.csv'
map_A = mo.SpatialField(name_map_A, pd.read_csv(path_data, skip_blank_lines=True), attribute=attribute, crs=crs)
map_A.norm_raster(nodatavalue=-9999, res=res)

path_data = path_B
if '.' not in path_data[-4:]:
    path_data += '.csv'
map_B = mo.SpatialField(name_map_B, pd.read_csv(path_data, skip_blank_lines=True), attribute=attribute, crs=crs)
map_B.norm_raster(nodatavalue=-9999, res=res)


