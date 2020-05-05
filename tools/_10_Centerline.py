"""____________________________________________________________________________
Script Name:          _10_Centerline.py
Description:          Creates a stream centerline from a bankfull polygon. 
Date:                 4/19/2018

Usage:
Creates a new feature class representing the centerline of the input bankfull 
polygon.  

Parameters:
output_workspace      -- Path to the output workspace.
dem                   -- Path to the digital elevation model (DEM).
banks_poly            -- Path to a banks polygon representing the channel area 
                         for which slope will be calculated. 
smooth_tolerance      -- The PAEK smoothing tolerance that controls the 
                         calculating of new vertices. Acceptable smoothing 
                         occurs with values between 2 - 5.

Outputs:
centerline            -- a new centerline line feature class
____________________________________________________________________________"""
 
import os
import arcpy
from arcpy.sa import *

def Centerline(output_workspace, dem, banks_poly, smooth_tolerance):
    # Check out the extension license 
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    arcpy.env.extent = dem
    arcpy.env.snapRaster = dem
    arcpy.env.cellSize = 2
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
    
    # Convert the banks polygon to raster
    arcpy.PolygonToRaster_conversion(in_features = banks_poly, 
                                     value_field = "gridcode", 
                                     out_rasterdataset = "banks")
    
    # Thin the banks raster
    stream = arcpy.sa.Thin(in_raster = "banks", 
                           background_value = "ZERO", 
                           filter = "FILTER", 
                           corners = "ROUND")
    
    # Convert the synthetic stream to a centerline feature class
    arcpy.RasterToPolyline_conversion(in_raster = stream, 
                                      out_polyline_features = "centerline_raw",
                                      background_value = "ZERO",
                                      minimum_dangle_length = 10,
                                      simplify = "SIMPLIFY")
    
    # Smooth centerline
    arcpy.SmoothLine_cartography(in_features = "centerline_raw", 
                                 out_feature_class = "centerline", 
                                 algorithm = "PAEK", 
                                 tolerance = smooth_tolerance)
    
    arcpy.AddMessage("Created centerline")
    
    # Return
    arcpy.SetParameter(4, "centerline")
    
    # Cleanup
    arcpy.Delete_management(in_data = "banks")
    arcpy.Delete_management(in_data = "centerline_raw")


def main():
    # Call the ChannelSlope function with command line parameters
    Centerline(output_workspace, dem, banks_poly, smooth_tolerance)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    dem              = arcpy.GetParameterAsText(1)
    banks_poly       = arcpy.GetParameterAsText(2)
    smooth_tolerance = arcpy.GetParameterAsText(3)
    
    main()
