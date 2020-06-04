# Fuzzy Map Comparison for Numerical Model Validation
***
This repository contains the work developed during a Master Thesis on Fuzzy-Kappa 
map comparison to assess the performance of hydro-morphodynamic models.

Further improvements are being done and the final code will be available
at the end of October. 

- For usage please read the Lincense terms.


## Folder's Description

This repository contains the following folders:
- (FMAPHMM) Fuzzy Map Comparison to Assess Performance of Morphodynamic Models:
	- analysis: Figures related to the analysis of the data, histograms, initial overviews etc.
	- codes: 
		- anaylsis: Codes used for analysis of the data 
		- debug: Folder for debugging and keeping track of previous problems
		- main: Folder which contains the main codes for running the Fuzzy-Kappa for Numerical Model Validation
		- testing: Initial tests, trials for getting familiar with functions and libraries in Python
	- rasters: Contains the rasters produced by the main code in formats .tif and .asc
	- shapefiles: Contains shapefiles to be converted in raster
	- raw_data: Stores the data directory which the code will read
- (GUI) Graphical User Interface
	- trials: first steps of the GUI development

## Data Description

The input data necessary for the code to run should follow the format of files:
hexagon_experiment.csv or hexagon_simulation.csv, in which the spatial data is stored 
in tree columns x, y and delta z(respective difference in bed elevation).

The current data being used stems from an experimental physical model set-up. The experiment was simulated using the
numerical model SSIIMM and the results of Bed Elevation Difference compared with the experiment's.

## Code Descriptions

The code presented here is written in ``Python 3.7`` and will be coupled with ``C++`` to run the Fuzzy-Kappa
map comparison algorithm.

