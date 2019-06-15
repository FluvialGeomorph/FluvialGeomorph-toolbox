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
            
    # Con operation to select cells less than detrend_value
    banks = Con(detrend_dem, 0, 1, "value >= " + str(detrend_value))
    
    # Convert the banks raster to a polygon
    arcpy.RasterToPolygon_conversion(
              in_raster = banks, 
              out_polygon_features = "banks_raw_" + 
                                     str(detrend_value).replace(".", "_"),
              simplify = "SIMPLIFY",
              raster_field = "VALUE")
    
    arcpy.AddMessage("Created water surface area feature class")


def main():
    # Call the BankfullPolygon function with command line parameters
    BankfullPolygon(output_workspace, detrend_dem, detrend_value)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    detrend_dem      = arcpy.GetParameterAsText(1)
    detrend_value    = arcpy.GetParameterAsText(2)
    
    main()
