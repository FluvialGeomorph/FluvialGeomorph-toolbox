# FluvialGeomorph v0.2.2 (Release date: 2024-05-26)

## Major Changes
* Added the report `Report - L1 b` that displays cross sections plots disaggregated by extent. 
* Added the report `XS Compare Plot, L1` that plots XS points for a specified extent of the cross section. 
* Added the tool `14a - XS Points Classify` that classifies XS station points as falling within floodplain and channel polygons. 
* Recommended a Level 1 workflow adjustment to use the `detrend` raster to make a rough estimate of the channel and floodplain at the end of L1, rather than wait until L2 for a more informed estimate. Use tool `08 - Water Surface Extent` to create new polygon feature classes `channel_xxx` and `floodplain_xxx` (where xxx represents the detrended elevation) to capturet these L1 rough estimates. These will be revised further in L2 with better estimates. 
* Added the data management `Join From CSV` tool to workaround the inability to reliably write results into ESRI geodatabases. 

## Bug Fixes
* Fixed a bug in the `15b - XS Dimensions, Level 2` tool that was causing slope and sinuosity values for the last cross section to calculate null values. 
* Fixed tool 12 - XS Watershed Area. 
* Updated tools 15a, 15b, 15c to use only `sf` functions from `fluvgeo`. 
* Updated tool in the `Check` toolset. 
* Removed all remaining `sp` and `rgdal` dependencies. 
* Removed all use of the `arcgisbinding::arc.write` function as it has proven over the past 2 years to be too fragile to risk any further production use. No reliable write methods remain for the file geodatabase format from R. Therefore, all R data frame output is now written to `.csv` files for later import into file geodatabase format. Adoption of this strategy mitigates any further disruption to this project from ESRI's lack of support for ensuring a robust `arcgisbinding::arc.write` function. 

***


# FluvialGeomorph v0.2.1 (Release date: 2024-01-22)

## Major Changes
* Updated workflow to support importing on-the-ground field survey data. Added or modified the following tools:
  
  * Added the `Import Thalweg` tool - Creates a `thalweg_points` feature class from a field survey. 
  * Added the `Import Field XS` tool - Creates a `field_xs_points` feature class from a field survey. 
  * Added the `DEM From Field` tool - Creates a DEM from field survey points. 
  * Added the `Flowline Thalweg` tool - Creates a `flowline` feature class from a `thalweg_points` feature class. 
  * Updated the `Flowline Points` tool  - It now allows setting the `station_distance` parameter to zero to support using field surveys. Setting `station_distance` to zero turns off simplification of the `flowline` and creating regularly spaced `flowline_points` at the station_distance spacing. This preserves the original field surveyed thalweg locations. 
  * Added the `XS From Field` tool - Creates a polyline feature class from a `field_xs_points` feature class. 

## Bug fixes
* Refactored R scripts to use the [`here`](https://here.r-lib.org//articles/here.html) package to resolve script location within the toolbox folder structure. 
* Updated the process for pandoc executable detection. 

***

# FluvialGeomorph v0.1.8 (Release date: 2023-08-24)

## Major Changes
* None

## Bug fixes
* Install latest stable release of RegionalCurve.  

***

# FluvialGeomorph v0.1.7 (Release date: 2023-03-22)

## Major Changes
* Removed `ceramic` dependency and added in `maptiles` and `terrainr` to create 
basemaps for aerial and elevation data. 

## Bug fixes
* Removed dependency on the  package `ceramic`. 

## Compatability Matrix
This table describes the latest versions the software has been tested with. 

Software        |Tested    
---             |---               
ArcGIS Pro      |3.0.2              
R               |4.2.2             
R-bridge        |1.0.1.300  
FluvialGeomorph |0.1.7  

***

# FluvialGeomorph v0.1.6 (Release date: 2023-01-25)

## Major Changes
* To ensure that all feature classes are in the same coordinate system, each project file geodatabase will use a feature dataset to store all feature classes. To support this change, all tools have been refactored to expect feature classes to reside within a feature dataset. 
* Discovered that `arcgisbinding::arc.write` frequently fails to write feature classes to a file geodatabase. To workaround this limitation, we have decided 
to only write table data from R back to the file geodatabase. The tools `04b - Gradient`, `15a - XS Dimensions, Level 1`, `15b - XS Dimensions, Level 2`, and `15c - XS Planform, Level 3` now write their results as tables. 
* Added a `JoinField` tool to the `Data Management` toolset. This allows calculations made in R and written to tables to be joined back to their geometry feature classes. 

## Bug fixes
* Removed dependency on the unmaintained package `facetscales`. 

## Compatability Matrix
This table describes the latest versions the software has been tested with. 

Software        |Tested    
---             |---               
ArcGIS Pro      |3.0.2              
R               |4.2.0             
R-bridge        |1.0.1.300  
FluvialGeomorph |0.1.6   

***

# FluvialGeomorph v0.1.5 (Release date: 2022-05-16)

## Major Changes
* None.

## Bug fixes
* Updated the install tool to handle Pandoc located within the RStudio Quarto distribution

## Compatability Matrix
This table describes the latest versions the software has been tested with. 

Software        |Tested    
---             |---               
ArcGIS Pro      |2.9.2              
ArcMap          |-                
R               |4.1.3             
R-bridge        |1.0.1.244  
FluvialGeomorph |0.1.5     

***

# FluvialGeomorph v0.1.42 (Release date: 2021-02-28)

## Major Changes
* The R-bridge (arcgisbinding v1.0.1.244) now fully supports R 4.x. Therefore, the FluvialGeomorph toolbox can now be used in ArcGIS Pro and Map with the latest version of R. 

## Bug fixes
* The install script now creates the ceramic cache directory. If this directory doesn't previously exist, tools calling ceramic would fail when the interactive prompt wasn't responded to. On certian computers, this bug prevented all reports from running since a map calling ceramic is at the beginning of each report. 

## Compatability Matrix
This table describes the latest versions the software has been tested with. 

Software        |Tested    |Not Tested
---             |---       |---          
ArcGIS Pro      |2.6.1     |2.7+          
ArcMap          |10.7.1    |10.8+         
R               |4.0.3     |4.0.4          
R-bridge        |1.0.1.244 | -   
FluvialGeomorph |0.1.42    | -  

***

# FluvialGeomorph v0.1.41 (Release date: 2020-12-14)

## Major Changes
* Added chart output to the XS River Position tool to allow the user to QA the watershed area and river position calculations before proceeding. 

## Bug fixes
* Fixed the feature class check functions. 

## Compatibility Matrix
Please follow the compatibility matrix below to determine the required combination of software components necessary to run the toolbox. 

Software        |Suported  |Not Supported
---             |---       |---          
ArcGIS Pro      |2.5       |2.6          
ArcMap          |10.7      |10.8         
R               |3.6       |![](https://img.shields.io/badge/-4.0-red)          
R-bridge        |1.0.1.239 |![](https://img.shields.io/badge/-1.0.1.241-red)  
FluvialGeomorph |0.1.41    |0.1.41             

***

# FluvialGeomorph v0.1.40 (Release date: 2020-09-27)

## Major Changes
* None.

## Bug fixes
* Fixed a bug that prevented the Level 1 and 2 reports from displaying slope. 
* Adjusted the `loess_span` default values. 

## Compatibility Matrix
Please follow the compatibility matrix below to determine the required combination of software components necessary to run the toolbox. 

Software        |Suported  |Not Supported
---             |---       |---          
ArcGIS Pro      |2.5       |2.5          
ArcMap          |10.7      |10.8         
R               |3.6       |![](https://img.shields.io/badge/-4.0-red)          
R-bridge        |1.0.1.239 |![](https://img.shields.io/badge/-1.0.1.241-red)  
FluvialGeomorph |0.1.40    |0.1.40             

**Note: The ArcGIS R-bridge does not yet support R 4.0 for use in ArcGIS Pro or ArcMap geoprocessing tools.**

***

# FluvialGeomorph v0.1.39 (Release date: 2020-09-21)

## Major Changes
* Added the Level 3 Report. 
* Added cross section maps to the Level 1 and Estimate Bankful reports. 

## Bug fixes
* Clarified the x-axis label in the `xs_compare_plot_*` to more clearly communicate the orientation of the cross section. 
* The Level 1, Estimate Bankfull, and Level 2 reports option `Show XS Map` no longer causes the reports to fail. 

## Compatibility Matrix
Please follow the compatibility matrix below to determine the required combination of software components necessary to run the toolbox. 

Software        |Suported  |Not Supported
---             |---       |---          
ArcGIS Pro      |2.5       |2.5          
ArcMap          |10.7      |10.8         
R               |3.6       |![](https://img.shields.io/badge/-4.0-red)          
R-bridge        |1.0.1.239 |![](https://img.shields.io/badge/-1.0.1.241-red)  
FluvialGeomorph |0.1.39    |0.1.39             

**Note: The ArcGIS R-bridge does not yet support R 4.0 for use in ArcGIS Pro or ArcMap geoprocessing tools.**

***

# FluvialGeomorph v0.1.38 (Release date: 2020-09-13)

## Major Changes
* Added a new Level 1 cross sections dimensions tool. This supports the new Level 1 workflow that calculates the dimensions possible at this stage of the analysis. 
* Updated the Level 1 Report with a new cross section metrics graph. 
* Updated the Estimate Bankfull Report cross section graphs to use a square aspect ratio.
* Updated the Level 2 Report cross section graphs to use a wide aspect ratio.
* Added a labeling frequency parameter to all cross section maps and graphs. 
* Updated the Estimate Bankfull and Level 2 reports with the complete list of regions used in the `RegionalCurve` R package. 

## Bug fixes
* Fixed Level 1 graph series order to match Level 2 report series order. 
* Several bug fixes in the `fluvgeo` R package. 
* Caution: The Level 2 Report option `Show XS Map` will cause the report to fail. 

## Compatibility Matrix
Please follow the compatibility matrix below to determine the required combination of software components necessary to run the toolbox. 

Software        |Suported  |Not Supported
---             |---       |---          
ArcGIS Pro      |2.5       |2.5          
ArcMap          |10.7      |10.8         
R               |3.6       |![](https://img.shields.io/badge/-4.0-red)          
R-bridge        |1.0.1.239 |![](https://img.shields.io/badge/-1.0.1.241-red)  
FluvialGeomorph |0.1.38    |0.1.38             

**Note: The ArcGIS R-bridge does not yet support R 4.0 for use in ArcGIS Pro or ArcMap geoprocessing tools.**

***

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

***

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

***

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

***

# FluvialGeomorph v0.1.34 (Release date: 2020-07-27)

## Major Changes
* None.

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

***

# FluvialGeomorph v0.1.33 (Release date: 2020-07-27)

## Major Changes
* None.

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

***

# FluvialGeomorph v0.1.32 (Release date: 2020-07-09)

## Major Changes
* None.

## Bug Fixes
* Overhauled the `R` package install process to make it more robust and secure on a wider range of previous `R` installs. 

***

# FluvialGeomorph v0.1.31 (Release date: 2020-07-06)

## Major Changes
* Tested toolbox to ensure it supports `R` 4.0 on both ArcGIS Pro (2.5) and ArcMap (10.7.1). 

## Bug Fixes
* Fixed a bug that was preventing tools from running in ArcGIS Pro due to an apparent circular dependency reference (`devtools` unable to install `pkgload`). 

***

# FluvialGeomorph v0.1.30 (Release date: 2020-06-30)

## Major Changes
* FluvialGeomorph `R` packages (i.e., `RegionalCurve`, `fluvgeo`) now install directly from GitHub using the `Install R packages` tool. 

## Bug Fixes
* None.

***

# FluvialGeomorph v0.1.29 (Release date: 2020-06-18)

## Major Changes
* Added the `Longitudinal Profile Compare` tool to the Reports toolset. 
* Added the `XS Longitudinal Profile Compare` tool to the Reports toolset.
* Added the `Level 1 Report` tool to the Reports toolset.

## Bug Fixes
* Added the Cole Creek test datasets (2004, 2010, 2016) for tools that need multiple time periods. 

***

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

***

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
