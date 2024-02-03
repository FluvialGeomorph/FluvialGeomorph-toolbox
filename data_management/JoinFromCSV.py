"""____________________________________________________________________________
Script Name:          JoinFromCSV.py
Description:          Creates a new feature class containing the csv table 
                      fields. 
Date:                 01/30/2024

Usage:
Creates a new feature class using the feature class parameter and joins the 
csv table's fields to the new feature class.  

This tool assumes that the csv table was generated from calculations made on 
the feature class. Therefore the feature class and table must have the same 
number of records and the same unique identifier field values. The new 
feature class is saved to the location of the fc using the name of the table 
with the "_table" suffix removed. 

Parameters:
feature_dataset       -- Path to the feature dataset
fc                    -- Path to the feature class.
fc_field              -- The feature class field used for the join.
csv_file              -- Path to the csv file. 
csv_field             -- The csv field used for the join. 

Outputs:
Creates a new feature class using the feature class and containing the fields 
from the table.  
____________________________________________________________________________"""

import os 
from pathlib import Path
import arcpy

def JoinFromCSV(feature_dataset, fc, fc_field, csv_file, csv_field):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("fc: {}".format(arcpy.Describe(fc).baseName))
    arcpy.AddMessage("table: {}".format(arcpy.Describe(csv_file).baseName))
    
    # Convert .csv to geodatabase table
    csv_filename = Path(csv_file).stem
    table_path = os.path.join(arcpy.env.workspace, csv_filename)
    arcpy.conversion.ExportTable(in_table = csv_file, 
                                 out_table = table_path)
    arcpy.AddMessage("Imported .csv file")
    
    # Create the new output feature class
    out_fc_name = csv_filename.replace("_table", "")
    out_fc_path = os.path.join(feature_dataset, out_fc_name)
    arcpy.management.CopyFeatures(in_features = fc, 
                                  out_feature_class = out_fc_path)
    arcpy.AddMessage("Created new fc")
    
    # Join `table` to the new feature class
    arcpy.management.JoinField(in_data = out_fc_path,
                               in_field = fc_field,
                               join_table = table_path,
                               join_field = csv_field)
    arcpy.AddMessage("Joined table to new fc")
    
    # Delete duplicate fields
    dup_fields = [f.name for f in arcpy.ListFields(dataset = out_fc_path, 
                                                  wild_card = "*_1")]
    arcpy.management.DeleteField(in_table = out_fc_path,
                                 drop_field = dup_fields)
    arcpy.AddMessage("Deleted duplicate fields")
    
    
    # Cleanup
    arcpy.management.Delete(table_path)
    
    # Return
    arcpy.SetParameter(5, out_fc_path)


def main():
    JoinFromCSV(feature_dataset, fc, fc_field, csv_file, csv_field)

if __name__ == "__main__":
    feature_dataset  = arcpy.GetParameterAsText(0)
    fc               = arcpy.GetParameterAsText(1)
    fc_field         = arcpy.GetParameterAsText(2)
    csv_file         = arcpy.GetParameterAsText(3)
    csv_field        = arcpy.GetParameterAsText(4)
    
    main()
