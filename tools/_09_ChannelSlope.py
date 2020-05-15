"""____________________________________________________________________________
Script Name:          _09_ChannelSlope.py
Description:          Calculates the slope within a stream channel. 
Date:                 05/14/2020

Usage:

Parameters:
output_workspace (str)-- Path to the output workspace.
dem (str)             -- Path to the digital elevation model (DEM).
banks_poly (str)      -- Path to a banks polygon representing the channel area 
                         for which slope will be calculated. 
z_factor              -- Number of ground x,y units in one surface z unit. The 
                         z-factor adjusts the units of measure for the z units 
                         when they are different from the x,y units of the input 
                         surface. The z-values of the input surface are 
                         multiplied by the z-factor when calculating the final 
                         output surface. 
                         
                         If the x,y units and z units are in the same units of 
                         measure, the z-factor is 1. This is the default.
                         
                         If the x,y units and z units are in different units of 
                         measure, the z-factor must be set to the appropriate 
                         factor, or the results will be incorrect. For example, 
                         if your z units are feet and your x,y units are meters, 
                         you would use a z-factor of 0.3048 to convert your 
                         z units from feet to meters (1 foot = 0.3048 meter).

Outputs:
channel_slope         -- a new channel slope raster
____________________________________________________________________________"""
 
import os
import arcpy
from arcpy.sa import *

def ChannelSlope(output_workspace, dem, banks_poly, z_factor):
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
    arcpy.AddMessage("z-factor: {}".format(z_factor))
    
    # Set the environment mask to the banks_poly to clip results to channel
    arcpy.env.mask = banks_poly
    
    # Calculate slope raster
    arcpy.AddMessage("Calculating channel slope...")
    channel_slope = arcpy.sa.Slope(in_raster = dem, 
                                   output_measurement = "DEGREE", 
                                   z_factor = z_factor)
    
    channel_slope_path = os.path.join(output_workspace, "channel_slope")
    arcpy.CopyRaster_management(in_raster = channel_slope, 
                                out_rasterdataset = channel_slope_path)
    
    arcpy.AddMessage("Created slope raster")
    
    # Return
    arcpy.SetParameter(4, channel_slope_path)


def main():
    # Call the ChannelSlope function with command line parameters
    ChannelSlope(output_workspace, dem, banks_poly, z_factor)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    dem              = arcpy.GetParameterAsText(1)
    banks_poly       = arcpy.GetParameterAsText(2)
    z_factor         = arcpy.GetParameterAsText(3)
    
    main()
