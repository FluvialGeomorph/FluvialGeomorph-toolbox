"""____________________________________________________________________________
Script Name:          _10_Centerline.py
Description:          Creates a stream centerline from a bankfull polygon. 
Date:                 4/19/2018

Usage:
Creates a new feature class representing the centerline of the input bankfull 
polygon.  

Parameters:
feature_dataset       -- Path to the feature dataset.
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

def Centerline(feature_dataset, dem, banks_poly, smooth_tolerance):
    # Check out the extension license 
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    arcpy.env.extent = dem
    arcpy.env.snapRaster = dem
    arcpy.env.cellSize = 2
    arcpy.env.compression = "LZ77"
    arcpy.env.outputCoordinateSystem = dem    
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("DEM: {}".format(arcpy.Describe(dem).baseName))
    arcpy.AddMessage("Banks polygon: "
                     "{}".format(arcpy.Describe(banks_poly).baseName))
    
    # Set the environment mask to the banks_poly to clip results to channel
    arcpy.env.mask = banks_poly
    
    # Convert the banks polygon to raster
    banks_path = os.path.join(arcpy.env.workspace, "banks")
    arcpy.PolygonToRaster_conversion(in_features = banks_poly, 
                                     value_field = "gridcode", 
                                     out_rasterdataset = banks_path)
    arcpy.AddMessage("Converted the banks polygon to a raster.")
    
    # Thin the banks raster
    stream = arcpy.sa.Thin(in_raster = "banks", 
                           background_value = "ZERO", 
                           filter = "FILTER", 
                           corners = "ROUND")
    arcpy.AddMessage("Used the Thin tool on the banks raster.")
    
    # Convert the synthetic stream to a centerline feature class
    cl_raw_path = os.path.join(feature_dataset, "centerline_raw")
    arcpy.RasterToPolyline_conversion(in_raster = stream, 
                                      out_polyline_features = cl_raw_path,
                                      background_value = "ZERO",
                                      minimum_dangle_length = 10,
                                      simplify = "SIMPLIFY")
    arcpy.AddMessage("Convert thinned raster stream to a polyline.")
    
    # Smooth centerline
    centerline_path = os.path.join(feature_dataset, "centerline")
    arcpy.SmoothLine_cartography(in_features = cl_raw_path, 
                                 out_feature_class = centerline_path, 
                                 algorithm = "PAEK", 
                                 tolerance = smooth_tolerance)
    arcpy.AddMessage("Smoothed centerline")
    
    # Return
    arcpy.SetParameter(4, centerline_path)
    
    # Cleanup
    arcpy.Delete_management(in_data = banks_path)
    arcpy.Delete_management(in_data = cl_raw_path)


def main():
    # Call the ChannelSlope function with command line parameters
    Centerline(feature_dataset, dem, banks_poly, smooth_tolerance)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset  = arcpy.GetParameterAsText(0)
    dem              = arcpy.GetParameterAsText(1)
    banks_poly       = arcpy.GetParameterAsText(2)
    smooth_tolerance = arcpy.GetParameterAsText(3)
    
    main()
