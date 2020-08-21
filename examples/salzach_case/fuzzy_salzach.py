from pathlib import Path
import timeit
import fuzzyevaluation as fuzz

# ------------------------INPUT--------------------------------------
# Neighborhood definition
n = 2  # 'radius' of neighborhood
halving_distance = 1

# Output map and textfile
current_dir = Path.cwd()
Path(current_dir / "results/fuzzy_numerical").mkdir(exist_ok=True)  # create dir if not existent
save_dir = str(current_dir / "results/fuzzy_numerical/sensitivity_cellsize")

comparison_name = "vali_surrogate_meas_res20_n2hd1"  # filename for the results (.txt) and comparison map (
# .tif)

# Maps to compare
map_A_in = str(current_dir / "rasters/vali_aPC_MAP_2013_res20_clipped.tif")
map_B_in = str(current_dir / "rasters/vali_meas_2013_res20_clipped.tif")
# ------------------------------------------------------------------

# Start run time count
start = timeit.default_timer()

# Perform fuzzy comparison
compareAB = fuzz.FuzzyComparison(map_A_in, map_B_in, n, halving_distance)
global_simil = compareAB.fuzzy_numerical(comparison_name, save_dir=save_dir)

# Print global similarity
print('Average fuzzy similarity:', global_simil)

# Stops run time count
stop = timeit.default_timer()

# Print run time:
print('Enlapsed time: ', stop - start, 's')
