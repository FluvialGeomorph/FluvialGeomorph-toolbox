"""____________________________________________________________________________
Script Name:          _13_XSAssignRiverPosition.py
Description:          Adds a "distance to the mouth of the river" field to 
                      each cross section. 
Date:                 06/15/2019

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
flowline_points       -- Path to the flowline route feature class

Outputs:
Writes the river position to a new field `km_to_mouth` field in the cross 
section feature class.
____________________________________________________________________________"""
 
import arcpy

def DeleteExistingFields(in_table, field):
    field_names = [f.name for f in arcpy.ListFields(in_table)]
    if field in field_names:
        arcpy.DeleteField_management(in_table = cross_section, 
                                     drop_field = [field])

def XSAssignRiverPosition(output_workspace, cross_section, flowline_points):
    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Cross Section: "
                     "{}".format(arcpy.Describe(cross_section).baseName))
    arcpy.AddMessage("flowline: "
                     "{}".format(arcpy.Describe(flowline_points).baseName))
    
    # Check if the fields that will be joined to the cross section feature class 
    # exist from a previous run. If so, delete the fields before the joins. 
    DeleteExistingFields(cross_section, "km_to_mouth")
    DeleteExistingFields(cross_section, "POINT_X")
    DeleteExistingFields(cross_section, "POINT_Y")
    DeleteExistingFields(cross_section, "POINT_M")
    DeleteExistingFields(cross_section, "Z")
    
    # Spatial Join the cross sections with the closest flowline point
    arcpy.SpatialJoin_analysis(target_features = cross_section, 
                               join_features = flowline_points, 
                               out_feature_class = "cross_section_flowline_point",  
                               match_option = "CLOSEST")

    # Join fields from the `cross_section_flowline_point` table back to the 
    # `cross_section` feature class
    arcpy.JoinField_management(in_data = cross_section, 
                               in_field = "Seq", 
                               join_table = "cross_section_flowline_point", 
                               join_field = "Seq", 
                               fields = ["POINT_X", "POINT_Y", "POINT_M", "Z"])
    
    # Calculate the "km_to_mouth" field
    arcpy.AddField_management(in_table = cross_section, 
                              field_name = "km_to_mouth", 
                              field_type = "DOUBLE")
    arcpy.CalculateField_management(in_table = cross_section, 
                                    field = "km_to_mouth",
                                    expression = "!POINT_M!", 
                                    expression_type = "PYTHON_9.3")

    # Cleanup
    arcpy.Delete_management(in_data = "xs_flowline_pt")
    arcpy.Delete_management(in_data = "cross_section_flowline_point")
    return

def main():
    # Call the XSAssignRiverPosition function with command line parameters
    XSAssignRiverPosition(output_workspace, cross_section, flowline_points)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    cross_section    = arcpy.GetParameterAsText(1)
    flowline_points  = arcpy.GetParameterAsText(2)
    
    main()

