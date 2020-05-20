import gdal

fn = "C:/Users/beatr/PycharmProjects/myFirstPythonCode/plot_mapA.png"
ds = gdal.Open(fn)

band1 = ds.GetRasterBand(1).ReadAsArray()

print(band1.shape)
print(type(band1))