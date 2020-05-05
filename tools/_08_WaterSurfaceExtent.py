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
output_workspace      -- Path to the output workspace.
detrend_dem           -- Path to the detrended digital elevation model (DEM).
detrend_value         -- Detrended elevation value used to define the 
                         innundated area. All raster values below this value
                         will be extracted to a polygon. 
smoothing             -- Smoothing factor (0, no smoothing - 5, high smoothing)

Outputs:
banks                 -- a new polygon feature class representing the area 
                         innundated by the specified detrend_value
____________________________________________________________________________"""
 
import os
import string
import arcpy
from arcpy.sa import *

def BankfullPolygon(output_workspace, detrend_dem, detrend_value, smoothing):
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
    arcpy.AddMessage("Smoothing: {}".format(str(smoothing)))
            
    # Select cells less than detrend_value
    arcpy.AddMessage("Selecting cells <= {}".format(str(detrend_value)))
    banks = Con(detrend_dem, 0, 1, "value >= " + str(detrend_value))

    # Smooth the banks raster
    arcpy.AddMessage("Smoothing banks raster")
    i = 1
    while i <= int(smoothing):
        banks = MajorityFilter(banks, number_neighbors = "EIGHT", 
                                      majority_definition = "HALF")
        arcpy.AddMessage("Completed majority filter: {}".format(str(i)))
        i += 1
    
    # Clean the edges of the banks
    arcpy.AddMessage("Cleaning bank boundaries")
    banks_clean = BoundaryClean(banks, sort_type = "DESCEND", 
                                number_of_runs = "TWO_WAY")
    arcpy.AddMessage("Bank boundaries cleaned")
    
    # Convert the banks raster to a polygon
    banks_raw = "banks_raw_" + str(detrend_value).replace(".", "_")
    arcpy.RasterToPolygon_conversion(
              in_raster = banks_clean, 
              out_polygon_features = banks_raw,
              simplify = "SIMPLIFY",
              raster_field = "VALUE")
    arcpy.AddMessage("Created water surface area feature class: " + 
                     banks_raw)
    
    # Return
    arcpy.SetParameter(4, banks_raw)


def main():
    # Call the BankfullPolygon function with command line parameters
    BankfullPolygon(output_workspace, detrend_dem, detrend_value, smoothing)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    detrend_dem      = arcpy.GetParameterAsText(1)
    detrend_value    = arcpy.GetParameterAsText(2)
    smoothing        = arcpy.GetParameterAsText(3)
    
    main()


