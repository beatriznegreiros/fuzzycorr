from pathlib import Path
import timeit
import fuzzyevaluation as fuzz

# ------------------------INPUT--------------------------------------
# Neighborhood definition
n = 8  # 'radius' of neighborhood
halving_distance = 4
comparison_name = "vali_hydrostoch_meas_simil_n8hd4"

# Create directory if not existent
current_dir = Path.cwd()
Path(current_dir / "rasters").mkdir(exist_ok=True)
map_A_in = str(current_dir / "rasters/vali_meas_2013_clipped.tif")
map_B_in = str(current_dir / "rasters/vali_Hydro_FT-2D_MAP_2013_clipped.tif")
# ------------------------------------------------------------------

# Start run time count
start = timeit.default_timer()

# Perform fuzzy comparison
compareAB = fuzz.FuzzyComparison(map_A_in, map_B_in, current_dir, n, halving_distance)
global_simil = compareAB.fuzzy_numerical(comparison_name)

# Print global similarity
print('Average fuzzy similarity:', global_simil)

# Stops run time count
stop = timeit.default_timer()

# Print run time:
print('Enlapsed time: ', stop - start, 's')
