from pathlib import Path
import timeit
import fuzzynumerical as fz

# ------------------------INPUT--------------------------------------
# Neighborhood definition
n = 4  # 'radius' of neighborhood
halving_distance = 2
comparison_name = "Hydro_FT_vali_manual_simil"

# Create directory if not existent
current_dir = Path.cwd()
Path(current_dir / "rasters").mkdir(exist_ok=True)
map_A_in = str(current_dir / "rasters/dz_meas_2010-2013_norm.tif")
map_B_in = str(current_dir / "rasters/Hydro_FT-2D_manual_2013_norm.tif")
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
