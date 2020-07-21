from pathlib import Path
import timeit
import fuzzyrmse as fr

# ------------------------INPUT--------------------------------------
# Neighborhood definition
n = 2  # 'radius' of neighborhood
halving_distance = 1
comparison_name = "hexagon_comp_fuzzyrmse_testtospeedup"

# Create directory if not existent
current_dir = Path.cwd()
Path(current_dir / "rasters").mkdir(exist_ok=True)
map_A_in = str(current_dir / "rasters/hexagon_sim_01_norm.tif")
map_B_in = str(current_dir / "rasters/hexagon_exp_01_norm.tif")
# ------------------------------------------------------------------

# Start run time count
start = timeit.default_timer()

# Perform fuzzy comparison
compareAB = fr.FuzzyComparison(map_A_in, map_B_in, current_dir, n, halving_distance)
global_simil = compareAB.fuzzy_error(comparison_name)

# Print global similarity
print('Fuzzy error [-]:', global_simil)

# Stops run time count
stop = timeit.default_timer()

# Print run time:
print('Enlapsed time: ', stop - start, 's')
