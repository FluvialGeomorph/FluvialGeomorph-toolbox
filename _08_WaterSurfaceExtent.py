"""____________________________________________________________________________
Script Name:          _08_WaterSurfaceExtent.py
Description:          Extracts a water surface extent polygon from a detrended 
                      DEM. 
Date:                 06/02/2019

Usage:
This tool is based on the detrending method used in the River Bathymetry 
Toolkit (RBT) http://essa.com/tools/river-bathymetry-toolkit-rbt/. 

This tool produces a polygon representing the area innundated by the 
detrended elevation value specified. 

Parameters:
output_workspace (str)-- Path to the output workspace
detrend_dem (str)     -- Path to the detrended digital elevation model (DEM)
detrend_value (double)-- Detrended elevation value used to define the 
                         innundated area. All raster values below this value
                         will be extracted to a polygon. 

Outputs:
banks                 -- a new polygon feature class representing the area 
                         innundated by the specified detrend_value
____________________________________________________________________________"""
 
import os
import string
import arcpy
from arcpy.sa import *

def BankfullPolygon(output_workspace, detrend_dem, detrend_value):
    # Check out the extension license 
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    arcpy.env.extent = detrend_dem
    arcpy.env.snapRaster = detrend_dem
    arcpy.env.cellSize = arcpy.Describe(detrend_dem).meanCellHeight
    arcpy.env.compression = "LZ77"
    arcpy.env.outputCoordinateSystem = detrend_dem    
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Detrended DEM: "
                     "{}".format(arcpy.Describe(detrend_dem).baseName))
    arcpy.AddMessage("Detrend Value: {}".format(str(detrend_value)))
            
    # Select cells less than detrend_value
    banks = Con(detrend_dem, 0, 1, "value >= " + str(detrend_value))
    arcpy.AddMessage("Selected cells <= " + str(detrend_value))
    
    # Majority filter five times
    arcpy.AddMessage("Filtering bank boundaries")
    banks_maj1 = MajorityFilter(banks, number_neighbors = "EIGHT", 
                                majority_definition = "HALF")
    arcpy.AddMessage("Filter 1 of 5")
    banks_maj2 = MajorityFilter(banks_maj1, number_neighbors = "EIGHT", 
                                majority_definition = "HALF")
    arcpy.AddMessage("Filter 2 of 5")
    banks_maj3 = MajorityFilter(banks_maj2, number_neighbors = "EIGHT", 
                                majority_definition = "HALF")
    arcpy.AddMessage("Filter 3 of 5")
    banks_maj4 = MajorityFilter(banks_maj3, number_neighbors = "EIGHT", 
                                majority_definition = "HALF")
    arcpy.AddMessage("Filter 4 of 5")
    banks_maj5 = MajorityFilter(banks_maj4, number_neighbors = "EIGHT", 
                                majority_definition = "HALF")
    arcpy.AddMessage("Filter 5 of 5")
    
    # Clean the edges of the banks
    arcpy.AddMessage("Cleaning bank boundaries")
    banks_clean = BoundaryClean(banks_maj5, sort_type = "DESCEND", 
                                number_of_runs = "TWO_WAY")
    arcpy.AddMessage("Bank boundaries cleaned")
    
    # Convert the banks raster to a polygon
    out_feature_class = "banks_raw_" + str(detrend_value).replace(".", "_")
    arcpy.RasterToPolygon_conversion(
              in_raster = banks_clean, 
              out_polygon_features = out_feature_class,
              simplify = "SIMPLIFY",
              raster_field = "VALUE")
    arcpy.AddMessage("Created water surface area feature class: " + 
                     out_feature_class)


def main():
    # Call the BankfullPolygon function with command line parameters
    BankfullPolygon(output_workspace, detrend_dem, detrend_value)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    detrend_dem      = arcpy.GetParameterAsText(1)
    detrend_value    = arcpy.GetParameterAsText(2)
    
    main()
