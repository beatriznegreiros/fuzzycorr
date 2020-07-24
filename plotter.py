import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from pathlib import Path
import rasterio as rio
import earthpy.plot as ep
import matplotlib.patches as patches
from matplotlib import colors
import matplotlib


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
        # plt.title(title)
        plt.grid(True)
        plt.subplots_adjust(left=0.17, bottom=0.15)
        plt.savefig(outputpath, dpi=600)
        plt.clf()

    def plot_raster(self, save_name, bounds, list_colors, title=None):
        raster_np = self.read_raster()
        f, ax = plt.subplots(figsize=(10, 8))
        cmap = matplotlib.colors.ListedColormap(list_colors)
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        #divcolor = colors.TwoSlopeNorm(vcenter=0., vmax=1., vmin=-0.2)
        #im = ax.imshow(raster_np, cmap='Spectral', norm=divcolor)
        im = ax.imshow(raster_np, cmap=cmap, norm=norm)
        ep.colorbar(im, pad=0.3, size='5%')
        plt.title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        '''axins = zoomed_inset_axes(ax, 10, loc=1)  # zoom-factor: 2.5, location: upper-left
        axins.plot()
        x1, x2, y1, y2 = 0, 140, 0, 120  # specify the limits
        axins.set_xlim(x1, x2)  # apply the x-limits
        axins.set_ylim(y1, y2)  # apply the y-limits
        plt.yticks(visible=False)
        plt.xticks(visible=False)
        mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")'''
        rectangle = patches.Rectangle((100, 200), 120, 140, fill=False)
        ax.add_patch(rectangle)
        plt.savefig(save_name, dpi=600)
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
