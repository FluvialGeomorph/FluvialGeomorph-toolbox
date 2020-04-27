"""____________________________________________________________________________
Script Name:          _09_ChannelSlope.py
Description:          Calculates the slope within a stream channel. 
Date:                 11/26/2017

Usage:

Parameters:
output_workspace (str)-- Path to the output workspace
dem (str)             -- Path to the digital elevation model (DEM).
banks_poly (str)      -- Path to a banks polygon representing the channel area 
                         for which slope will be calculated. 

Outputs:
channel_slope         -- a new channel slope raster
____________________________________________________________________________"""
 
import os
import arcpy
from arcpy.sa import *

def ChannelSlope(output_workspace, dem, banks_poly):
    # Check out the extension license 
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    arcpy.env.extent = dem
    arcpy.env.snapRaster = dem
    arcpy.env.cellSize = arcpy.Describe(dem).meanCellHeight
    arcpy.env.compression = "LZ77"
    arcpy.env.outputCoordinateSystem = dem    
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("DEM: "
                     "{}".format(arcpy.Describe(dem).baseName))
    arcpy.AddMessage("Banks polygon: "
                     "{}".format(arcpy.Describe(banks_poly).baseName))
    
    # Set the environment mask to the banks_poly to clip results to channel
    arcpy.env.mask = banks_poly
    
    # Calculate slope raster
    channel_slope = arcpy.sa.Slope(in_raster = dem, 
                                   output_measurement = "DEGREE", 
                                   z_factor = 0.3048)
    
    channel_slope = os.path.join(output_workspace, "channel_slope")
    arcpy.CopyRaster_management(in_raster = channel_slope, 
                                out_rasterdataset = channel_slope)
    
    arcpy.AddMessage("Created slope raster")
    
    # Return
    arcpy.SetParameter(3, channel_slope)


def main():
    # Call the ChannelSlope function with command line parameters
    ChannelSlope(output_workspace, dem, banks_poly)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    dem              = arcpy.GetParameterAsText(1)
    banks_poly       = arcpy.GetParameterAsText(2)
    
    main()
