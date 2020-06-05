try:
    import mapoperator as mo
    from pathlib import Path
    import numpy as np
    import gdal
except:
    print('ExceptionERROR: Missing fundamental packages (required: pathlib, numpy).')

# INPUT: d84 as parameter
d = 0.013  # in cm
n_classes = 6

current_dir = Path.cwd().parent.parent
Path(current_dir / "rasters").mkdir(exist_ok=True)

# INPUT: Raster input path

map_A_in = str(current_dir / "rasters/map_A.tif")
map_B_in = str(current_dir / "rasters/map_B.tif")

# INPUT: Rasters output path
map_A_out = str(current_dir / "rasters/map_A_class.tif")
map_B_out = str(current_dir / "rasters/map_B_class.tif")

# INPUT: Ascii files path
map_A_asc = str(current_dir / "rasters/map_A_class.asc")
map_B_asc = str(current_dir / "rasters/map_B_class.asc")

# Classification based on d84
# Bins to classify the data Legend: HE (High Erosion), HIE (High Intermediate Erosion), IE (Intermediate Erosion),
# LIE (Low Intermediate Erosion), LE (Low Erosion), Static,  LD (Low Deposition), LID (Low Intermediate Deposition),
# ID (Intermediate Deposition), HID (High Intermediate Deposition), HD (High Deposition).
'''class_bins = [-100 * d, -20 * d, -10 * d, -5 * d, -2 * d, -0.5 * d, 0.5 * d, 2 * d, 5 * d, 10 * d, 20 * d,
              np.iinfo(np.int32).max]
'''

# Import raster as np array
array_A = mo.MapArray(mo.raster_to_np(map_A_in))
array_B = mo.MapArray(mo.raster_to_np(map_B_in))

# Classify the array and save the output file as .tif raster
nb_classes = array_A.nb_classes(n_classes) # Extract the optimized intervalls for the map A
array_A.classifier(map_A_out, nb_classes)
array_B.classifier(map_B_out, nb_classes)

# Convert .tif to ascii file
gdal.Translate(map_A_asc, map_A_out, format='AAIGrid')
gdal.Translate(map_B_asc, map_B_out, format='AAIGrid')



