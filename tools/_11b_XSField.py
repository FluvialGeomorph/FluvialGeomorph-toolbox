"""____________________________________________________________________________
Script Name:          _11b_XSField.py
Description:          Creates cross sections from a field_xs_points feature 
                      class. 
Date:                 01/13/2024

Usage:
Creates cross sections from a field_xs_points feature class.  

Parameters:
feature_dataset       -- Path to the feature dataset. 
field_xs_points       -- Path to the field_xs_points feature class.

Outputs:
field_xs -- a new cross section feature class. 
____________________________________________________________________________"""

import os
import arcpy

def XSField(feature_dataset, field_xs_points):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    arcpy.env.outputZFlag = "Enabled"
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    
    # Create field_xs from field_xs_points
    field_xs = os.path.join(feature_dataset, "field_xs")
    arcpy.AddMessage("Started arcpy PointsToLine...")
    arcpy.management.PointsToLine(Input_Features = field_xs_points, 
                                  Output_Feature_Class = field_xs, 
                                  Line_Field = "XSName", 
                                  Sort_Field = "Station", 
                                  Attribute_Source = "START", 
                                  Transfer_Fields = ["ReachName"])
    arcpy.AddMessage("Converted field_xs_points to a field_xs line.")
    
    # Create `Seq` field
    arcpy.management.AddField(in_table = field_xs, 
                              field_name = "Seq", field_type = "SHORT")
    arcpy.management.CalculateField(in_table = field_xs, 
                                    field = "Seq", 
                                    expression = "!OBJECTID!", 
                                    expression_type = "PYTHON3")
    arcpy.AddMessage("Added Sequence field.")
    
    # Fix field names (AlterField is broke)
    arcpy.management.AddField(in_table = field_xs, 
                              field_name = "ReachName", 
                              field_type = "TEXT")
    arcpy.management.CalculateField(in_table = field_xs, 
                                    field = "ReachName", 
                                    expression = "!START_ReachName!")
    arcpy.management.DeleteField(in_table = field_xs, 
                                 drop_field = "START_ReachName")
    arcpy.AddMessage("Fixed field names")
    
    # Return
    arcpy.SetParameter(2, field_xs)


def main():
    XSField(feature_dataset, field_xs_points)
    
if __name__ == "__main__":
    feature_dataset  = arcpy.GetParameterAsText(0)
    field_xs_points  = arcpy.GetParameterAsText(1)

    main()
