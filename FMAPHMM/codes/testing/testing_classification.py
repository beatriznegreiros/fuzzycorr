import rasterio as rio
from rasterio.plot import plotting_extent
from pathlib import Path
import numpy as np
import sys
import earthpy as et
import earthpy.plot as ep
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import cm
import traceback


# INPUT: d84 as parameter
d = 0.013  # in cm

current_dir = Path.cwd().parent.parent
map_A_path = str(current_dir / "rasters/map_A.tif")
map_B_path = str(current_dir / "rasters/map_B.tif")

with rio.open(map_A_path) as src:
    raster_A = src.read(1, masked=True)
    spatial_extent = plotting_extent(src)
    msk_A = src.read_masks(1)  # reading map's mask
    nodatavalue = src.nodata  # storing nodatavalue of raster
    meta = src.meta.copy()

# Overview of the raster's histogram
ep.hist(raster_A.ravel(), bins=50, title="Distribution of raster cells in map A (experiment)",
        xlabel="Delta z", ylabel="Number of Pixels")
fig = str(current_dir / "analysis/hist_rasterA.png")
plt.savefig(fig, dpi=600)
plt.clf()

# Bins to classify the data Legend: HE (High Erosion), HIE (High Intermediate Erosion), IE (Intermediate Erosion),
# LIE (Low Intermediate Erosion), LE (Low Erosion), Static,  LD (Low Deposition), LID (Low Intermediate Deposition),
# ID (Intermediate Deposition), HID (High Intermediate Deposition), HD (High Deposition).
class_bins = [-100*d, -20 * d, -10 * d, -5 * d, -2 * d, -0.5 * d, 0.5 * d, 2 * d, 5 * d, 10 * d, 20 * d, np.iinfo(np.int32).max]

# Classify the original image array, then unravel it again for plotting
raster_A_class = np.digitize(raster_A, class_bins)

raster_A_ma = np.ma.masked_where(raster_A_class == 0.0,
                                 raster_A_class,
                                 copy=True)

print(np.unique(raster_A_ma))
ep.hist(raster_A_ma.ravel())
fig = str(current_dir / "analysis/hist_rasterA_classified.png")
plt.savefig(fig, dpi=600)
plt.clf()

# Create a colormap from a list of colors
colors = ['darkred', 'red', 'orangered', 'tomato', 'lightsalmon', 'linen', 'lightskyblue', 'deepskyblue', 'dodgerblue',
          'blue', 'darkblue']

cmap = ListedColormap(colors)
norm = BoundaryNorm(class_bins, len(colors))
ep.plot_bands(raster_A_ma,
              cmap=cmap,
              title="Classified Raster from Experimental Model (Map A)",
              scale=False,
              norm=norm)
plt.show()

raster_A_ma_fi = np.ma.filled(raster_A_ma, fill_value=nodatavalue)

if raster_A_ma_fi.min() == nodatavalue:
    out_path = str(current_dir / "rasters/map_A_classified.tif")
    with rio.open(out_path, 'w', **meta) as outf:
        outf.write(raster_A_ma_fi.astype(rio.float32), 1)
else:
    raise TypeError("NoDataValue Error")