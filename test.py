from pathlib import Path

current_dir = Path.cwd()
raster_file = str(current_dir / 'rasters') + '/' + 'something' + '.tif'

map_asc = Path(raster_file[1:-4] + '.asc')

print(map_asc)