try:
    import matplotlib.pyplot as plt
    import mapoperator as mo
    from pathlib import Path
    import numpy as np
    import gdal
except:
    print('ModuleNotFoundError: Missing fundamental packages (required: pathlib, numpy, gdal).')

# ---------------------INPUT------------------------------------------
# Data:
list_files = ['vali_Hydro_FT-2D_MAP_2013_clipped',
              'vali_aPC_MAP_2013_clipped',
              'vali_hydro_FT_manual_2013_clipped']


#nb_classes = [-3.6, -3.0, -2.4, -1.8, -1.2, -0.6, 0.0, 0.6, 1.2, 1.8, 2.4, 3.0]
# --------------------------------------------------------------------

dir = Path.cwd()
Path(dir / "rasters").mkdir(exist_ok=True)


raster_meas = mo.MapArray(str(dir/'rasters') + '/' + 'vali_meas_2013_clipped.tif')
nb_classes = raster_meas.nb_classes(12)
#raster_meas.categorize_raster(nb_classes, map_out=str(dir/'rasters') + '/' + 'vali_meas_2013_clipped_class_nbreaks.tif')
plt.hlines(1, -3, 3)
plt.eventplot(nb_classes[1::], orientation='horizontal')
plt.axis('off')
plt.show()

'''# Classify the array and save the output file as .tif raster
for file in list_files:
    array_ = mo.MapArray(str(dir/'rasters') + '/' + file + '.tif')
    map_output = (str(dir/'rasters') + '/' + file + '_class_nbreaks.tif')
    array_.categorize_raster(nb_classes, map_output)'''

