"""____________________________________________________________________________
Script Name:          JoinTable.py
Description:          Creates a new feature class containing the table fields. 
Date:                 01/25/2023

Usage:
Creates a new feature class using the feature class parameter and joins the 
table's fields to the new feature class.  

This tool assumes that the table was generated from calculations made on the 
feature class. Therefore the feature class and table must have the smae number 
of records and the same unique identifier field values. The new feature class 
is saved to the location of the fc using the name of the table with the 
"_table" suffix removed. 

Parameters:
output_workspace      -- Path to the output workspace.
fc                    -- Path to the feature class.
fc_field              -- The feature class field used for the join.
table                 -- Path to the table. 
table_field           -- The table field used for the join. 

Outputs:
Creates a new feature class using the feature class and containing the fields 
from the table.  
____________________________________________________________________________"""

import os 
import arcpy


def CopyJoin(output_workspace, fc, fc_field, table, table_field):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("fc: {}".format(arcpy.Describe(fc).baseName))
    arcpy.AddMessage("table: {}".format(arcpy.Describe(table).baseName))
    
    # Create the new output feature class
    feature_dataset = os.path.dirname(fc)
    table_name  = os.path.basename(table)
    out_fc_name = table_name.replace("_table", "")
    out_fc_path = os.path.join(feature_dataset, out_fc_name)
    arcpy.management.CopyFeatures(in_features = fc, 
                                  out_feature_class = out_fc_path)
    arcpy.AddMessage("Created new fc")
                               
    # Join `table` to the new feature class
    arcpy.management.JoinField(in_data = out_fc_path,
                               in_field = fc_field,
                               join_table = table,
                               join_field = table_field)
    arcpy.AddMessage("Joined table to new fc")
    
    # Delete duplicate fields
    dup_fields = [f.name for f in arcpy.ListFields(dataset = out_fc_path, 
                                                  wild_card = "*_1")]
    arcpy.management.DeleteField(in_table = out_fc_path,
                                  drop_field = dup_fields)
    arcpy.AddMessage("Deleted duplicate fields")
    
    # Return
    arcpy.SetParameter(5, out_fc_path)


def main():
    CopyJoin(output_workspace, fc, fc_field, table, table_field)

if __name__ == "__main__":
    output_workspace = arcpy.GetParameterAsText(0)
    fc               = arcpy.GetParameterAsText(1)
    fc_field         = arcpy.GetParameterAsText(2)
    table            = arcpy.GetParameterAsText(3)
    table_field      = arcpy.GetParameterAsText(4)
    
    main()
