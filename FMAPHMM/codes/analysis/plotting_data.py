import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt


# Input data
path_A = r"C:/Users/beatr/PycharmProjects/FKAPHMM/raw_data/hexagon_experiment.csv"
path_B = r"C:/Users/beatr/PycharmProjects/FKAPHMM/raw_data/hexagon_simulation.csv"


# Importing raw data of map A (experimental data) as numpy array
map_A = genfromtxt(path_A, delimiter=',', skip_header=1)
lon_A, lat_A, dz_A = map_A[:, 0], map_A[:, 1], map_A[:, 2]


# Importing raw data from map B (simulation data) as np array
map_B = genfromtxt(path_B, delimiter=',', skip_header=1)
lon_B, lat_B, dz_B = map_B[:, 0], map_B[:, 1], map_B[:, 2]


# Printing general overlook of the map A and B
plt.scatter(lon_A, lat_A, s=15, c=dz_A, marker="s", cmap='Spectral')
plt.title('Erosion/Deposition Patterns after experiment')
outputfp = r"C:/Users/beatr/PycharmProjects/FKAPHMM/analysis/plot_mapA.png"
plt.savefig(outputfp, dpi=600)
plt.clf()


plt.scatter(lon_B, lat_B, s=15, c=dz_B, marker="s", cmap='Spectral')
plt.title('Erosion/Deposition Patterns after simulation')
outputfp = r"C:/Users/beatr/PycharmProjects/FKAPHMM/analysis/plot_mapB.png"
plt.savefig(outputfp, dpi=600)
plt.clf()

# Printing histograms of the map A and B
plt.hist(dz_A, bins= 30)
outputfp = r"C:/Users/beatr/PycharmProjects/FKAPHMM/analysis/hist_mapA.png"
plt.title('Histogram of map A')
plt.xlabel('Delta z')
plt.ylabel('Frequencies')
plt.savefig(outputfp, dpi=600)
plt.clf()


plt.hist(dz_B, bins= 30)
outputfp = r"C:/Users/beatr/PycharmProjects/FKAPHMM/analysis/hist_mapB.png"
plt.title('Histogram of map B')
plt.xlabel('Delta z')
plt.ylabel('Frequencies')
plt.savefig(outputfp, dpi=600)
plt.clf()


dz_total = np.concatenate((dz_A, dz_B), axis=0)
plt.hist(dz_total, bins= 30)
outputfp = r"C:/Users/beatr/PycharmProjects/FKAPHMM/analysis/hist_total.png"
plt.title('Histogram of maps A and B')
plt.xlabel('Delta z')
plt.ylabel('Frequencies')
plt.savefig(outputfp, dpi=600)