try:
    import matplotlib.pyplot as plt
    import mapoperator as mo
    from pathlib import Path
    import numpy as np
    import gdal
except:
    print('ModuleNotFoundError: Missing fundamental packages (required: pathlib, numpy, gdal).')

# ---------------------INPUT------------------------------------------
#d = 0.00013  # in m d90
n_classes = 6

# Measured Data:
raster_A = "diamond_exp_01_norm"

# Simulated Data:
raster_B = "diamond_sim_01_norm"

# Selected output names for the classified rasters
name_A = "diamond_exp_01_class"
name_B = "diamond_sim_01_class"
# --------------------------------------------------------------------

dir = Path.cwd()
Path(dir / "rasters").mkdir(exist_ok=True)

if '.' not in raster_A[-4:]:
    raster_A += '.tif'
map_A_in = str(dir / "rasters") + "/" + raster_A

if '.' not in raster_B[-4:]:
    raster_B += '.tif'
map_B_in = str(dir / "rasters/") + "/" + raster_B

# Import raster as np array
array_A = mo.MapArray(map_A_in)
array_B = mo.MapArray(map_B_in)

# Classify the array and save the output file as .tif raster
nb_classes = array_A.nb_classes(n_classes)  # Extract the optimized intervals for the map A

array_A.categorize_raster(nb_classes, map_out=str(dir/'rasters') + '/' + name_A + '.tif')
array_B.categorize_raster(nb_classes, map_out=str(dir/'rasters') + '/' + name_B + '.tif')

'''# Plot the histogram of maps and the breaks division
#  Map of Measured values
classes = [0.03175, 0.04222, 0.04967, 0.05717, 0.06744]
plt.vlines(np.array(classes), 0, 350, linestyles='solid')
plt.hist(array_A.array[~array_A.array.mask], bins=50)
plt.title('Histogram: Rasterized hexagon-shaped')
plt.xlabel('Measured bed level change [m]')
plt.ylabel('Frequencies')
outputfile = str(dir / "results/hist_hexagon_rasterized_meas.png")
plt.savefig(outputfile, dpi=600)
plt.clf()

#  Map of simulated values
#plt.vlines(np.array(nb_classes[1:-1]), 0, 120, linestyles='solid')
plt.hist(array_B.array[~array_B.array.mask], bins=50)
plt.title('Histogram: Rasterized hexagon-shaped')
plt.xlabel('Simulated bed level change [m]')
plt.ylabel('Frequencies')
outputfile = str(dir / "results/hist_hexagon_rasterized_sim.png")
plt.savefig(outputfile, dpi=600)'''


