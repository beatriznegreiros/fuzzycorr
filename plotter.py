import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from pathlib import Path
import rasterio as rio


class RasterDataPlotter:
    def __init__(self, file, path):
        self.file = file
        self.path = path

    def make_hist(self, legendx, legendy, title, fontsize, outputpath):
        plt.rcParams.update({'font.size': fontsize})
        with rio.open(self.path) as src:
            raster_np = src.read(1, masked=True)
        fig, ax = plt.subplots()
        ax.hist(raster_np[~raster_np.mask], bins=60)
        plt.xlabel(legendx)
        plt.ylabel(legendy)
        #plt.title(title)
        plt.grid(True)
        plt.subplots_adjust(left=0.17, bottom=0.15)
        plt.savefig(outputpath, dpi=600)
        plt.clf()


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

    outA = str(dir / "results/hist_diamond_raw_meas.png")
    outB = str(dir / "results/hist_diamond_raw_sim.png")

    histA.make_hist(outA)
    histB.make_hist(outB)
