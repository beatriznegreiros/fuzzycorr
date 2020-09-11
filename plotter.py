import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from pathlib import Path
import rasterio as rio
import earthpy.plot as ep
import matplotlib.patches as patches
from matplotlib import colors
import matplotlib
import matplotlib.transforms


class RasterDataPlotter:
    def __init__(self, path):
        self.path = path

    def read_raster(self):
        with rio.open(self.path) as src:
            raster_np = src.read(1, masked=True)
        return raster_np

    def make_hist(self, legendx, legendy, fontsize, outputpath, figsize, set_ylim=None, set_xlim=None):

        plt.rcParams.update({'font.size': fontsize})
        raster_np = self.read_raster()
        fig, ax = plt.subplots(figsize=figsize)
        ax.hist(raster_np[~raster_np.mask], bins=60)

        if set_ylim is not None:
            ax.set_ylim(set_ylim)
        if set_xlim is not None:
            ax.set_xlim(set_xlim)

        np.savetxt('trial.csv', raster_np[~raster_np.mask], delimiter=',')
        plt.xlabel(legendx)
        plt.ylabel(legendy)
        # plt.title(title)
        plt.grid(True)
        plt.subplots_adjust(left=0.17, bottom=0.15)
        plt.savefig(outputpath, dpi=600)
        plt.clf()

    def plot_raster_w_window(self, save_name, bounds, xy, width, height, list_colors=None, cmap=None):
        #xy: lower left corner from the lower left corner of the picture
        raster_np = self.read_raster()
        print('Raster has size: ', raster_np.shape)
        fig, ax = plt.subplots(1, 2, figsize=(10, 8))
        fig.tight_layout()

        if cmap is None and list_colors is not None:
            cmap = matplotlib.colors.ListedColormap(list_colors)

        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        ax[0].imshow(raster_np, cmap=cmap, norm=norm)
        rectangle = patches.Rectangle(xy, width, height, fill=False)
        ax[0].add_patch(rectangle)
        plt.setp(ax, xticks=[], yticks=[])

        #  Plot Patch
        box_np = raster_np[xy[1]: xy[1] + height, xy[0]: xy[0] + width]
        im = ax[1].imshow(box_np, cmap=cmap, norm=norm)
        ax[1].axis('off')
        cbar = ep.colorbar(im, pad=0.3, size='5%')
        cbar.ax.tick_params(labelsize=20)
        fig.savefig(save_name, dpi=800, bbox_inches='tight')

    def plot_raster(self, save_name, bounds, list_colors=None, cmap=None):
        raster_np = self.read_raster()
        fig1, ax1 = plt.subplots(figsize=(6, 8), frameon=False)

        if cmap is None and list_colors is not None:
            cmap = matplotlib.colors.ListedColormap(list_colors)

        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        im1 = ax1.imshow(raster_np, cmap=cmap, norm=norm)
        fig1.tight_layout()
        #plt.setp(ax1, xticks=[], yticks=[])
        #ax1.axis('off')

        cbar = ep.colorbar(im1, pad=0.3, size='5%')
        cbar.ax.tick_params(labelsize=20)
        fig1.savefig(save_name, dpi=600, bbox_inches='tight')

    def plot_continuous_raster(self, save_name, cmap, vmax, vmin):
        raster_np = self.read_raster()
        fig1, ax1 = plt.subplots(figsize=(6, 8), frameon=False)
        #norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        im1 = ax1.imshow(raster_np, cmap=cmap, vmax=vmax, vmin=vmin)
        fig1.tight_layout()
        plt.setp(ax1, xticks=[], yticks=[])
        cbar = ep.colorbar(im1, pad=0.3, size='5%')
        cbar.ax.tick_params(labelsize=15)
        ax1.axis('off')
        fig1.savefig(save_name, dpi=600, bbox_inches='tight')

    def plot_categorical_raster(self, save_name, legend, xy, width, height):
        raster_np = self.read_raster()
        print('Raster has size: ', raster_np.shape)
        fig, ax = plt.subplots(1, 2, figsize=(10, 8))
        im = ax[0].imshow(raster_np)
        fig.tight_layout()
        rectangle = patches.Rectangle(xy, width, height, fill=False)
        ax[0].add_patch(rectangle)
        plt.setp(ax, xticks=[], yticks=[])

        #  Plot Patch
        box_np = raster_np[xy[1]: xy[1] + height, xy[0]: xy[0] + width]
        im = ax[1].imshow(box_np)
        #ax[1].axis('off')
        ep.draw_legend(im, titles=legend)
        fig.savefig(save_name, dpi=800, bbox_inches='tight')


class DataPlotter:
    def __init__(self, path_textfile):
        self.textfile = path_textfile

    def make_hist(self, legendx, legendy, outputpath):
        file = genfromtxt(self.textfile, delimiter=',', skip_header=1)
        lon, lat, attribute = file[:, 0], file[:, 1], file[:, 2]

        # Printing histograms of the map
        _ = plt.hist(attribute, bins=50, density=True)
        #plt.title()
        plt.grid(True)
        plt.xlabel(legendx)
        plt.ylabel(legendy)
        plt.savefig(outputpath, dpi=600)
        plt.clf()

