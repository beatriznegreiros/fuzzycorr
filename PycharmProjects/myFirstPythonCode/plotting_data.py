import numpy as np
import sys
import matplotlib.pyplot as plt
from numpy import genfromtxt


# Importing raw data of map A (experimental data) as numpy array
map_A = genfromtxt('hexagon_experiment.csv', delimiter=',', skip_header=1)
lon_A, lat_A, dz_A = map_A[:, 0], map_A[:, 1], map_A[:, 2]

# Importing raw data from map B (simulation data) as np array
map_B = genfromtxt('hexagon_simulation.csv', delimiter=',', skip_header=1)
lon_B, lat_B, dz_B = map_B[:, 0], map_B[:, 1], map_B[:, 2]

# Printing a general overlook of the map A
plt.scatter(lon_A, lat_A, s=15, c=dz_A, marker="s", cmap='Spectral')
plt.title('Erosion/Deposition Patterns after experiment')
outputfp = "plot_mapA.png"
plt.savefig(outputfp, dpi=600)

plt.clf()

# Printing a general overlook of the map B
plt.scatter(lon_B, lat_B, s=15, c=dz_B, marker="s", cmap='Spectral')
plt.title('Erosion/Deposition Patterns after simulation')
outputfp = "plot_mapB.png"
plt.savefig(outputfp, dpi=600)

plt.clf()

plt.hist(dz_B, bins= 30)
outputfp = "hist_mapB.png"
plt.title('Histogram of map B')
plt.xlabel('Delta z')
plt.ylabel('Frequencies')
plt.savefig(outputfp, dpi=600)

plt.clf()

plt.hist(dz_A, bins= 30)
outputfp = "hist_mapA.png"
plt.title('Histogram of map A')
plt.xlabel('Delta z')
plt.ylabel('Frequencies')
plt.savefig(outputfp, dpi=600)

dz_total = np.concatenate((dz_A, dz_B), axis=0)

plt.clf()

plt.hist(dz_total, bins= 30)
outputfp = "hist_total.png"
plt.title('Histogram of maps A and B')
plt.xlabel('Delta z')
plt.ylabel('Frequencies')
plt.savefig(outputfp, dpi=600)