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
    def __init__(self, rasterA, rasterB, project_dir, neigh=4, halving_distance=2):
        self.raster_A = rasterA
        self.raster_B = rasterB
        self.dir = project_dir
        self.neigh = neigh
        self.halving_distance = halving_distance

        self.array_A, self.nodatavalue, self.meta_A, self.src_A, self.dtype_A = \
            self.read_raster(self.raster_A)
        self.array_B, self.nodatavalue_B, self.meta_B, self.src_B, self.dtype_B = \
            self.read_raster(self.raster_B)

        if halving_distance <= 0:
            print('Halving distance must be at least ')
        if self.nodatavalue != self.nodatavalue_B:
            print('Warning: Maps have different NoDataValues, I will use the NoDataValue of the first map')
        if self.src_A != self.src_B:
            sys.exit('MapError: Maps have different coordinate system')
        if self.dtype_A != self.dtype_B:
            print('Warning: Maps have different data types, I will use the datatype of the first map')

    def read_raster(self, raster):
        with rio.open(raster) as src:
            raster_np = src.read(1, masked=True)
            nodatavalue = src.nodata  # storing nodatavalue of raster
            meta = src.meta.copy()
        return raster_np, nodatavalue, meta, meta['crs'], meta['dtype']

    def jaccard(self, a, b):
        jac = 1 - (a * b) / (2 * abs(a) + 2 * abs(b) - a * b)
        return jac

    def f_similarity(self, centrall_cell, neighbours):
        """ Similarity function for the fuzzy numerical comparison

        :param centrall_cell: float
        :param neighbours: numpy array of floats
        :return: numpy array of floats, Local similarity between each of two cells
        """
        simil_neigh = np.ma.masked_array(np.zeros(np.shape(neighbours)), mask=neighbours.mask)
        for index, entry in np.ndenumerate(neighbours):
            simil_neigh[index] = 1 - (abs(entry - centrall_cell)) / max(abs(entry), abs(centrall_cell))
        return simil_neigh

    def neighbours(self, array, x, y):
        """ Takes the neighbours and their memberships

        :param array: array A or B
        :param x: int, cell in x
        :param y: int, cell in y
        :return: ndarray (float) membership of the neighbours, ndarray (float) neighbours' cells
        """
        x_up = max(x - self.neigh, 0)
        x_lower = min(x + self.neigh + 1, array.shape[0])
        y_up = max(y - self.neigh, 0)
        y_lower = min(y + self.neigh + 1, array.shape[1])

        memb = np.zeros((x_lower - x_up, y_lower - y_up), dtype=self.dtype_A)

        np.seterr(divide='ignore', invalid='ignore')

        for i, row in np.ndenumerate(np.arange(x_up, x_lower)):
            for j, column in np.ndenumerate(np.arange(y_up, y_lower)):
                d = ((row - x)**2 + (column - y)**2)**0.5
                memb[i, j] = 2**(-d / self.halving_distance)

            #memb = np.ma.masked_array(memb, mask=array[x_up: x_lower, y_up: y_lower].mask)

        return memb, array[x_up: x_lower, y_up: y_lower]

    def fuzzy_numerical(self, comparison_name, map_of_comparison=True):
        """ compares a pair of raster maps using fuzzy numerical spatial comparison

        :param comparison_name: string, name of the comparison
        :param map_of_comparison: boolean, create map of comparison
        :return: overall performance index
        """

        # Two-way similarity, first A x B then B x A
        s_AB = np.full(np.shape(self.array_A), self.nodatavalue, dtype=self.dtype_A)
        s_BA = np.full(np.shape(self.array_A), self.nodatavalue, dtype=self.dtype_A)

        #  Loop to calculate similarity A x B
        for index, central in np.ndenumerate(self.array_A):
            memb, neighboursA = self.neighbours(self.array_B, index[0], index[1])
            f_i = np.ma.multiply(self.f_similarity(self.array_A[index], neighboursA), memb)
            f_i = np.ma.filled(f_i, fill_value=self.nodatavalue)
            '''print('neighboursA',neighboursA)
            print('simil', self.f_similarity(self.array_A[index], neighboursA))
            print('memb',memb)
            print('f_i', f_i)'''
            s_AB[index] = np.amax(f_i)

        #  Loop to calculate similarity B x A
        for index, central in np.ndenumerate(self.array_B):
            memb, neighboursB = self.neighbours(self.array_A, index[0], index[1])
            f_i = np.ma.multiply(self.f_similarity(self.array_B[index], neighboursB), memb)
            f_i = np.ma.filled(f_i, fill_value=self.nodatavalue)
            s_BA[index] = np.amax(f_i)

        # Mask cells where there's no similarity measure

        S_i = np.minimum(s_AB, s_BA)
        S_i_ma = np.ma.masked_where(S_i == self.nodatavalue, S_i, copy=True)

        # Overall similarity
        S = S_i_ma.mean()

        # Fill nodatavalues into array
        S_i_ma_fi = np.ma.filled(S_i_ma, fill_value=self.nodatavalue)

        # Saves a results file
        Path(self.dir / "results").mkdir(exist_ok=True)
        result_file = str(self.dir / "results") + "/" + comparison_name + ".txt"
        lines = ["Fuzzy numerical spatial comparison \n", "\n", "Compared maps: \n",
                 str(self.raster_A) + "\n", str(self.raster_B) + "\n", "\n", "Halving distance: " +
                 str(self.halving_distance) + " cells  \n", "Neighbourhood: " + str(self.neigh) + " cells  \n", "\n"]
        file1 = open(result_file, "w")
        file1.writelines(lines)
        file1.write('Average fuzzy similarity: ' + str(format(S, '.4f')))
        file1.close()

        # Create map of comparison
        if map_of_comparison:
            if '.' not in comparison_name[-4:]:
                comparison_name += '.tif'
            comp_map = str(self.dir / "results") + "/" + comparison_name
            raster = rio.open(comp_map, 'w', **self.meta_A)
            raster.write(S_i_ma_fi, 1)
            raster.close()

        return S
