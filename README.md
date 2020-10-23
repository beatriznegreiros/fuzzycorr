## Fuzzy Map Comparison for the Evaluation of Hydro-morphodynamic Numerical Models 
---
This repository contains the work developed for a Master Thesis on fuzzy map comparison methods to evaluate the performance of hydro-morphodynamic numerical models.

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

This repository contains the following modules:
- ``prepro.py``: This module's capabilities include the reading, normalizing and rasterizing vector data. These are preprocessing steps for fuzzy map comparison (module fuzzycomp).
- ``fuzzycomp.py``: Module for performing fuzzy map comparison in continuous valued rasters. The reader is referred to [Hagen(2006)](https://www.researchgate.net/publication/242690490_Comparing_Continuous_Valued_Raster_Data_A_Cross_Disciplinary_Literature_Scan) for more details. Future methods may be developed
- ``plotter.py``: Module for the visualization of output and input rasters.

### Usage
- The docstrings of the package are located in the folder ``docs``.
- The best way to learn the usage is by examples. In the directory ``examples``, the usage of the modules are demonstrated in a case study.
Example:
- Inside the folder ``salzach_case``, the results from a hydro-morphodynamic numerical simulation ( i.e., simulated bed elevation change, deltaZ) are located in ``raw_data``. For more details on the hydro-morphodynamic numerical models the reader is referred to [Beckers et al (2020)](https://www.researchgate.net/publication/342181386_Bayesian_Calibration_and_Validation_of_a_Large-scale_and_Time-demanding_Sediment_Transport_Model).
  - ``prepro_salzach.py``: example of the usage of the class ``PreProFuzzy`` of the module ``prepro.py``, where vector data is interpolated and rasterized.
  - ``classification_salzach.py``: example of the usage of the class ``PreProCategorization`` of the module ``prepro.py``.
  - ``fuzzycomparison_salzach.py``: example of the usage of the class ``FuzzyComparison`` of the module ``fuzzycomp.py``, which creates a correlation (similarity) measure between simulated and observed datasets.
  - ``plot_salzach.py``, ``plot_class_rasters.py`` and ``performance_salzach``: example of the usage of the module ``plotter.py``.
  - ``random_map``: example of generating a raster followin a uniformly random disribution, which uses the module ``prepro.py``.

### Code description
The repository is coded in  ``Python 3.6 x`` 

### Dependencies and Environment

The necessary modules for running this repo are specified in the ``environment.yml`` file, to install all packages in the environment simply:
- navigate with the Anaconda Prompt through your directories to the ``.yml`` file
- type ``conda env create -f environment.yml`` and your environment is ready to go under the name ``env-fuzzycorr``

### References

[Ross Kushnereit](https://github.com/rosskush/skspatial)
&nbsp;&nbsp; | &nbsp;&nbsp;
[Chris Wills](http://chris35wills.github.io/gridding_data/)

### Developed in:

[![Image](Logo_LWW.JPG)](https://www.iws.uni-stuttgart.de/lww/)
