import numpy as np
from collections import Iterable  # used in the flatten function
import os, sys, glob, time  # remove irrelevant

def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item
			
def pearson_r(X, Y):
    # returns the pearson correlation coefficient of two vectors X and Y (same length)
    # handles np.nan, see https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    if not (X.__len__() == Y.__len__()):
        print('WARNING: Different length of X and Y vectors.')
        try:
            print('WARNING: Different length of X and Y vectors.')
        except:
            print('WARNING: This information could not be written to the logfile.')
        return np.nan
    else:
        X_sub, Y_sub = resample_vectors(X, Y)
        if X_sub.__len__() > 30:
            eff_len = X_sub.__len__()
            try:
                print('     -- correlation info: valid percentage in X data = %0.9f percent' % (eff_len / X.__len__() * 100))
            except:
                print(' -- correlation info: valid percentage in X/Y data = %0.9f' % (eff_len / X.__len__() * 100))
            mean_x = float(np.nansum(X) / eff_len)
            mean_y = float(np.nansum(Y) / eff_len)
            nominator = 0.0
            denominator_x = 0.0
            denominator_y = 0.0
            eps = 0.000001
            for i in range(0, X_sub.__len__()):
                if not (np.any(np.absolute(X_sub[i]) < eps) or np.any(np.absolute(Y_sub[i]) < eps)):
                    nominator += (X_sub[i] - mean_x) * (Y_sub[i] - mean_y)
                    denominator_x += float((X_sub[i] - mean_x) ** 2)
                    denominator_y += float((Y_sub[i] - mean_y) ** 2)
            try:
                return float(nominator / (np.sqrt(denominator_x) * np.sqrt(denominator_y)))
            except:
                return np.nan
        else:
            try:
                print('     -- SET OF VALID DATA IS TOO SMALL (size: %i < 30)' % int(X_sub.__len__()))
            except:
                print('     -- SET OF VALID DATA IS TOO SMALL (size: %i < 30)' % int(X_sub.__len__()))
            return np.nan

if __name__ == '__main__':
    data_array_physical = np.array((100, 100))  # change to 2D array data (e.g., physical model output for terrain change)
    data_array_numerical = np.array((100, 100))  # change to 2D array data (e.g., numerical model output for terrain change)
    try:
        corr = pearson_r(list(flatten(data_array_physical)), list(flatten(data_array_numerical)))
        if corr == np.nan:
            print('WARNING: Pearson r is nan.')
    except:
        print('ERROR: Failed to calculate global correlation coefficient.')
        corr = np.nan