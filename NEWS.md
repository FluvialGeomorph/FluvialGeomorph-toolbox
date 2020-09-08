# FluvialGeomorph v0.1.37 (Release date: 2020-09-07)

## Major Changes
* Updated the Level 1 Report with new options. 
* Updated the Estimate Bankfull Report with new options.
* Updated the Level 2 Report with new options.

## Bug fixes
* Lots of little bug fixes in the `fluvgeo` R package. 
* The Level 2 Report option `Show XS Map` will cause the report to fail. 

## Compatibility Matrix
Please follow the compatibility matrix below to determine the required combination of software components necessary to run the toolbox. 

Software        |Suported  |Not Supported
---             |---       |---          
ArcGIS Pro      |2.5       |2.5          
ArcMap          |10.7      |10.8         
R               |3.6       |![](https://img.shields.io/badge/-4.0-red)          
R-bridge        |1.0.1.239 |![](https://img.shields.io/badge/-1.0.1.241-red)  
FluvialGeomorph |0.1.37    |0.1.37             

**Note: The ArcGIS R-bridge does not yet support R 4.0 for use in ArcGIS Pro or ArcMap geoprocessing tools.**



# FluvialGeomorph v0.1.36 (Release date: 2020-08-31)

## Major Changes
* The `Level 2 Report` tool now has the option to not display the cross section map. This speeds report production. 

## Bug fixes
* Lots of little bug fixes in the `fluvgeo` R package. 

## Compatibility Matrix
Please follow the compatibility matrix below to determine the required combination of software components necessary to run the toolbox. 

Software        |Suported  |Not Supported
---             |---       |---          
ArcGIS Pro      |2.5       |2.5          
ArcMap          |10.7      |10.8         
R               |3.6       |![](https://img.shields.io/badge/-4.0-red)          
R-bridge        |1.0.1.239 |![](https://img.shields.io/badge/-1.0.1.241-red)  
FluvialGeomorph |0.1.36    |0.1.36             

**Note: The ArcGIS R-bridge does not yet support R 4.0 for use in ArcGIS Pro or ArcMap geoprocessing tools.**


# FluvialGeomorph v0.1.35 (Release date: 2020-08-15)

## Major Changes
* Updated the `Slope and Sinuosity` tool. 
* Added the `Level 2 Report` tool. 

## Bug fixes
* Fixed the `Estimate Bankfull` tool. 


## Compatibility Matrix
Please follow the compatibility matrix below to determine the required combination of software components necessary to run the toolbox. 

Software        |Suported  |Not Supported
---             |---       |---          
ArcGIS Pro      |2.5       |2.5          
ArcMap          |10.7      |10.8         
R               |3.6       |![](https://img.shields.io/badge/-4.0-red)          
R-bridge        |1.0.1.239 |![](https://img.shields.io/badge/-1.0.1.241-red)  
FluvialGeomorph |0.1.35    |0.1.35             

**Note: The ArcGIS R-bridge does not yet support R 4.0 for use in ArcGIS Pro or ArcMap geoprocessing tools.**


# FluvialGeomorph v0.1.34 (Release date: 2020-07-27)

## Bug fixes
* Fixed Level 1 Report.

## Compatibility Matrix
Please follow the compatibility matrix below to determine the required combination of software components necessary to run the toolbox. 

Software        |Suported  |Not Supported
---             |---       |---          
ArcGIS Pro      |2.5       |2.5          
ArcMap          |10.7      |10.8         
R               |3.6       |![](https://img.shields.io/badge/-4.0-red)          
R-bridge        |1.0.1.239 |![](https://img.shields.io/badge/-1.0.1.241-red)  
FluvialGeomorph |0.1.34    |0.1.34             

**Note: The ArcGIS R-bridge does not yet support R 4.0 for use in ArcGIS Pro or ArcMap geoprocessing tools.**


# FluvialGeomorph v0.1.33 (Release date: 2020-07-27)

## Bug Fixes
* Continued improvements to the R package install process to be more resilient. 
* Updated all toolbox R functions to use the new R package load process.  

## Compatibility Matrix
Please follow the compatibility matrix below to determine the required combination of software components necessary to run the toolbox. 

Software        |Suported  |Not Supported
---             |---       |---          
ArcGIS Pro      |2.5       |2.5          
ArcMap          |10.7      |10.8         
R               |3.6       |![](https://img.shields.io/badge/-4.0-red)          
R-bridge        |1.0.1.239 |![](https://img.shields.io/badge/-1.0.1.241-red)  
FluvialGeomorph |0.1.33    |0.1.33             

**Note: The ArcGIS R-bridge does not yet support R 4.0 for use in ArcGIS Pro or ArcMap geoprocessing tools.**


# FluvialGeomorph v0.1.32 (Release date: 2020-07-09)

## Bug Fixes
* Overhauled the `R` package install process to make it more robust and secure on a wider range of previous `R` installs. 


# FluvialGeomorph v0.1.31 (Release date: 2020-07-06)

## Major Changes
* Tested toolbox to ensure it supports `R` 4.0 on both ArcGIS Pro (2.5) and ArcMap (10.7.1). 

## Bug Fixes
* Fixed a bug that was preventing tools from running in ArcGIS Pro due to an apparent circular dependency reference (`devtools` unable to install `pkgload`). 


# FluvialGeomorph v0.1.30 (Release date: 2020-06-30)

## Major Changes
* FluvialGeomorph `R` packages (i.e., `RegionalCurve`, `fluvgeo`) now install directly from GitHub using the `Install R packages` tool. 


# FluvialGeomorph v0.1.29 (Release date: 2020-06-18)

## Major Changes
* Added the `Longitudinal Profile Compare` tool to the Reports toolset. 
* Added the `XS Longitudinal Profile Compare` tool to the Reports toolset.
* Added the `Level 1 Report` tool to the Reports toolset.

## Bug Fixes
* Added the Cole Creek test datasets (2004, 2010, 2016) for tools that need multiple time periods. 


# FluvialGeomorph v0.1.28 (Release date: 2020-05-28)

## Major Changes
* Updated all tools to ensure they work in both ArcMap and ArcGIS Pro. 
* Added the `XS Compare Plot` to allow users to create a cross section plot for multiple survey time periods. 
* The `XS Dimension` tool is now running in both ArcMap and ArcGIS Pro. 
* The `XS planform` tool is now running in both ArcMap and ArcGIS Pro. 
* Moved existing dataset symbology tools into a new toolset named `Datasets` within the `Symbology` toolset to make room for new symbology tools that will standardize symbolization of stream dimensions. 
* Created a new toolset called `Export`. Added a new tool to export attribute tables for Level 1 feature classes. This export capability supports further analysis in other applications. 
* Renamed several tools to improve consistency. Tools are being renamed to the feature classes they create:
    * 02 - Burn Cutlines was renamed to: 02 - Hydro DEM
    * 04c - Point Watershed was renamed to: 04c - Watersheds
    * 05 - Create Flowline was renamed to: 05 - Flowline
    * 06 - Stream Profile Points was renamed to: 06 - Flowline Points
    * 13 - XS Assign River Position was renamed to: 13 - XS River Position
    * 14 - XS Station Points was renamed to: 14 - XS Points
    * RAS Watersurface was renamed to: 16 - XS RAS Watersurface
* Streamlined the interface of the `XS Layout` tool to more closely match the other tools in the FG toolbox.

## Bug Fixes
* Added a set of functions for troubleshooting the mapping of tool parameters from ESRI to R. Many bugs were resulting from the difference between ESRI and R's data type mapping. A new table will be added to the beginning of each tool message output to make these mappings clear to streamline troubleshooting. 
* Tool running in ArcGIS Pro had been hindered by the different way Pro handles the assignment of datasets to the current workspace (compared with ArcMap). Explicit data path references were added to prevent conflicts and protect the FG codebase from future changes ESRI might make. 
* Updated package test data. 


# FluvialGeomorph v0.1.27 (Release date: 2020-05-14)

## Major Changes
* Updated the `Stream Profile Points` tool to support route calibration. Now a "mile marker" point feature class can be specified and the output points will be stationed according to these "mile markers". This supports analysis of large rivers with established stationing and change analysis where the same stream is surveyed at multiple time periods, but the stationing of a base year is used for comparison. 

* Added the `Point Watershed` tool that allows a user to calculate the upstream contributing area for each point in the input point feature class. Optionally, it allows land cover to be summarized for each contributing watershed. 

* Added the `Contributing Area D8` tool to support delineating watersheds using the new `Point Watershed` tool. It produces a D8 flow direction raster needed for watershed delineation. 

* Updated the `Burn Cutlines` tool to allow for widening the cut made by each cutline. 
* Updated the `Channel Slope` tool to expose the `z_factor` parameter to handle z-units different from z, y-units. 

* Removed the `Point Landcover` tool. This tool was replaced by the functionality in the `Point Watershed` tool. 

## Bug Fixes
* Fixed bug in `Burn Cutlines` when `widen_cells` = 0. 
* Fixed bug in `Channel Slope`. 
* Updated the help text for all tools. 
