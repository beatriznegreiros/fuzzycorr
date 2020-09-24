import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
import rasterio as rio
import earthpy.plot as ep
import matplotlib.patches as patches
from matplotlib import colors
import matplotlib
import matplotlib.transforms
import scipy.stats


class RasterDataPlotter:
    def __init__(self, path):
        self.path = path

    def read_raster(self):
        with rio.open(self.path) as src:
            raster_np = src.read(1, masked=True)
        return raster_np

    def make_hist(self, legendx, legendy, fontsize, output_file, figsize, set_ylim=None, set_xlim=None):
        """
        Create a histogram of numerical raster
        :param legendx: string, legend of the x axis of he histogram
        :param legendy: string, legend of the y axis of he histogram
        :param fontsize: integer, size of the font
        :param output_file: string, path for the output file
        :param figsize: tuple of integers, size of the width x height of the figure
        :param set_ylim: float, set the maximum limit of the y axis
        :param set_ylim: float, set the maximum limit of the x axis
        :output: saves the figure of the histogram
        """
        plt.rcParams.update({'font.size': fontsize})
        raster_np = self.read_raster()
        fig, ax = plt.subplots(figsize=figsize)
        _, bins, _ = ax.hist(raster_np[~raster_np.mask], bins=60)

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

        # Plot line with data mean (Sfuzzy)
        plt.axvline(raster_np.mean(), color='k', linestyle='dashed', linewidth=1)
        min_ylim, max_ylim = plt.ylim()
        plt.text(raster_np.mean() * 1.1, max_ylim * 0.9, 'Sfuzzy: {:.4f}'.format(raster_np.mean()))

        # Save fig
        plt.savefig(output_file, dpi=300)
        plt.clf()

    def plot_raster_w_window(self, output_file, xy, width, height, bounds, **kwargs):
        """
        Create a figure of a raster with a zoomed window
        :param output_file: path, file path of the figure
        :param xy: tuple (x,y), origin of the zoomed window, the upper left corner
        :param width: integer, width (number of cells) of the zoomed window
        :param height: integer, height (number of cells) of the zoomed window
        :param bounds: list of float, limits for each color of the colormap
        :kwarg cmap: string, colormap to plot the raster
        :kwarg list_colors: list of colors (str), as alternative to using a colormap
        :output: saves the figure of the raster
        """
        #xy: upper left corner from the lower left corner of the picture
        raster_np = self.read_raster()
        print('Raster has size: ', raster_np.shape)
        fig, ax = plt.subplots(1, 2, figsize=(10, 8))
        fig.tight_layout()

        # Creates a colormap based on the given list_colors, if the cmap is not given
        if kwargs['cmap'] is None and kwargs['list_colors'] is not None:
            cmap = matplotlib.colors.ListedColormap(kwargs['list_colors'])
        elif kwargs['cmap'] is not None:
            cmap = kwargs['cmap']
        else:
            print('Error: Insuficient number of arguments')

        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        ax[0].imshow(raster_np, cmap=cmap, norm=norm)
        rectangle = patches.Rectangle(xy, width, height, fill=False)
        ax[0].add_patch(rectangle)
        plt.setp(ax, xticks=[], yticks=[])

        #  Plot Patch
        box_np = raster_np[xy[1]: xy[1] + height, xy[0]: xy[0] + width]
        im = ax[1].imshow(box_np, cmap=cmap, norm=norm)
        #ax[1].axis('off')
        cbar = ep.colorbar(im, pad=0.3, size='5%')
        cbar.ax.tick_params(labelsize=20)

        fig.savefig(output_file, dpi=600, bbox_inches='tight')

    def plot_raster(self, output_file, bounds, list_colors=None, cmap=None):
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
        fig1.savefig(output_file, dpi=300, bbox_inches='tight')

    def plot_continuous_raster(self, output_file, cmap, vmax, vmin):
        raster_np = self.read_raster()
        fig1, ax1 = plt.subplots(figsize=(6, 8), frameon=False)
        #norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        im1 = ax1.imshow(raster_np, cmap=cmap, vmax=vmax, vmin=vmin)
        fig1.tight_layout()
        plt.setp(ax1, xticks=[], yticks=[])
        cbar = ep.colorbar(im1, pad=0.3, size='5%')
        cbar.ax.tick_params(labelsize=15)
        ax1.axis('off')
        fig1.savefig(output_file, dpi=300, bbox_inches='tight')

    def plot_categorical_raster(self, output_file, labels, cmap):
        raster_np = self.read_raster()
        print('Classes identified in the raster: ', np.unique(raster_np))
        #cmap = matplotlib.colors.ListedColormap(list_colors)
        fig, ax = plt.subplots()
        im = ax.imshow(raster_np, cmap=cmap)
        ep.draw_legend(im, titles=labels)
        ax.set_axis_off()
        plt.show()
        fig.savefig(output_file, dpi=700, bbox_inches='tight')

    def plot_categorical_w_window(self, output_file, labels, cmap, xy, width, height):
        raster_np = self.read_raster()
        print('Classes identified in the raster: ', np.unique(raster_np))
        #cmap = matplotlib.colors.ListedColormap(list_colors)
        fig, ax = plt.subplots(1, 2)

        ax[0].imshow(raster_np, cmap=cmap)
        rectangle = patches.Rectangle(xy, width, height, fill=False)
        ax[0].add_patch(rectangle)
        plt.setp(ax, xticks=[], yticks=[])

        #  Plot Patch
        box_np = raster_np[xy[1]: xy[1] + height, xy[0]: xy[0] + width]
        im = ax[1].imshow(box_np, cmap=cmap)
        # ax[1].axis('off')
        cbar = ep.draw_legend(im, titles=labels)
        #cbar.ax[].tick_params(labelsize=20)
        #ax.set_axis_off()
        fig.savefig(output_file, dpi=700, bbox_inches='tight')


class DataPlotter:
    def __init__(self, path_textfile):
        self.textfile = path_textfile

    def make_hist(self, legendx, legendy, output_file):
        file = genfromtxt(self.textfile, delimiter=',', skip_header=1)
        lon, lat, attribute = file[:, 0], file[:, 1], file[:, 2]

        # Printing histograms of the map
        _ = plt.hist(attribute, bins=50, density=True)
        #plt.title()
        plt.grid(True)
        plt.xlabel(legendx)
        plt.ylabel(legendy)
        plt.savefig(output_file, dpi=300)
        plt.clf()

