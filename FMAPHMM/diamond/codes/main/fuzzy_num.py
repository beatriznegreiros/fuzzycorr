try:
    import mapoperator as mo
    from pathlib import Path
    import numpy as np
    import gdal
except:
    print('ExceptionERROR: Missing fundamental packages (required: pathlib, numpy, gdal, pysal).')

# 1. Create directory if not existent
current_dir = Path.cwd().parent.parent
Path(current_dir / "rasters").mkdir(exist_ok=True)

# 2. Neighborhood definition
n = 4  # 'radius' of neighborhood
halving_distance = 2

# 3. INPUT: Rasters input path
map_A_in = str(current_dir / "rasters/map_A.tif")
map_B_in = str(current_dir / "rasters/map_B.tif")

# 4. Read rasters as arrays
A = mo.MapArray(mo.raster_to_np(map_A_in))
B = mo.MapArray(mo.raster_to_np(map_B_in))

# 5. Two-way similarity, first A x B then B x A
s_AB = np.zeros(np.shape(A.array), dtype=float)
s_BA = np.zeros(np.shape(A.array), dtype=float)

#  5.1  Loop to calculate similarity A x B
for index, a in np.ndenumerate(A.array):
    memb, neighbours = B.neighbours(index[0], index[1], n=n, halving_dist=halving_distance)
    f_i = -np.inf
    for nei_index, neighbor in np.ndenumerate(neighbours):
        a = A.array[index]
        b = neighbor
        f = mo.f_similarity(a, b) * memb[nei_index]
        if f > f_i:
            f_i = f
    s_AB[index] = f_i

#  5.2  Loop to calculate similarity B x A
for index, a in np.ndenumerate(B.array):
    memb, neighbours = A.neighbours(index[0], index[1], n=n, halving_dist=halving_distance)
    f_i = -np.inf
    for nei_index, neighbor in np.ndenumerate(neighbours):
        a = B.array[index]
        b = neighbor
        f = mo.f_similarity(a, b) * memb[nei_index]
        if f > f_i:
            f_i = f
    s_BA[index] = f_i

# 6.  Mask pixels where there's no similarity measure
S_i = np.minimum(s_AB, s_BA)
S_i_ma = np.ma.masked_where(S_i == -np.inf,
                            S_i,
                            copy=True)
S = S_i_ma.mean()
# 7.  Local similarity
print(S_i_ma.shape)

# 8. Overall similarity
print("The overall average similarity is:", S)
