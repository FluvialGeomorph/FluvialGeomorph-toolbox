"""____________________________________________________________________________
Script Name:          _03a_ContributingAreaD8.py
Description:          Calculates D8 flow accumulation and flow direction 
                      rasters from an input DEM. 
Date:                 05/14/2020

Usage:
This tool calculates Flow Direction and Flow Accumulation using the D8 method 
from a hydro modified digital elevation model (DEM). 

The ESRI Watershed tool requires a flow direction raster to be calculated using 
the D8 method. Therefore, this tool is intentended to be used prior to the 
FluvialGeomorph Point Watershed tool. 

Parameters:
output_workspace      -- Path to the output workspace. 
dem_hydro             -- Path to the hydro modified digital elevation model (DEM). 
processes             -- The number of processes to use for parallel processing.

Outputs:
contributing_area_D8  -- an flow accumulation raster using the D* method. Units 
                         are the linear units of the input DEM. ESRI refers to 
                         this as a flow accumulation raster. 
flow_direction_D8     -- A flow direction raster using the D8 method (integer 
                         flow directions). 
____________________________________________________________________________"""
 
import os
import arcpy
from arcpy.sa import *

def StudyAreaWatershed(output_workspace, dem_hydro, processes):
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    arcpy.env.scratchWorkspace = output_workspace
    arcpy.env.cellSize = dem_hydro
    arcpy.env.parallelProcessingFactor = processes

    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("DEM hydro: "
                     "{}".format(arcpy.Describe(dem_hydro).baseName))
    
    # Fill sinks
    arcpy.AddMessage("Beginning filling sinks...")
    dem_fill = arcpy.sa.Fill(in_surface_raster = dem_hydro)
    arcpy.AddMessage("Fill sinks complete.")
    
    # Calculate D8 flow direction (suitable for input into the Watershed tool)
    arcpy.AddMessage("Beginning flow direction...")
    flow_dir_d8 = arcpy.sa.FlowDirection(in_surface_raster = dem_fill, 
                                         flow_direction_type = "D8")
    arcpy.CopyRaster_management(in_raster = flow_dir_d8, 
                                out_rasterdataset = "flow_direction_d8")
    # Calculate raster statistics and build pyramids
    arcpy.AddMessage("    Calculating statistics...")
    arcpy.CalculateStatistics_management(os.path.join(output_workspace, 
                                                      "flow_direction_d8"))
    arcpy.AddMessage("    Building pyraminds...")
    arcpy.BuildPyramids_management(os.path.join(output_workspace, 
                                                      "flow_direction_d8"))
    arcpy.AddMessage("Flow direction complete.")
    
    # Calculate flow accumulation
    arcpy.AddMessage("Beginning flow accumulation...")
    flow_accum_d8 = arcpy.sa.FlowAccumulation(flow_dir_d8, 
                                              data_type = "FLOAT", 
                                              flow_direction_type = "D8")
    arcpy.CopyRaster_management(in_raster = flow_accum_d8, 
                                out_rasterdataset = "flow_accumulation_d8")
    # Calculate raster statistics and build pyramids
    arcpy.AddMessage("    Calculating statistics...")
    arcpy.CalculateStatistics_management(os.path.join(output_workspace, 
                                                      "flow_accumulation_d8"))
    arcpy.AddMessage("    Building pyraminds...")
    arcpy.BuildPyramids_management(os.path.join(output_workspace, 
                                                      "flow_accumulation_d8"))
    arcpy.AddMessage("Flow accumulation complete.")
    
    # Return
    #arcpy.SetParameter(3, flow_dir_d8)    

def main():
    # Call the StudyAreaWatershed function with command line parameters
    StudyAreaWatershed(output_workspace, dem_hydro, processes)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    dem_hydro        = arcpy.GetParameterAsText(1)
    processes        = arcpy.GetParameterAsText(2)

    main()

