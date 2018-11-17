"""____________________________________________________________________________
Script Name:          _13_XSAssignRiverPosition.py
Description:          Adds a "distance to the mouth of the river" field to 
                      each cross section. 
Date:                 11/16/2017

Usage:
Calculates the river position of the input cross section. Writes the  
value to a new field. 

This tool assumes that there is a field in the cross section feature class 
called `Seq`, field type long integer, that uniquely identifies each cross 
section. 

This tool assumes that there is a field in the flowline feature class 
called `Name` that uniquely identifies each stream reach. 

This tool assumes that the stream flowline is digitized beginning from the 
downstream end of the stream. Open an edit session, select the flowline, 
choose to edit vertices, and ensure that the red endpoint is at the 
downstream end of the flowline. 

Parameters:
output_workspace      -- Path to the output workspace
cross_section         -- Path to the cross section line feature class
flowline_route        -- Path to the flowline route feature class

Outputs:
Writes the river position to a new field `km_to_mouth` field in the cross 
section feature class.
____________________________________________________________________________"""
 
import arcpy

def XSAssignRiverPosition(output_workspace, cross_section, flowline_route):
    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Cross Section: "
                     "{}".format(arcpy.Describe(cross_section).baseName))
    arcpy.AddMessage("flowline: "
                     "{}".format(arcpy.Describe(flowline_route).baseName))
    
    # Intersect the `cross_section` fc with the `flowline_route` fc
    arcpy.Intersect_analysis(in_features = [cross_section, flowline_route], 
                             out_feature_class = "xs_flowline_pt", 
                             output_type = "POINT")

    # Locate each cross section along the `flowline_route` feature class
    arcpy.LocateFeaturesAlongRoutes_lr(
                    in_features = "xs_flowline_pt", 
                    in_routes = flowline_route,
                    route_id_field = "ReachName",
                    radius_or_tolerance = "1 Meter",
                    out_table = "cross_section_route_table",
                    out_event_properties = "ReachName POINT km_to_mouth")

    # Before joining the `km_to_mouth` field to the `cross_section` fc, 
    # check if the `km_to_mouth` field exists from a previous run. If so, 
    # delete the field. 
    field_names = [f.name for f in arcpy.ListFields(cross_section)]
    if "km_to_mouth" in field_names:
        arcpy.DeleteField_management(in_table = cross_section, 
                                     drop_field = ["km_to_mouth"])
    
    # Join fields from the `cross_section_route_table` table to the 
    # `cross_section` feature class
    arcpy.JoinField_management(in_data = cross_section, 
                               in_field = "Seq", 
                               join_table = "cross_section_route_table", 
                               join_field = "Seq", 
                               fields = ["km_to_mouth"])

    # Cleanup
    arcpy.Delete_management(in_data = "xs_flowline_pt")
    arcpy.Delete_management(in_data = "cross_section_route_table")
    return

def main():
    # Call the XSAssignRiverPosition function with command line parameters
    XSAssignRiverPosition(output_workspace, cross_section, flowline_route)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    cross_section    = arcpy.GetParameterAsText(1)
    flowline_route   = arcpy.GetParameterAsText(2)
    
    main()

