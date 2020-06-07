Validation Tools ![Image](Image.png)

## Fuzzy Map Comparison for Numerical Model Validation
---
This repository contains the work developed during a Master Thesis on fuzzy map comparison methods to assess the performance of hydro-morphodynamic models.

Further improvements are being done and the final code will be available
at the end of October. 

- For usage please read the Lincense terms.

### The goal of the Study

Sediment transport and river flow processes are simulated with numerical models such as SSIIMM, 
Hydro_AS_2D and others. The validity of such models is done comparing simulated against the observed data sets. 
With this purpose, two main methods of comparison arise: comparison via statistical methods such as RMSE 
(Root Mean Squared Error) or visual human comparison. Local measures of similarity (or asimilarity) like the RMSE are very 
sensible to locational and value uncertainty and may indicate low agreement even when the overall patterns were adequately 
simulated. 

In contrast, visual comparison is able to capture global similarity, which is one of the reasons why modelers still
use it for model validation. Humans are capable of finding patterns without deliberately trying and therefore this comparison offers 
substantial advantages over local similarity measures. Nevertheless, more research has to be done to implement automated validation tools 
with some features of human thinking. That is necessary because human comparison is not transparent and prone to subjective interpretations; 
moreover, it is time consuming and hardly reproducible.

In this context, the concept of fuzzy set theory has proven to be remarkable in capturing spatial patterns similar to human thinking.
By introducing fuzziness of location, one introduces tolerance to spatial uncertainties in the outputs of hydro-morphodynamic models. 
Fuzzy logic is, therefore, highly applicable to these models because the last hold considerable uncertainties in model's structure, 
parameters and input data.

This work addresses such necessity in evaluating model performance through the use of fuzzy map comparison. The tools developed here
could be applied to assess hydro-morphodynamic model's validity and aid modelers on designing calibration procedures.


### Projects's Description

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

### Data Description

The input data necessary for the code to run should follow the format of files:
hexagon_experiment.csv or hexagon_simulation.csv, in which the spatial data is stored 
in tree columns x, y and delta z(respective difference in bed elevation).

The current data being used stems from an experimental physical model set-up. The experiment was simulated using the
numerical model SSIIMM and the results of Bed Elevation Difference compared with the experiment's.

### Code Descriptions

The repository is coded in  ``Python 3.7`` 


