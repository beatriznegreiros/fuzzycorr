try:
    import numpy as np
    import gdal
    import rasterio as rio
    import math
    import sys
    from rasterio.transform import from_origin
    from pathlib import Path
except:
    print('ExceptionERROR: Missing fundamental packages (required: pathlib, numpy, gdal).')

# Create directory if not existent
current_dir = Path.cwd().parent.parent
Path(current_dir / "rasters").mkdir(exist_ok=True)


class FuzzyComparison:
    def __init__(self, rasterA, rasterB, neigh=4, halving_distance=2):
        self.raster_A = rasterA
        self.raster_B = rasterB
        self.neigh = neigh
        self.halving_distance = halving_distance

        self.array_A, self.nodatavalue, self.meta_A = self.read_raster(self.raster_A)
        self.array_B, self.nodatavalue_B, self.meta_B = self.read_raster(self.raster_B)

        if self.nodatavalue != self.nodatavalue_B:
            print("Warning: Maps have different NoDataValues, I'll use the NoDataValue of the first map")
        if self.meta_A != self.meta_B:
            sys.exit('MapError: Maps have different MetaData. Hint: Make sure both maps have same src.')

    def read_raster(self, raster):
        with rio.open(raster) as src:
            raster_np = src.read(1, masked=True)
            nodatavalue = src.nodata  # storing nodatavalue of raster
            meta = src.meta.copy()
        return raster_np, nodatavalue, meta

    def f_similarity(self, a, b):
        """ Similarity function for the fuzzy numerical comparison

        :param a: float
        :param b: float
        :return: float, Local similarity between two cells
        """
        return 1 - (abs(a - b)) / max(abs(a), abs(b))

    def neighbours(self, array, x, y):
        """ Takes the neighbours and their memberships

        :param array:
        :param x: int, cell in x
        :param y: int, cell in y
        :param n: int, 'radius' of neighbourhood
        :param halving_dist: int, halving distance of the distance decay function
        :return: ndarray (float) membership of the neighbours, ndarray (float) neighbours' cells
        """
        x_up = max(x - n, 0)
        x_lower = min(x + n + 1, array.shape[0])
        y_up = max(y - n, 0)
        y_lower = min(y + n + 1, array.shape[1])
        memb = np.zeros((x_lower - x_up, y_lower - y_up), dtype=np.float32)

        np.seterr(divide='ignore', invalid='ignore')

        i = 0
        for row in range(x_up, x_lower):
            j = 0
            for column in range(y_up, y_lower):
                d = math.sqrt((row - x) ** 2 + (column - y) ** 2)
                memb[i, j] = 2 ** (-d / self.halving_distance)
                j += 1
            i += 1

        return memb, array[x_up: x_lower, y_up: y_lower]

    def fuzzy_numerical(self, comparison_name):
        """Compares a pair of maps using fuzzy numerical spatial comparison

        :param map_A: path of one raster
        :param map_B: path of the other raster
        :return: overall performance index
        """

        # Two-way similarity, first A x B then B x A
        s_AB = np.zeros(np.shape(self.array_A), dtype=np.float64)
        s_BA = np.zeros(np.shape(self.array_A), dtype=np.float64)

        #  Loop to calculate similarity A x B
        for index, a in np.ndenumerate(self.array_A):
            memb, neighbours = self.neighbours(self.array_B, index[0], index[1])
            f_i = -np.inf
            for nei_index, neighbor in np.ndenumerate(neighbours):
                a = self.array_A[index]
                b = neighbor
                f = self.f_similarity(a, b) * memb[nei_index]
                if f > f_i:
                    f_i = f
            s_AB[index] = f_i

        #  Loop to calculate similarity B x A
        for index, a in np.ndenumerate(self.array_B):
            memb, neighbours = self.neighbours(self.array_A, index[0], index[1])
            f_i = -np.inf
            for nei_index, neighbor in np.ndenumerate(neighbours):
                a = self.array_B[index]
                b = neighbor
                f = self.f_similarity(a, b) * memb[nei_index]
                if f > f_i:
                    f_i = f
            s_BA[index] = f_i

        # Mask pixels where there's no similarity measure
        S_i = np.minimum(s_AB, s_BA)
        S_i_ma = np.ma.masked_where(S_i == -np.inf,
                                    S_i,
                                    copy=True)
        # Overall similarity
        S = S_i_ma.mean()

        return S


if __name__ == '__main__':
    import timeit

    # ------------------------INPUT--------------------------------------
    # Neighborhood definition
    n = 4  # 'radius' of neighborhood
    halving_distance = 2
    comparison_name = "diamond_res0.1_norm_comparison"

    # Rasters input path
    map_A_in = str(current_dir / "rasters/diamond_map_A_res0.1_norm.tif")
    map_B_in = str(current_dir / "rasters/diamond_map_B_res0.1_norm.tif")
    # ------------------------------------------------------------------

    # Start run time count
    start = timeit.default_timer()

    # Perform fuzzy comparison
    compareAB = FuzzyComparison(map_A_in, map_B_in, n, halving_distance)
    global_simil = compareAB.fuzzy_numerical(comparison_name)

    # Print global similarity
    print("Average fuzzy similarity:", global_simil)

    # Stops run time count
    stop = timeit.default_timer()

    # Print run time:
    print('Enlapsed time: ', stop - start, 's')

# Local similarity
'''S_i_ma = np.flipud(np.array(S_i_ma))
comparison_map = str(current_dir / "rasters") + "/" + comparison_name + ".tif"
transform = from_origin(self.xmin, self.ymax, self.res, self.res)
new_dataset = rio.open(comparison_map, 'w', driver='GTiff',
                       height=S_i_ma.shape[0], width=S_i_ma.shape[1], count=1, dtype=S_i_ma.dtype,
                       crs=S_i_ma.crs, transform=transform, nodata=nodatavalue)
new_dataset.write(array, 1)
new_dataset.close()'''