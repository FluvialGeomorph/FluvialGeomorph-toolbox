# FluvialGeomorph v0.1.27 (Release date: 2020-05-14)

## Major Changes
* Updated the `Stream Profile Points` tool to support route calibration. Now a "mile marker" point feature class can be specified and the output points will be stationed according to these "mile markers". This supports analysis of large rivers with established stationing and change analysis where the same stream is surveyed at multiple time periods, but the stationing of a base year is used for comparison. 

* Added the `Point Watershed` tool that allows a user to calculate the upstream contributing area for each point in the input point feature class. Optionally, it allows land cover to be summarized for each contributing watershed. 

* Added the `Contributing Area D8` tool to support delineating watersheds using the new `Point Watershed` tool. It produces a D8 flow direction raster needed for watershed delineation. 

* Added the `XS Compare Plot` to allow users to create a cross section plot for multiple survey time periods. 

* Updated the `Burn Cutlines` tool to allow for widening the cut made by each cutline. 
* Removed the `Point Landcover` tool. This tool was replaced by the functionality in the `Point Watershed` tool. 

## Bug Fixes
* Fixed bug in `Burn Cutlines` when `widen_cells` = 0. 

* Updated the help text for all tools. 

