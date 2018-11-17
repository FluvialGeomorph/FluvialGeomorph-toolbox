"""____________________________________________________________________________
Script Name:          _07_DetrendDEM.py
Description:          Creates a detrended DEM. 
Date:                 11/22/2017

Usage:
This tool is based on the detrending method used in the River Bathymetry Toolkit (RBT) http://essa.com/tools/river-bathymetry-toolkit-rbt/. 

Parameters:
output_workspace (str)-- Path to the output workspace
flowline_points  (str)-- Path to the flowline_points feature class.
dem (str)             -- Path to the digital elevation model (DEM).
buffer_distance (int) -- Distance the flowline_points feature class will be 
                         buffered to define the extent of the output 
                         detrended DEM. Units are defined by the coordinate 
                         system of the DEM. 

Outputs:
detrended              -- a new detrended DEM
____________________________________________________________________________"""
 
import os
import arcpy
from arcpy.sa import *

def DetrendDEM(output_workspace, flowline_points, dem, buffer_distance):
    # Check out the extension license 
    arcpy.CheckOutExtension("3D")
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
    arcpy.AddMessage("Flowline Points: "
                     "{}".format(arcpy.Describe(flowline_points).baseName))
    arcpy.AddMessage("DEM: {}".format(arcpy.Describe(dem).baseName))
    arcpy.AddMessage("Buffer Distance: {}".format(str(buffer_distance)))
    
    # Buffer the flowline_points
    flowline_buffer = os.path.join(output_workspace, "flowline_buffer")
    arcpy.Buffer_analysis(in_features = flowline_points, 
                          out_feature_class = flowline_buffer, 
                          buffer_distance_or_field = buffer_distance, 
                          line_side = "FULL", 
                          line_end_type = "ROUND", 
                          dissolve_option = "ALL")
    
    arcpy.AddMessage("Buffered flowline_points")

    # Set the environment mask to the flowline_buffer to clip all rasters
    arcpy.env.mask = flowline_buffer
    
    # Create the trend raster
    trend = os.path.join(output_workspace, "trend")
    arcpy.Idw_3d(in_point_features = flowline_points, 
                 z_field = "Z", 
                 out_raster = trend, 
                 power = 2, 
                 search_radius = "VARIABLE")
    
    arcpy.AddMessage("Created trend raster")
    
    # Smooth the trend raster
    trend_smooth = arcpy.sa.FocalStatistics(
                             in_raster = trend, 
                             neighborhood = arcpy.sa.NbrCircle(50, "CELL"), 
                             statistics_type = "Mean")
    arcpy.CopyRaster_management(
                      in_raster = trend_smooth, 
                      out_rasterdataset = os.path.join(output_workspace, 
                                                       "trend_smooth"))
    arcpy.AddMessage("Smoothed trend raster")
    
    # Create the detrended raster
    detrend = (Raster(dem) - Raster("trend_smooth")) + float(100)
    arcpy.CopyRaster_management(
                      in_raster = detrend, 
                      out_rasterdataset = os.path.join(output_workspace, 
                                                       "detrend"))
    arcpy.AddMessage("Created detrended raster")
    
    # Calculate raster statistics and build pyramids
    arcpy.CalculateStatistics_management(
              os.path.join(output_workspace, "detrend"))
    arcpy.BuildPyramids_management(
              os.path.join(output_workspace, "detrend"))
    arcpy.AddMessage("Calculated raster statistics and pyramids.")
    
    # Cleanup
    arcpy.Delete_management(in_data = flowline_buffer)
    arcpy.Delete_management(in_data = trend)
    arcpy.Delete_management(in_data = "trend_smooth")
        

def main():
    # Call the DetrendDEM function with command line parameters
    DetrendDEM(output_workspace, flowline_points, dem, buffer_distance)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    flowline_points  = arcpy.GetParameterAsText(1)
    dem              = arcpy.GetParameterAsText(2)
    buffer_distance  = arcpy.GetParameterAsText(3)
    
    main()