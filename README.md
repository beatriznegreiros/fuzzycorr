## Fuzzy Map Comparison for Numerical Model Validation 
---
This repository contains the work developed during a Master Thesis on fuzzy map comparison methods to assess the performance of hydro-morphodynamic models.

Further improvements are being done and the final code will be available
at the end of October. 

- For usage please read the Lincense terms.

### The goal of the study

Sediment transport and river flow processes are simulated with numerical models such as SSIIMM, 
Hydro_AS_2D and others. The applicability of models built with such softwares is done comparing the simulated and the observed data sets, in a step called validation. 
With the purpose of analysing simulated and observed bed elevation change, two main methods of comparison arise: comparison via statistical methods such as RMSE 
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


### Repo's description

This repository contains the following modules (both can run as stand-alone):
- mapoperator: This module's capabilities include the reading, normalizing and rasterizing spatial data.
- fuzzynumerical: Module for model evaluation based on fuzzy numerical map comparison. Future methods may be developed
- plotter: Module for the visualization of output rasters.

Examples of usage on the package are found in the directory ``examples``. In each of the case studies the organization of the files are done as following:
- raw_data: Stores the data directory which the code will read
- rasters: Rasters will be saved and searched for here
- analysis: Figures related to the analysis of the data, histograms, initial overviews etc.
- shapefiles: Contains shapefiles output or to be converted to rasters, as well as polygons used in the clipping of rasters.
- results: Output of fuzzy comparisons are saved here.


### Code description

The repository is coded in  ``Python 3.6 x`` 

### Dependencies and Environment

The necessary modules for running this repo are specified in the ``environment.yml`` file, to install all packages in the environment simply:
- navigate with the Anaconda Prompt through your directories to the ``.yml`` file
- type ``conda env create -f environment.yml`` and your environment is ready to go under the name ``env-valitools``


