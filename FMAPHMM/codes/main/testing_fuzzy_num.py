try:
    import mapoperator as mo
    from pathlib import Path
    import numpy as np
    import gdal
except:
    print('ExceptionERROR: Missing fundamental packages (required: pathlib, numpy, gdal, pysal).')

current_dir = Path.cwd().parent.parent
Path(current_dir / "rasters").mkdir(exist_ok=True)

# INPUT: Raster input path

map_A_in = str(current_dir / "rasters/map_A.tif")
map_B_in = str(current_dir / "rasters/map_B.tif")

A = mo.MapArray(mo.raster_to_np(map_A_in))
B = mo.MapArray(mo.raster_to_np(map_B_in))

# Two-way similarity, first A x B then B x A
s_AB = np.zeros(np.shape(A.array), dtype=float)
s_BA = np.zeros(np.shape(A.array), dtype=float)

for index, a in np.ndenumerate(A.array):
    neighbours = B.neighbours(index[0], index[1])
    f_i = -np.inf
    for nei_index, neighbor in np.ndenumerate(neighbours):
        a = A.array[index]
        b = neighbor
        f = mo.f_similarity(a, b) # * multiply by membership

        if f > f_i:
            f_i = f
    s_AB[index] = f_i

print(s_AB)
print(np.shape(s_AB))

# perform the other-way comparison B versus A
