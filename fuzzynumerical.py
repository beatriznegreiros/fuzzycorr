try:
    import numpy as np
    import gdal
    import rasterio as rio
    import math
    import sys
    from rasterio.transform import from_origin
    from pathlib import Path
except:
    print('ModuleNotFoundError: Missing fundamental packages (required: pathlib, numpy, gdal, rasterio, math, sys).')


class FuzzyComparison:
    def __init__(self, rasterA, rasterB, neigh=4, halving_distance=2):
        self.raster_A = rasterA
        self.raster_B = rasterB
        self.neigh = neigh
        self.halving_distance = halving_distance

        self.array_A, self.nodatavalue, self.meta_A = self.read_raster(self.raster_A)
        self.array_B, self.nodatavalue_B, self.meta_B = self.read_raster(self.raster_B)

        if self.nodatavalue != self.nodatavalue_B:
            print('Warning: Maps have different NoDataValues, I will use the NoDataValue of the first map')
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

        :param array: array A or B
        :param x: int, cell in x
        :param y: int, cell in y
        :return: ndarray (float) membership of the neighbours, ndarray (float) neighbours' cells
        """
        x_up = max(x - n, 0)
        x_lower = min(x + n + 1, array.shape[0])
        y_up = max(y - n, 0)
        y_lower = min(y + n + 1, array.shape[1])
        memb = np.zeros((x_lower - x_up, y_lower - y_up), dtype=np.float32)

        np.seterr(divide='ignore', invalid='ignore')

        for i, row in np.ndenumerate(np.arange(x_up, x_lower)):
            for j, column in np.ndenumerate(np.arange(y_up, y_lower)):
                d = math.sqrt((row - x) ** 2 + (column - y) ** 2)
                memb[i, j] = 2 ** (-d / self.halving_distance)

        return memb, array[x_up: x_lower, y_up: y_lower]

    def fuzzy_numerical(self, comparison_name, map_of_comparison=True):
        """ Reads and compares a pair of raster maps using fuzzy numerical spatial comparison

        :param comparison_name: string, name of the comparison
        :param map_A: path of one raster
        :param map_B: path of the other raster
        :param map_of_comparison: boolean, create map of comparison
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

        # Fill nodatavalues into array
        S_i_ma_fi = np.ma.filled(S_i_ma, fill_value=self.nodatavalue)

        # Saves a results file
        result_file = str(dir / "results") + "/" + comparison_name + ".txt"
        lines = ["Fuzzy numerical spatial comparison \n", "\n", "Compared maps: \n",
                 str(self.raster_A) + "\n", str(self.raster_B) + "\n", "\n"]
        file1 = open(result_file, "w")
        file1.writelines(lines)
        file1.write('Average fuzzy similarity: ' + str(format(S, '.4f')))
        file1.close()

        # Create map of comparison
        if map_of_comparison:
            if '.' not in comparison_name[-4:]:
                comparison_name += '.tif'
            comp_map = str(dir / "results") + "/" + comparison_name
            raster = rio.open(comp_map, 'w', **self.meta_A)
            raster.write(S_i_ma_fi, 1)
            raster.close()

        return S


if __name__ == '__main__':
    import timeit

    # ------------------------INPUT--------------------------------------
    # Neighborhood definition
    n = 4  # 'radius' of neighborhood
    halving_distance = 2
    comparison_name = "diamond_res0.1_norm_comparison"

    # Create directory if not existent
    dir = Path.cwd()
    Path(dir / "rasters").mkdir(exist_ok=True)
    Path(dir / "results").mkdir(exist_ok=True)
    map_A_in = str(dir / "rasters/diamond_map_A_res0.1_norm.tif")
    map_B_in = str(dir / "rasters/diamond_map_B_res0.1_norm.tif")
    # ------------------------------------------------------------------

    # Start run time count
    start = timeit.default_timer()

    # Perform fuzzy comparison
    compareAB = FuzzyComparison(map_A_in, map_B_in, n, halving_distance)
    global_simil = compareAB.fuzzy_numerical(comparison_name)

    # Print global similarity
    print('Average fuzzy similarity:', global_simil)

    # Stops run time count
    stop = timeit.default_timer()

    # Print run time:
    print('Enlapsed time: ', stop - start, 's')


