try:
    import mapoperator as mo
    from pathlib import Path
    import numpy as np
    import gdal
except:
    print('ExceptionERROR: Missing fundamental packages (required: pathlib, numpy, gdal).')

# Create directory if not existent
current_dir = Path.cwd().parent.parent
Path(current_dir / "rasters").mkdir(exist_ok=True)


def f_similarity(a, b):
    """ Similarity function for the fuzzy numerical comparison

    :param a: float
    :param b: float
    :return: float, Local similarity between two cells
    """
    return 1 - (abs(a - b)) / max(abs(a), abs(b))


def fuzzy_numerical(map_A, map_B):
    """Compares a pair of maps using fuzzy numerical spatial comparison

    :param map_A: path of one raster
    :param map_B: path of the other raster
    :return: overall performance index
    """
    # Read rasters as arrays
    A = mo.MapArray(mo.raster_to_np(map_A))
    B = mo.MapArray(mo.raster_to_np(map_B))

    # Two-way similarity, first A x B then B x A
    s_AB = np.zeros(np.shape(A.array), dtype=float)
    s_BA = np.zeros(np.shape(A.array), dtype=float)

    #  Loop to calculate similarity A x B
    for index, a in np.ndenumerate(A.array):
        memb, neighbours = B.neighbours(index[0], index[1], n=n, halving_dist=halving_distance)
        f_i = -np.inf
        for nei_index, neighbor in np.ndenumerate(neighbours):
            a = A.array[index]
            b = neighbor
            f = f_similarity(a, b) * memb[nei_index]
            if f > f_i:
                f_i = f
        s_AB[index] = f_i

    #  Loop to calculate similarity B x A
    for index, a in np.ndenumerate(B.array):
        memb, neighbours = A.neighbours(index[0], index[1], n=n, halving_dist=halving_distance)
        f_i = -np.inf
        for nei_index, neighbor in np.ndenumerate(neighbours):
            a = B.array[index]
            b = neighbor
            f = f_similarity(a, b) * memb[nei_index]
            if f > f_i:
                f_i = f
        s_BA[index] = f_i

    # Mask pixels where there's no similarity measure
    S_i = np.minimum(s_AB, s_BA)
    S_i_ma = np.ma.masked_where(S_i == -np.inf,
                                S_i,
                                copy=True)
    S = S_i_ma.mean()
    # Local similarity


    # Overall similarity
    print("The overall average similarity is:", S)


if __name__ == '__main__':
    # 2. Neighborhood definition
    n = 4  # 'radius' of neighborhood
    halving_distance = 2

    # 3. INPUT: Rasters input path
    map_A_in = str(current_dir / "rasters/hexagon_map_A.tif")
    map_B_in = str(current_dir / "rasters/hexagon_map_B.tif")

    fuzzy_numerical(map_A_in, map_B_in)
