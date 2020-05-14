"""____________________________________________________________________________
Script Name:          _06_StreamProfilePoints.py
Description:          Converts a stream flowline to a route using the 
                      distance to mouth parameter and creates a feature class 
                      of stream profile points. 
Date:                 05/09/2020

Usage:
Creates a new feature class of stream longitudinal profile points with 3D 
information describing points along a stream.  

This tool assumes that there is a field in the flowline feature class 
called `ReachName` that uniquely identifies each stream reach. 

This tool assumes that the stream flowline is digitized in the direction of 
flow. Open an edit session, select the flowline, choose to edit vertices, and
ensure that the red endpoint is at the downstream 
end of the flowline. 

The station distance parameter is specified in the linear units of the 
flowline feature class.

Parameters:
output_workspace      -- Path to the output workspace
flowline              -- Path to the flowline feature class
dem                   -- Path to the digital elevation model (DEM)
km_to_mouth           -- Kilometers to the mouth of the study area outlet.
station_distance      -- Distance between output flowline station points (in 
                         the linear units of the flowline feature class)
calibration_points    -- A point feature class used to calibrate the output 
                         flowline points. 
point_id_field        -- The field that identifies the route on which each 
                         calibration point is located.The values in this field 
                         match those in the route identifier field. This field 
                         can be numeric or character. If using a flowline_points
                         feature class, the id_field is "ReachName".
measure_field         -- The field containing the measure value for each 
                         calibration point. This field must be numeric. If using
                         a flowline_points feature class, the measure_field is 
                         "POINT_M".
search_radius         -- Limits how far a calibration point can be from a route 
                         by specifying the distance and its unit of measure 
                         (e.g., "25 Meters"). If the units of measure are 
                         not specified, the same units as the coordinate system 
                         of the route feature class will be used.

Outputs:
flowline_points        -- a new feature class of densified vertices along the 
                          flowline
____________________________________________________________________________"""
 
from datetime import datetime
import arcpy

# Define the StreamProfilePoints function
def StreamProfilePoints(output_workspace, flowline, dem, km_to_mouth, 
                        station_distance, 
                        calibration_points, point_id_field, measure_field,
                        search_radius):
    # Check out the extension licenses 
    arcpy.CheckOutExtension("3D")

    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("flowline: {}".format(arcpy.Describe(flowline).baseName))
    arcpy.AddMessage("km_to_mouth: {}".format(str(km_to_mouth)))
    arcpy.AddMessage("DEM: {}".format(arcpy.Describe(dem).baseName))
    arcpy.AddMessage("Station distance: {}".format(str(station_distance)))
    if calibration_points:
        arcpy.AddMessage("Calibration points: {}".format(str(calibration_points)))
        arcpy.AddMessage("point_id_field: {}".format(str(point_id_field)))
        arcpy.AddMessage("measure_field: {}".format(str(measure_field)))
        arcpy.AddMessage("search_radius: {}".format(str(search_radius)))
    
    # Add a field to hold the linear referencing route from measure
    # Check if the field already exists and if not add it
    field_names = [f.name for f in arcpy.ListFields(flowline)]
    if "from_measure" not in field_names:
        arcpy.AddField_management(in_table = flowline, 
                                  field_name = "from_measure", 
                                  field_type = "DOUBLE")

    # Set the value of the flowline `from_measure` to the input parameter 
    # `km_to_mouth` in units kilometers
    arcpy.CalculateField_management(in_table = flowline, 
                                    field = "from_measure", 
                                    expression = km_to_mouth, 
                                    expression_type = "PYTHON_9.3")

    # Add a field to hold the linear referencing route to measure
    if "to_measure" not in field_names:
        arcpy.AddField_management(in_table = flowline, 
                                  field_name = "to_measure", 
                                  field_type = "DOUBLE")

    # Set the value of the flowline `to_measure` to the length of the flowline
    # in units kilometers plus the value of km_to_mouth 
    expression = "!shape.length@kilometers! + {}".format(str(km_to_mouth))
    
    arcpy.CalculateField_management(in_table = flowline, 
                                    field = "to_measure", 
                                    expression = expression, 
                                    expression_type = "PYTHON_9.3")

    # Simplify the flowline to speed interpolation
    arcpy.SimplifyLine_cartography(in_features = flowline, 
                                   out_feature_class = "flowline_simplify", 
                                   algorithm = "POINT_REMOVE", 
                                   tolerance = "1 Feet")
    arcpy.AddMessage("Simplified flowline: flowline_simplify")
    
    # Densify vertices of the flowline_simplify feature class using the Densify tool.
    arcpy.CopyFeatures_management(in_features = "flowline_simplify", 
                                  out_feature_class = "flowline_densify")
    arcpy.Densify_edit(in_features = "flowline_densify", 
                       densification_method = "DISTANCE", 
                       distance = station_distance)
    arcpy.AddMessage("Densified verticies of flowline: flowline_densify")

    # Convert the flowline feature class to a route
    arcpy.CreateRoutes_lr(in_line_features = "flowline_densify", 
                          route_id_field = "ReachName", 
                          out_feature_class = "flowline_densify_route", 
                          measure_source = "TWO_FIELDS", 
                          from_measure_field = "from_measure", 
                          to_measure_field = "to_measure")
    arcpy.AddMessage("Converted densfied flowline to a route: "
                     "flowline_densify_route")
    
    # Calibrate route
    if calibration_points:
        arcpy.CalibrateRoutes_lr(in_route_features = "flowline_densify_route", 
                                 route_id_field = "ReachName", 
                                 in_point_features = calibration_points,
                                 point_id_field = point_id_field,
                                 measure_field = measure_field,
                                 out_feature_class = "flowline_route_calibrate",
                                 calibrate_method = "DISTANCE",
                                 search_radius = search_radius)
        arcpy.CopyFeatures_management(in_features = "flowline_route_calibrate", 
                                  out_feature_class = "flowline_densify_route")
        arcpy.AddMessage("Calibrated route")
    
    # Convert flowline feature vertices to points
    arcpy.FeatureVerticesToPoints_management(
                     in_features = "flowline_densify_route", 
                     out_feature_class = "flowline_points")
    arcpy.AddMessage("Converted densified flowline route to points: "
                     "flowline_points")

    # Add x, y, z, and m values to the `flowline_points` feature class
    arcpy.AddGeometryAttributes_management(Input_Features = "flowline_points", 
                                           Geometry_Properties = "POINT_X_Y_Z_M", 
                                           Length_Unit = "METERS")

    # Set the first m-value for the flowline_points to zero. The `create 
    # route` tool sets it to NULL. 
    # Create code block that inserts the km_to_mouth value for the NULL record
    # (the first record) 
    #arcpy.AddMessage("Set Null m-values to zero - start: {}".format(datetime.now().strftime("%H:%M:%S")))
    
    codeBlock = """def setNull2Zero(m):
                       if m is None: 
                           return {}
                       else:
                           return m""".format(km_to_mouth)
    arcpy.CalculateField_management(in_table = "flowline_points", 
                                field = "POINT_M", 
                                expression = "setNull2Zero(!POINT_M!)", 
                                code_block = codeBlock,
                                expression_type = "PYTHON_9.3")
    #arcpy.AddMessage("Set Null m-values to zero - end: {}".format(datetime.now().strftime("%H:%M:%S")))

    # Delete un-needed fields
    arcpy.DeleteField_management(in_table = "flowline_points", 
                                 drop_field = ["ORIG_FID","POINT_Z"])

    # Add elevations to the `flowline_points` feature class
    arcpy.AddSurfaceInformation_3d(in_feature_class = "flowline_points", 
                                   in_surface = dem, 
                                   out_property = "Z",
                                   z_factor = 1.0)
    arcpy.AddMessage("Added geometry fields to flowline points.")
    
    # Return
    arcpy.SetParameter(5, "flowline_points")
    
    # Cleanup
    arcpy.Delete_management(in_data = "flowline_simplify")
    arcpy.Delete_management(in_data = "flowline_simplify_Pnt")
    arcpy.Delete_management(in_data = "flowline_densify")
    arcpy.Delete_management(in_data = "flowline_route_calibrate")
    arcpy.Delete_management(in_data = "flowline_densify_route")
    return
    
def main():
    # Call the StreamProfilePoints function with command line parameters
    StreamProfilePoints(output_workspace, flowline, dem, km_to_mouth, 
                        station_distance, 
                        calibration_points, point_id_field, measure_field,
                        search_radius)

if __name__ == "__main__":
    # Get input parameters
    output_workspace   = arcpy.GetParameterAsText(0)
    flowline           = arcpy.GetParameterAsText(1)
    dem                = arcpy.GetParameterAsText(2)
    km_to_mouth        = arcpy.GetParameterAsText(3)
    station_distance   = arcpy.GetParameterAsText(4)
    calibration_points = arcpy.GetParameterAsText(5)
    point_id_field     = arcpy.GetParameterAsText(6)
    measure_field      = arcpy.GetParameterAsText(7)
    search_radius      = arcpy.GetParameterAsText(8)
    
    main()

