import pandas as pd
import geo_operator
import mapclassify
import geopandas
import matplotlib.pyplot as plt

data_A = pd.read_csv("hexagon_experiment.csv")
data_B = pd.read_csv("hexagon_simulation.csv")

data_A.dropna(how='any', inplace=True, axis=0)
data_B.dropna(how='any', inplace=True, axis=0)

geo_operator.data_to_shape(data_B, "map_A.shp")
gdfA = geopandas.GeoDataFrame.from_file('map_A.shp')

classifier = mapclassify.Quantiles(y=gdfA['dz'])
gdfA['dz'].plot.hist(bins=50)

for value in classifier.bins:
    plt.axvline(value, color='k', linestyle='dashed', linewidth=1)

plt.show()