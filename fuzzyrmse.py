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
            print('Halving distance must be at least 1')
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

    def squared_error(self, centrall_cell, neighbours):
        """ Similarity function for the fuzzy numerical comparison

        :param centrall_cell: float
        :param neighbours: numpy array of floats
        :return: numpy array of floats, Local similarity between each of two cells
        """
        # simil_neigh = np.ma.masked_array(np.zeros(np.shape(neighbours)), mask=neighbours.mask)
        simil_neigh = np.zeros(np.shape(neighbours))
        for index, entry in np.ndenumerate(neighbours):
            simil_neigh[index] = ((entry - centrall_cell) ** 2)
        return simil_neigh

    def residual(self, centrall_cell, neighbours):
        """ Similarity function for the fuzzy numerical comparison

        :param centrall_cell: float
        :param neighbours: numpy array of floats
        :return: numpy array of floats, Local similarity between each of two cells
        """
        # simil_neigh = np.ma.masked_array(np.zeros(np.shape(neighbours)), mask=neighbours.mask)
        simil_neigh = np.zeros(np.shape(neighbours))
        for index, entry in np.ndenumerate(neighbours):
            simil_neigh[index] = (entry - centrall_cell)
        return simil_neigh

    def neighbours(self, array, x, y):
        """ Takes the neighbours and their memberships

        :param array: array A or B
        :param x: int, cell in x
        :param y: int, cell in y
        :return: ndarray (float) membership of the neighbours (without mask), ndarray (float) neighbours' cells (without mask)
        """
        array_ma = np.ma.masked_where(array == self.nodatavalue, array, copy=True)

        x_up = max(x - self.neigh, 0)
        x_lower = min(x + self.neigh + 1, array.shape[0])
        y_up = max(y - self.neigh, 0)
        y_lower = min(y + self.neigh + 1, array.shape[1])

        memb = np.zeros((x_lower - x_up, y_lower - y_up), dtype=self.dtype_A)

        for i, row in np.ndenumerate(np.arange(x_up, x_lower)):
            for j, column in np.ndenumerate(np.arange(y_up, y_lower)):
                d = ((row - x) ** 2 + (column - y) ** 2) ** 0.5
                memb[i, j] = 2 ** (-d / self.halving_distance)

        memb_ma = np.ma.masked_array(memb, mask=array_ma[x_up: x_lower, y_up: y_lower].mask)

        return memb_ma[~memb_ma.mask], array_ma[x_up: x_lower, y_up: y_lower][
            ~array_ma[x_up: x_lower, y_up: y_lower].mask]

    def fuzzy_error(self, comparison_name, map_of_comparison=True):
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
            if not self.array_A.mask[index]:
                memb, neighboursA = self.neighbours(self.array_B, index[0], index[1])
                f_i = np.ma.divide(self.squared_error(self.array_A[index], neighboursA), memb)
                if f_i.size != 0:
                    s_AB[index] = np.amin(f_i)

        #  Loop to calculate similarity B x A
        for index, central in np.ndenumerate(self.array_B):
            if not self.array_B.mask[index]:
                memb, neighboursB = self.neighbours(self.array_A, index[0], index[1])
                f_i = np.ma.divide(self.squared_error(self.array_B[index], neighboursB), memb)
                # f_i = np.ma.filled(f_i, fill_value=self.nodatavalue)
                if f_i.size != 0:
                    s_BA[index] = np.amin(f_i)

        S_i = np.maximum(s_AB, s_BA)

        # Mask cells where there's no similarity measure
        S_i_ma = np.ma.masked_where(S_i == self.nodatavalue, S_i, copy=True)

        # Overall similarity
        S = (S_i_ma.mean())**0.5

        # Fill nodatavalues into array
        S_i_ma_fi = np.ma.filled(S_i_ma, fill_value=self.nodatavalue)

        # Saves a results file
        Path(self.dir / "results").mkdir(exist_ok=True)
        result_file = str(self.dir / "results") + "/" + comparison_name + ".txt"
        lines = ["Fuzzy RMSE for spatial comparison \n", "\n", "Compared maps: \n",
                 str(self.raster_A) + "\n", str(self.raster_B) + "\n", "\n", "Halving distance: " +
                 str(self.halving_distance) + " cells  \n", "Neighbourhood: " + str(self.neigh) + " cells  \n", "\n"]
        file1 = open(result_file, "w")
        file1.writelines(lines)
        file1.write('Fuzzy error: ' + str(format(S, '.4f')))
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
