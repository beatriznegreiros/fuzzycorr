from pathlib import Path
import timeit
import fuzzynumerical as fz

# ------------------------INPUT--------------------------------------
# Neighborhood definition
n = 2  # 'radius' of neighborhood
halving_distance = 1
comparison_name = "diamond_comp"

# Create directory if not existent
current_dir = Path.cwd()
Path(current_dir / "rasters").mkdir(exist_ok=True)
map_A_in = str(current_dir / "rasters/diamond_sim_01_norm.tif")
map_B_in = str(current_dir / "rasters/diamond_exp_01_norm.tif")
# ------------------------------------------------------------------

# Start run time count
start = timeit.default_timer()

# Perform fuzzy comparison
compareAB = fz.FuzzyComparison(map_A_in, map_B_in, current_dir, n, halving_distance)
global_simil = compareAB.fuzzy_numerical(comparison_name)

# Print global similarity
print('Average fuzzy similarity:', global_simil)

# Stops run time count
stop = timeit.default_timer()

# Print run time:
print('Enlapsed time: ', stop - start, 's')
