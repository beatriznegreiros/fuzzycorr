try:
    import mapoperator as mo
    from pathlib import Path
except:
    print('ExceptionERROR: Missing fundamental packages (required: pathlib).')

current_dir = Path.cwd().parent.parent

# --------------------------INPUT DATA--------------------------
# 1. Input:
#  1.1 Raw Data:
path_A = str(current_dir / "raw_data/hexagon_experiment.csv")
path_B = str(current_dir / "raw_data/hexagon_simulation.csv")

name_map_A = "hexagon_map_A"
name_map_B = "hexagon_map_B"

#  1.2 Raster Resolution: Change as appropriate
#  NOTE: For the Fuzzy Analysis choose one unique resolution
x_res_A = 0.2
y_res_A = 0.2
x_res_B = 0.2
y_res_B = 0.2
# -----------------------------------------------------------------------

mo.data_to_raster(path_A, name_map_A, x_res_A, y_res_A)
mo.data_to_raster(path_B, name_map_B, x_res_B, y_res_B)

