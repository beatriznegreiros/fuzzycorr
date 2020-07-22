import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from pathlib import Path
import rasterio as rio
import earthpy.plot as ep
import matplotlib.patches as patches

class RasterDataPlotter:
    def __init__(self, path):
        self.path = path

    def read_raster(self):
        with rio.open(self.path) as src:
            raster_np = src.read(1, masked=True)
        return raster_np

    def make_hist(self, legendx, legendy, title, fontsize, outputpath):
        plt.rcParams.update({'font.size': fontsize})
        raster_np = self.read_raster()
        fig, ax = plt.subplots()
        ax.hist(raster_np[~raster_np.mask], bins=60)
        np.savetxt('trial.csv', raster_np[~raster_np.mask], delimiter=',')
        plt.xlabel(legendx)
        plt.ylabel(legendy)
        #plt.title(title)
        plt.grid(True)
        plt.subplots_adjust(left=0.17, bottom=0.15)
        plt.savefig(outputpath, dpi=600)
        plt.clf()

    def plot_raster(self, save_name, title=None):
        raster_np = self.read_raster()
        f, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(raster_np)
        ep.colorbar(im)
        plt.tight_layout()
        plt.title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        rectangle = patches.Rectangle((0, 0), 120, 140, fill=False)
        ax.add_patch(rectangle)
        f.savefig(save_name, dpi=600, orientation='portrait')
        plt.show()

    def plot_patch(self, xy, width, height, save_name):
        raster_np = self.read_raster()


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
