"""____________________________________________________________________________
Script Name:          _21_RASWaterSurface.py
Description:          Calculates the RAS modeled water surface elevation (WSE) 
                      from the input RAS depth raster. 
Date:                 01/09/2020

Usage:


Parameters:
output_workspace (str)-- Path to the output workspace
xs_dims (str)         -- Path to the cross section dimension points feature 
                         class.
RAS_depth (str)       -- Path to the RAS model depth raster.
RAS_model_name (str)  -- Name of the RAS model that the depth raster represents.
                      This name will be used to name the calculated WSE fields. 

Outputs:
Fields are added to the input 
____________________________________________________________________________"""
 
import os
import arcpy
from arcpy.sa import *

def ras_wse(output_workspace, xs_dims, RAS_depth, RAS_model_name):
    # Check out the extension license 
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    arcpy.env.extent = RAS_depth
    arcpy.env.snapRaster = RAS_depth
    arcpy.env.cellSize = arcpy.Describe(RAS_depth).meanCellHeight
    arcpy.env.compression = "LZ77"
    arcpy.env.outputCoordinateSystem = xs_dims    
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("xs_dims: {}".format(arcpy.Describe(xs_dims).baseName))
    arcpy.AddMessage("RAS_depth: {}".format(arcpy.Describe(RAS_depth).baseName))
    arcpy.AddMessage("RAS_model_name: {}".format(str(RAS_model_name)))
    
    # Add the value of the RAS_depth raster to the xs_dims feature class
    depth_field_name = "ras_depth_{}".format(RAS_model_name)
    in_rasters = [[RAS_depth, depth_field_name]]
    arcpy.AddMessage("depth_field_name: {}".format(depth_field_name))
    arcpy.AddMessage("in_rasters: {}".format(in_rasters))
    
    # arcpy.gp.ExtractMultiValuesToPoints_sa("Z:/Work/Office/Regional/ERDC/EMRRP_Sediment/California_Santa_Ana_River/R2.gdb/Yr2_riffle_floodplain_dims_planform_pts", "'Z:/Work/Office/Regional/ERDC/EMRRP_Sediment/California_Santa_Ana_River/RAS_model/2-10yr Raster Depth Grid/Depth (2 YR).sarterrain.tif' Depth__2_YR__sarterrain", "NONE")
    arcpy.sa.ExtractMultiValuesToPoints(in_point_features = xs_dims,
                                        in_rasters = in_rasters)
    
    # Calculate RAS model WSE
    ras_wse_name = "ras_wse_{}".format(RAS_model_name)
    field_names = [f.name for f in arcpy.ListFields(xs_dims)]
    if ras_wse_name not in field_names:
        arcpy.AddField_management(in_table = xs_dims,
                                  field_name = ras_wse_name,
                                  field_type = "DOUBLE")
                                  
    expression = "!watersurface_elev! + !{}!".format(depth_field_name)
    arcpy.AddMessage("expression: {}".format(expression))
    arcpy.CalculateField_management(in_table = xs_dims, 
                                    field = ras_wse_name, 
                                    expression = expression, 
                                    expression_type = "PYTHON_9.3")

def main():
    # Call the ras_wse function with command line parameters
    ras_wse(output_workspace, xs_dims, RAS_depth, RAS_model_name)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    xs_dims          = arcpy.GetParameterAsText(1)
    RAS_depth        = arcpy.GetParameterAsText(2)
    RAS_model_name   = arcpy.GetParameterAsText(3)
    
    main()
