# FluvialGeomorph v0.1.27 (Release date: 2020-05-14)

## Major Changes
* Added the `Point Watershed` tool that allows a user to calculate the upstream contributing area for each point in the input point feature class. Optionally, it allows land cover to be summarized for each contributing watershed. 

* Added the `Contributing Area D8` tool to support delineating watersheds using the new `Point Watershed` tool. It produces a D8 flow direction raster needed for watershed delineation. 

* Added the `XS Compare Plot` to allow users to create a cross section plot for multiple survey time periods. 

* Updated the `Burn Cutlines` tool to allow for widening the cut made by each cutline. 
* Removed the `Point Landcover` tool. This tool was replaced by the functionality in the `Point Watershed` tool. 

## Bug Fixes
* Updated the help text for all tools. 

