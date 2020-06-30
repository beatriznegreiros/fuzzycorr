import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from pathlib import Path


class DataPlotter:
    def __init__(self, path_textfile, hist_title, variable):
        self.textfile = path_textfile
        self.his_title = hist_title
        self.variable = variable

    def make_hist(self, outputfile):
        file = genfromtxt(self.textfile, delimiter=',', skip_header=1)
        lon, lat, attribute = file[:, 0], file[:, 1], file[:, 2]

        # Printing histograms of the map
        plt.hist(attribute, bins=50, density=True)
        plt.title(self.his_title)
        plt.xlabel(self.variable)
        plt.ylabel('Frequencies')
        plt.savefig(outputfile, dpi=600)
        plt.clf()


if __name__ == '__main__':

    dir = Path.cwd()

    # Input data
    path_A = r"C:/Users/beatr/valitools/raw_data/diamond_experiment.csv"
    path_B = r"C:/Users/beatr/valitools/raw_data/diamond_simulation.csv"

    histA = DataPlotter(path_A, 'Histogram: Diamond-shaped', 'Measured bed level change [cm]')
    histB = DataPlotter(path_B, 'Histogram: Diamond-shaped', 'Simulated bed level change [cm]')

    outA = str(dir/"results/hist_diamond_raw_meas.png")
    outB = str(dir/"results/hist_diamond_raw_sim.png")

    histA.make_hist(outA)
    histB.make_hist(outB)