# GEOTrat Points
Mapping tool for agricultural experimentation that allows evaluating the efficiency of one treatment over the other through geostatistics.

## Installation
To install the plugin:
1 - download the .model3 file, or the .py file available in the repository;
2 - Open the QGIS software;
3 - Enable the processing toolbox (indicated by the gear icon);
4 - Click on the first icon that has 3 gears (red, gray and blue), and select the option add model to toolbox, select .model3 file;
5 - Still, in the processing toolbox, expand the Models option, and select GEOTrat - Points 1.1, and the tool will open in a new tab.
ATTENTION: the .model3 file cannot be deleted from your computer.

## Step-by-step usage guidelines
Select the following variables and layers in the input boxes:
Variable measured in the field: Point-type geometry vector that represents the variable measured in the field.

Variable field: Numeric type field that indicates the value measured in the field of the variable of interest. 

Treatment field: Text type field (T1/T2) that indicates which treatment the measured value belongs to. T1 must be the control treatment and T2 the treatment to be evaluated.

Reference treatment: Select reference treatment, if you select T1, the gain will be calculated as T1 - T2, if you select T2, the gain will be calculated as T2 - T1.

Study area polygon: Polygon type geometry vector representing the study area.

Projected Coordinate System: Projected coordinate system that the study area is located.

Pixel size (m): Pixel size in meters that will be the spacial resolution of the output surfaces. It is suggested that the value be approximated by the average distance between the entry points.

Semivariogram model: Model to be used for the kriging semivariogram. Choose from the options: linear, exponential, gaussian and spherical.

Results - T1:Estimated surface in raster format for the study area, simulating as if the area had been treated entirely with T1. And T2: Estimated surface in raster format for the study area, simulating as if the area had been treated entirely with T2.

##  Requirements and dependencies
Version: 1.1

Developed QGIS version: 3.22.8

Requires installation: SAGA and SAGA Next Gen

