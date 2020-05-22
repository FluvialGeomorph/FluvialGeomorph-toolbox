"""____________________________________________________________________________
Script Name:          _14b_BanklinePoints.py
Description:          Converts a stream banklines feature class to a route and 
                      creates a feature class of stream bankline points. 
Date:                 05/22/2020

Usage:
Creates a new feature class of bankline points with 3D information describing 
position along a stream reach.

This tool assumes that there is a field in the bankline feature class 
called `ReachName` that uniquely identifies each stream reach. 

The station distance parameter is specified in the linear units of the 
flowline feature class.

Parameters:
output_workspace      -- Path to the output workspace.
loop_points           -- Path to the loop_points feature class.
banklines             -- Path to the banklines feature class.
valleyline            -- Path to the valleyline feature class.
dem                   -- Path to the digital elevation model (DEM).
station_distance      -- Distance between output bankline station points (in 
                         the linear units of the banklines feature class).

Outputs:
bankline_points       -- a new feature class of vertices along each bankline
                         flowline
____________________________________________________________________________"""
 
import os
import arcpy
from FG_utils import *

def assignLoopAndBend(bankline_loop_points, loop_points):
    """
    Iterates through a feature class of bankline_loop_points and assigns loop 
    and bend values using the values in the loop_points feature class.
    """
    # Iterate through each stream loop
    loops = set([row[0] for row in arcpy.da.SearchCursor(loop_points, "loop")])
    arcpy.AddMessage("Loops: " + str(loops))
    
    for loop in loops:
        arcpy.AddMessage("Loop: " + str(loop))
        
        # Determine the number of bends for this loop
        loop_wc = """{0} = {1} """.format(
                arcpy.AddFieldDelimiters(loop_points, "loop"), str(loop))
        bends = set([row[0] for row in arcpy.da.SearchCursor(loop_points, "bend",
                     where_clause = loop_wc)])
        
        # Determine bank (left or right) of the current loop and bend(s)
        # Ex. sql: "loop" = 1
        bank_wc = """{0} = {1}""".format(
            arcpy.AddFieldDelimiters(loop_points, "loop"), str(loop))
        bank = set([row[0] for row in arcpy.da.SearchCursor(
                   bankline_loop_points, "bank",
                   where_clause = bank_wc)])
        
        # Iterate through each bend in the current loop
        for bend in bends:
            # Skip to the next iteration for bend = 0 (apex point designator)
            if bend == 0:
                continue
            arcpy.AddMessage("Bends: " + str(bends))
            arcpy.AddMessage("  Bend: " + str(bend))
            
            # Determine the current bend start m value
            # Ex. sql: "loop" = 1 AND "bend" = 1 AND "position" = 'start'
            start_wc = """{0} = {1} AND {2} = {3} AND {4} = '{5}'""".format(
                arcpy.AddFieldDelimiters(loop_points, "loop"), str(loop),
                arcpy.AddFieldDelimiters(loop_points, "bend"), str(bend),
                arcpy.AddFieldDelimiters(loop_points, "position"), "start")
            
            m_start = min([row[0] for row in arcpy.da.SearchCursor(
                          bankline_loop_points, "POINT_M",
                          where_clause = start_wc)])
            
            # Determine the current bend end m value
            # Ex. sql: "loop" = 1 AND "bend" = 1 AND "position" = 'end'
            end_wc = """{0} = {1} AND {2} = {3} AND {4} = '{5}'""".format(
                arcpy.AddFieldDelimiters(loop_points, "loop"), str(loop),
                arcpy.AddFieldDelimiters(loop_points, "bend"), str(bend),
                arcpy.AddFieldDelimiters(loop_points, "position"), "end")
            
            m_end = max([row[0] for row in arcpy.da.SearchCursor(
                        bankline_loop_points, "POINT_M",
                        where_clause = end_wc)])
            
            arcpy.AddMessage("    Bank: " + str(list(bank)[0]) + 
                             " Bend m_start: " + str(m_start) + 
                             " m_end: " + str(m_end))
            
            # Update loop and bend values for the current bend
            fc = bankline_loop_points
            fields = ["POINT_M", "loop", "bend"]
            # Ex. sql: "bank" = 'left descending' AND "POINT_M" >= 456.7 AND 
            # "POINT_M" <= 582.6
            bend_wc = """{0} = '{1}' AND {2} >= {3} AND {2} <= {4}""".format(
                arcpy.AddFieldDelimiters(bankline_loop_points, "bank"),
                list(bank)[0],
                arcpy.AddFieldDelimiters(loop_points, "POINT_M"), 
                str(m_start), str(m_end))
            arcpy.AddMessage("    " + str(bend_wc))
            
            with arcpy.da.UpdateCursor(fc, fields, where_clause = bend_wc) as cursor:
                for row in cursor: 
                    row[1] = int(loop)
                    row[2] = int(bend)
                    cursor.updateRow(row)
    
    arcpy.AddMessage("Assigned loop and bend values to bankline_loop_points")


def BanklinePoints(output_workspace, loop_points, banklines, valleyline, dem, 
                   station_distance):
    # Check out the extension licenses 
    arcpy.CheckOutExtension("3D")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("loop_points: {}".format(arcpy.Describe(loop_points).baseName))
    arcpy.AddMessage("banklines: {}".format(arcpy.Describe(banklines).baseName))
    arcpy.AddMessage("valleyline: {}".format(arcpy.Describe(valleyline).baseName))
    arcpy.AddMessage("DEM: {}".format(arcpy.Describe(dem).baseName))
    arcpy.AddMessage("Station distance: {}".format(str(station_distance)))
    
    # Snap loop_points to banklines
    snap_string = "{} 'EDGE' '50 feet'".format(arcpy.Describe(banklines).baseName)
    arcpy.Snap_edit(in_features = loop_points, 
                    snap_environment = snap_string)
    arcpy.AddMessage("loop_points snapped to banklines")
    
    # Convert banklines to points
    banklines_points = line_route_points(output_workspace = output_workspace,
                                         line = banklines, 
                                         station_distance = station_distance, 
                                         route_id_field = "bank_id",
                                         fields = ["bank","ReachName"])
    
    # Add elevation to banklines_points
    add_elevation(banklines_points, dem)
    
    # Buffer loop_points to use for spatal join
    loop_points_buffer = os.path.join(output_workspace, "loop_points_buffer")
    arcpy.Buffer_analysis(in_features = loop_points, 
                          out_feature_class = loop_points_buffer, 
                          buffer_distance_or_field = "1 Meters")
    
    # Identify loop_points close to bankline_points and transfer attributes
    bankline_loop_points = os.path.join(output_workspace, "bankline_loop_points")
    arcpy.SpatialJoin_analysis(target_features = banklines_points, 
                               join_features = loop_points_buffer, 
                               out_feature_class = bankline_loop_points, 
                               match_option = "INTERSECT")
    
    arcpy.DeleteField_management(in_table = bankline_loop_points, 
                                 drop_field = ["Join_Count", "TARGET_FID", 
                                               "ReachName_1"])
    arcpy.AddMessage("loop_points joined to banklines_points")
    
    # Assign loop and bend values to bankline_points
    assignLoopAndBend(bankline_loop_points, loop_points)
    
    # Convert valleyline to points
    valleyline_points = line_route_points(output_workspace = output_workspace,
                                          line = valleyline,
                                          station_distance = station_distance,
                                          route_id_field = "ReachName",
                                          fields = [])

    # Assign valleyline_points values to bankline_points
    bankline_points = os.path.join(output_workspace, "bankline_points")
    arcpy.SpatialJoin_analysis(target_features = bankline_loop_points,
                               join_features = valleyline_points,
                               out_feature_class = bankline_points,
                               match_option = "CLOSEST")

    arcpy.DeleteField_management(in_table = bankline_points,
                                 drop_field = ["Join_Count", "TARGET_FID", 
                                               "BUFF_DIST", "ORIG_FID",
                                               "ReachName_1" , "ReachName_12",
                                               "from_measure", "to_measure",
                                               "InLine_FID", "SmoLnFlag"])
    # Set the name of bankline_points coordinates
    arcpy.AlterField_management(bankline_points,
                                "POINT_X", 'bank_POINT_X', 'bank_POINT_X')
    arcpy.AlterField_management(bankline_points,
                                "POINT_Y", 'bank_POINT_Y', 'bank_POINT_Y')
    arcpy.AlterField_management(bankline_points,
                                "POINT_M", 'bank_POINT_M', 'bank_POINT_M')
    
    # Set the name of valleyline_points coordinates
    arcpy.AlterField_management(bankline_points,
                                "POINT_X_1", 'valley_POINT_X', 'valley_POINT_X')
    arcpy.AlterField_management(bankline_points,
                                "POINT_Y_1", 'valley_POINT_Y', 'valley_POINT_Y')
    arcpy.AlterField_management(bankline_points,
                                "POINT_M_1", 'valley_POINT_M', 'valley_POINT_M')

    # Return
    arcpy.SetParameter(6, bankline_points)
    
    # Cleanup
    arcpy.Delete_management(banklines_points)
    arcpy.Delete_management(bankline_loop_points)
    arcpy.Delete_management(loop_points_buffer)
    arcpy.Delete_management(valleyline_points)

    
def main():
    # Call the BanklinePoints function with command line parameters
    BanklinePoints(output_workspace, loop_points, banklines, valleyline, dem, 
                   station_distance)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    loop_points      = arcpy.GetParameterAsText(1)
    banklines        = arcpy.GetParameterAsText(2)
    valleyline       = arcpy.GetParameterAsText(3)
    dem              = arcpy.GetParameterAsText(4)
    station_distance = arcpy.GetParameterAsText(5)
    
    main()

