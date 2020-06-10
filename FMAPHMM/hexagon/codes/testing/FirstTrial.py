import numpy as np
import sys
import matplotlib.pyplot as plt
from numpy import genfromtxt
import gdal
import osr

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

'''
# Check to see if all columns have the same length
if len(lon_A) == len(lat_A) and len(lat_A) == len(dz_A):
    print("OK: Data has same column size")
    len_A = len(lon_A)
else:
    print("WARNING: Data does not have same columns size")
    sys.exit()

# Take the maximum values of map A
xmin, ymin, xmax, ymax, zmin, zmax = lon_A.min(), lat_A.min(), lon_A.max(), lat_A.max(), dz_A.min(), dz_A.max()
print(xmin, ymin, xmax, ymax, zmin, zmax)

# Check to see if there is erosion or deposition in the data
if xmin >= 0:
    print("There is only Sedimentation patterns in the data")
    only_sed = True
if xmax <= 0:
    print("There is only Erosion patterns in the data")
    only_ero = True

# Number of columns and rows
n_cols = 1
i = 0
y_coord = []

while i <= len_A - 1:
    n_cols = np.count_nonzero(lon_A == lon_A[i])  # counts how many latitudes (rows) there is in each column
    y_coord.append(n_cols)  # stores number of latitudes (rows) counted for that column in a list
    i += n_cols  # jumps to the next longitude (columns)

y_coord = np.array(y_coord)  # transforms list 'cols' into a np array
max_rows = int(y_coord.max())  # counts the number of longitudes
max_cols = len(y_coord)

print('max number of rows is ', max_rows, 'max number of columns is ', max_cols)
print("The raster map will have: ", max_rows, "x", max_cols, "pixels (x versus y)")
print(y_coord)
print(type(max_cols), type(max_rows))

#  Reshaping lat, long and dz
yres = (ymax - ymin) / (max_rows - 1)
xres = (xmax - xmin) / (max_cols - 1)
print(xres, yres)
'''

'''
lat_A_rs = np.linspace(ymax, ymin, max_rows)  # resizing the latitude coord.
aux1 = np.zeros((max_rows, max_cols), dtype=float)
for i in range(max_cols):
    aux1[:, i] = lat_A_rs
lat_A_rs = aux1
print(lat_A_rs)

lon_A_rs = np.linspace(xmax, xmin, max_cols)  # resizing the longitude coord.
aux2 = np.zeros((max_rows, max_cols), dtype=float)
for i in range(max_rows):
    aux2[i, :] = lon_A_rs
lon_A_rs = aux2
print(lon_A_rs)

ydeviance = 0.001
xdeviance = 0.001
i = 0
aux3 = np.zeros((max_rows, max_cols), dtype=float)
for index_y, lat in np.ndenumerate(lat_A_rs):
    for index_x, lon in np.ndenumerate(lon_A_rs):
        if abs(float(lat_A[i]-lat)) < xdeviance and abs(float(lon_A[i]-lon)) < ydeviance:
            aux3[index_x, index_y] = dz_A[i]
        i += 1
print(aux3)
'''

'''#  Rasterization of Map A
geotransform = (xmin, xres, 0, ymax, 0, -yres)
driver = gdal.GetDriverByName('GTiff')
output_raster = driver.Create('C:/Users/beatr/PycharmProjects/myFirstPythonCode/raster_Map_A.tif', max_cols, max_rows,
                              1, gdal.GDT_Float32)  # Open the file
output_raster.SetGeoTransform(geotransform)  # Specify its coordinates

srs = osr.SpatialReference()  # Establish its coordinate encoding
srs.ImportFromEPSG(4326)  # This one specifies WGS84 lat long.
output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system

# to the file

output_raster.GetRasterBand(1).WriteArray(dz_A)  # Writes my array to raster bands

output_raster.FlushCache()  # write file to disk
'''
# Categories (7) which classify each cell according to their bed elevation change, i.e. sediment deficit/surplus
categories = {"Elevated Erosion": range(-35, -25),
              "Low Erosion": range(-15, -5),
              "Intermediate Erosion": range(-25, -15),
              "Static": range(-5, 5),
              "Low Deposition": range(5, 15),
              "Intermediate Deposition": range(15, 25),
              "Elevated Deposition": range(25, 35)}
