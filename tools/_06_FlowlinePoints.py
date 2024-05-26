"""____________________________________________________________________________
Script Name:          _06_FlowlinePoints.py
Description:          Converts a stream flowline to a route using the 
                      distance to mouth parameter and creates a feature class 
                      of stream profile points. 
Date:                 05/27/2020

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
feature_dataset       -- Path to the feature dataset
flowline              -- Path to the flowline feature class
dem                   -- Path to the digital elevation model (DEM)
km_to_mouth           -- Kilometers to the mouth of the study area outlet.
station_distance      -- Distance between output flowline station points (in 
                         the linear units of the flowline feature class). If 
                         station_distance is set to zero, the original vertices
                         of the flowline will be preserved. 
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
flowline_points        -- a flowline_points feature class
____________________________________________________________________________"""
 
import os
from datetime import datetime
import arcpy

def FlowlinePoints(feature_dataset, flowline, dem, km_to_mouth, 
                   station_distance, 
                   calibration_points, point_id_field, measure_field,
                   search_radius):
    # Check out the extension licenses 
    arcpy.CheckOutExtension("3D")

    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    
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
    
    # Add fields to hold the linear referencing route from and to measures
    field_names = [f.name for f in arcpy.ListFields(flowline)]
    if "from_measure" not in field_names:
        arcpy.management.AddField(in_table = flowline, 
                                  field_name = "from_measure", 
                                  field_type = "DOUBLE")
                                  
    if "to_measure" not in field_names:
        arcpy.management.AddField(in_table = flowline, 
                                  field_name = "to_measure", 
                                  field_type = "DOUBLE")
                                  
    arcpy.AddMessage("Added required fields to flowline.")
                                  
    # Set the value of the flowline `from_measure` to the input parameter 
    # `km_to_mouth` in units kilometers
    arcpy.management.CalculateField(in_table = flowline, 
                                    field = "from_measure", 
                                    expression = km_to_mouth, 
                                    expression_type = "PYTHON3")

    # Set the value of the flowline `to_measure` to the length of the flowline
    # in units kilometers plus the value of km_to_mouth 
    expression = "!shape.length@kilometers! + {}".format(str(km_to_mouth))
    arcpy.management.CalculateField(in_table = flowline, 
                                    field = "to_measure", 
                                    expression = expression, 
                                    expression_type = "PYTHON3")
    arcpy.AddMessage("Calculated flowline from and to measures.")

    # Set the station distance
    if int(station_distance) == 0:
        # If station_distance is zero, use original flowline vertices unchanged
        arcpy.management.CopyFeatures(in_features = flowline, 
                                      out_feature_class = "flowline_vertices")
        arcpy.AddMessage("Vertices of flowline not changed.")
    else:
        # Simplify the flowline (speeds processing)
        arcpy.cartography.SimplifyLine(in_features = flowline, 
                                       out_feature_class = "flowline_simplify",
                                       algorithm = "POINT_REMOVE", 
                                       tolerance = "1 Feet")
        arcpy.AddMessage("Simplified flowline.")
        
        # Set the station distance by densifying vertices to station_distance
        arcpy.management.CopyFeatures(in_features = "flowline_simplify", 
                                      out_feature_class = "flowline_vertices")
        arcpy.edit.Densify(in_features = "flowline_vertices", 
                           densification_method = "DISTANCE", 
                           distance = station_distance)
        arcpy.AddMessage("Densified verticies of flowline to station_distance.")
    
    # Convert the flowline to a route
    arcpy.lr.CreateRoutes(in_line_features = "flowline_vertices", 
                          route_id_field = "ReachName", 
                          out_feature_class = "flowline_route", 
                          measure_source = "TWO_FIELDS", 
                          from_measure_field = "from_measure", 
                          to_measure_field = "to_measure")
    arcpy.AddMessage("Converted flowline to route.")

    if not calibration_points:
        arcpy.AddMessage("No flowline_route calibration required.")

        # Convert flowline_route vertices to flowline_points
        flowline_points = os.path.join(feature_dataset, "flowline_points")
        arcpy.management.FeatureVerticesToPoints(
                             in_features = "flowline_route", 
                             out_feature_class = flowline_points)
        arcpy.AddMessage("Converted flowline_route to flowline_points.")
    
        # Add x, y, and m values to the `flowline_points` feature class
        arcpy.management.CalculateGeometryAttributes(
                              in_features = flowline_points, 
                              geometry_property = [["POINT_X", "POINT_X"], 
                                                   ["POINT_Y", "POINT_Y"],
                                                   ["POINT_M", "POINT_M"]],
                              length_unit = "METERS")
        arcpy.AddMessage("Calculated flowline_points X, Y, and M attributes.")
    
        # Calculate the m-values for the uncalibrated route
        arcpy.management.AddField(in_table = flowline_points, 
                                  field_name = "POINT_M_uncalibrated", 
                                  field_type = "DOUBLE")
        arcpy.management.CalculateField(in_table = flowline_points, 
                                        field = "POINT_M_uncalibrated", 
                                        expression = "!POINT_M!", 
                                        expression_type = "PYTHON3")
        arcpy.AddMessage("Calculated m-values for the uncalibrated route.")

    if calibration_points:
        arcpy.AddMessage("flowline_route calibration required.")
        
        # Calibrate flowline_route using calibration points
        arcpy.lr.CalibrateRoutes(in_route_features = "flowline_route", 
                                 route_id_field = "ReachName", 
                                 in_point_features = calibration_points,
                                 point_id_field = point_id_field,
                                 measure_field = measure_field,
                                 out_feature_class = "flowline_route_calibrate",
                                 calibrate_method = "DISTANCE",
                                 search_radius = search_radius)
        arcpy.AddMessage("Calibrated flowline_route using calibration_points.")
        
        # Convert flowline_route vertices to flowline_points
        flowline_points = os.path.join(feature_dataset, "flowline_points")
        arcpy.management.FeatureVerticesToPoints(
                             in_features = "flowline_route_calibrate", 
                             out_feature_class = flowline_points)
        arcpy.AddMessage("Converted flowline_route_calibrate to flowline_points.")
        
        # Add x, y, and m values to the `flowline_points` feature class
        arcpy.management.CalculateGeometryAttributes(
                             in_features = flowline_points, 
                             geometry_property = [["POINT_X", "POINT_X"], 
                                                  ["POINT_Y", "POINT_Y"],
                                                  ["POINT_M", "POINT_M"]],
                             length_unit = "METERS")
        arcpy.AddMessage("Calculated flowline_points X, Y, and M attributes.")
        
        # Calculate the m-value for the uncalibrated route
        fl_pts_uncalibrated = os.path.join(arcpy.env.workspace, 
                                           "fl_pts_uncalibrated")
        arcpy.lr.LocateFeaturesAlongRoutes(
                 in_features = flowline_points, 
                 in_routes = "flowline_route", 
                 route_id_field = "ReachName", 
                 radius_or_tolerance = station_distance, 
                 out_table = fl_pts_uncalibrated, 
                 out_event_properties = "ReachName POINT POINT_M_uncalibrated")
        arcpy.AddMessage("Calculated m-values for the uncalibrated route.")
    
        arcpy.management.JoinField(in_data = flowline_points, 
                                   in_field = "OBJECTID", 
                                   join_table = fl_pts_uncalibrated, 
                                   join_field = "OBJECTID",
                                   fields = ["POINT_M_uncalibrated"])
        arcpy.AddMessage("Uncalibrated m-value joined to flowline_points.")

    # Delete un-needed fields
    arcpy.management.DeleteField(in_table = flowline_points, 
                                 drop_field = ["ORIG_FID"])
    
    # Calculate difference between calibrated and uncalibrated m-values
    arcpy.management.AddField(in_table = flowline_points, 
                              field_name = "calibration_diff", 
                              field_type = "DOUBLE")
    arcpy.management.CalculateField(
                          in_table = flowline_points, 
                          field = "calibration_diff", 
                          expression = "!POINT_M! - !POINT_M_uncalibrated!", 
                          expression_type = "PYTHON3")
    arcpy.AddMessage("Calculated calibration difference.")

    # Add elevations to the `flowline_points` feature class
    arcpy.ddd.AddSurfaceInformation(in_feature_class = flowline_points, 
                                    in_surface = dem, 
                                    out_property = "Z",
                                    z_factor = 1.0)
    arcpy.AddMessage("Added DEM elevation to flowline_points.")
    
    # Return
    arcpy.SetParameter(9, flowline_points)
    
    # Cleanup
    #arcpy.management.Delete(fl_pts_uncalibrated)
    return
    
def main():
    FlowlinePoints(feature_dataset, flowline, dem, km_to_mouth, 
                   station_distance, 
                   calibration_points, point_id_field, measure_field,
                   search_radius)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset    = arcpy.GetParameterAsText(0)
    flowline           = arcpy.GetParameterAsText(1)
    dem                = arcpy.GetParameterAsText(2)
    km_to_mouth        = arcpy.GetParameterAsText(3)
    station_distance   = arcpy.GetParameterAsText(4)
    calibration_points = arcpy.GetParameterAsText(5)
    point_id_field     = arcpy.GetParameterAsText(6)
    measure_field      = arcpy.GetParameterAsText(7)
    search_radius      = arcpy.GetParameterAsText(8)
    
    main()
