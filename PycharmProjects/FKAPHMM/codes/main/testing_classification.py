import rasterio as rio
from rasterio.plot import plotting_extent
from pathlib import Path
import numpy as np
import sys
import earthpy as et
import earthpy.plot as ep
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

# INPUT: d84 as parameter
d = 0.1

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

# Bins to classify the data
# Legend: LD (Low Deposition), LID (Low Intermediate Deposition), ID (Intermediate Deposition)
#         HID (High Intermediate Deposition), HD (High Deposition)
#            [      static    LD     LID    ID     HID      HD
class_bins = [raster_A.min(), 0.5 * d, 2 * d, 5 * d, 10 * d, 20 * d, 100 * d]
# another option: class_bins = [-2*d, 2*d, 5*d, 10*d, 20*d, 100*d, 200*d]

# Classify the original image array, then unravel it again for plotting
raster_A_class = np.digitize(raster_A, class_bins)
print(np.unique(raster_A_class))
ep.hist(raster_A_class.ravel())
fig = str(current_dir / "analysis/hist_rasterA_classified.png")
plt.savefig(fig, dpi=600)
plt.clf()

raster_A_class_ma = np.ma.masked_where(raster_A_class == 0,
                                       raster_A_class,
                                       copy=True)

# Create a colormap from a list of colors
colors = ['linen', 'lightgreen', 'darkgreen', 'maroon', 'darkblue']
cmap = ListedColormap(colors)
norm = BoundaryNorm(class_bins, len(colors))
ep.plot_bands(raster_A_class_ma,
              cmap=cmap,
              title="Classified Raster from Experimental Model (Map A)",
              scale=False,
              norm=norm)
plt.show()

raster_A_class_ma_fi = np.ma.filled(raster_A_class_ma, fill_value=nodatavalue)
print(raster_A_class_ma_fi.min(), nodatavalue)

out_path = str(current_dir / "rasters/map_A_classified.tif")
with rio.open(out_path, 'w', **meta) as outf:
    outf.write(raster_A_class_ma_fi.astype(rio.float32), 1)
