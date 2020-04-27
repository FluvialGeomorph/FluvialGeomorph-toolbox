"""____________________________________________________________________________
Script Name:          _07_DetrendDEM.py
Description:          Creates a detrended DEM. 
Date:                 01/14/2020

Usage:
This tool is based on the detrending method used in the River Bathymetry Toolkit (RBT) http://essa.com/tools/river-bathymetry-toolkit-rbt/. 

Parameters:
output_workspace (str)-- Path to the output workspace.
flowline (str)        -- Path to the flowline feature class.
flowline_points (str) -- Path to the flowline_points feature class.
dem (str)             -- Path to the digital elevation model (DEM).
buffer_distance (int) -- Distance the flowline_points feature class will be 
                         buffered to define the extent of the output 
                         detrended DEM. Units are defined by the coordinate 
                         system of the DEM. 

Outputs:
detrend               -- a new detrended DEM
____________________________________________________________________________"""
 
import os
from datetime import datetime
import arcpy
from arcpy.sa import *

def DetrendDEM(output_workspace, flowline, flowline_points, dem, buffer_distance):
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
    arcpy.AddMessage("Flowline: "
                     "{}".format(arcpy.Describe(flowline).baseName))
    arcpy.AddMessage("Flowline Points: "
                     "{}".format(arcpy.Describe(flowline_points).baseName))
    arcpy.AddMessage("DEM: {}".format(arcpy.Describe(dem).baseName))
    arcpy.AddMessage("Buffer Distance: {}".format(str(buffer_distance)))
    
    # Buffer the flowline_points
    #arcpy.AddMessage("Buffering flowline start: {}".format(datetime.now().strftime("%H:%M:%S")))
    flowline_buffer = os.path.join(output_workspace, "flowline_buffer")
    arcpy.Buffer_analysis(in_features = flowline, 
                          out_feature_class = flowline_buffer, 
                          buffer_distance_or_field = buffer_distance, 
                          line_side = "FULL", 
                          line_end_type = "ROUND", 
                          dissolve_option = "ALL")
    arcpy.AddMessage("Buffering flowline: complete")

    # Set the environment mask to the flowline_buffer to clip all rasters
    arcpy.AddMessage("Setting mask to flowline_buffer...")
    arcpy.env.mask = flowline_buffer
    arcpy.AddMessage("Setting mask to flowline_buffer: complete")
    
    # Create the trend raster
    arcpy.AddMessage("Creating trend raster...")
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
    
    # Return
    arcpy.SetParameter(5, "detrend")
    
    # Cleanup
    arcpy.Delete_management(in_data = flowline_buffer)
    # arcpy.Delete_management(in_data = trend)
    arcpy.Delete_management(in_data = "trend_smooth")
        

def main():
    # Call the DetrendDEM function with command line parameters
    DetrendDEM(output_workspace, flowline, flowline_points, dem, buffer_distance)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    flowline         = arcpy.GetParameterAsText(1)
    flowline_points  = arcpy.GetParameterAsText(2)
    dem              = arcpy.GetParameterAsText(3)
    buffer_distance  = arcpy.GetParameterAsText(4)
    
    main()
