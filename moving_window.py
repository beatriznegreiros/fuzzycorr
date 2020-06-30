import numpy as np
import math


class MovingWindow:
    def __init__(self, array, neigh, halving_dist):
        self.array = array
        self.neigh = neigh
        self.halv_dist = halving_dist

    def neighbours(self, x, y):
        """ Takes the neighbours and their memberships

        :param array: array A or B
        :param x: int, cell in x
        :param y: int, cell in y
        :return: ndarray (float) membership of the neighbours, ndarray (float) neighbours' cells
        """
        x_up = max(x - self.neigh, 0)
        x_lower = min(x + self.neigh + 1, self.array.shape[0])
        y_up = max(y - self.neigh, 0)
        y_lower = min(y + self.neigh + 1, self.array.shape[1])
        memb = np.zeros((x_lower - x_up, y_lower - y_up))

        np.seterr(divide='ignore', invalid='ignore')

        for i, row in np.ndenumerate(np.arange(x_up, x_lower)):
            for j, column in np.ndenumerate(np.arange(y_up, y_lower)):
                d = math.sqrt((row - x) ** 2 + (column - y) ** 2)
                memb[i, j] = 2 ** (-d / self.halv_dist)

        return memb, self.array[x_up: x_lower, y_up: y_lower]