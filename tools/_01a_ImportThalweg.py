"""____________________________________________________________________________
Script Name:          _01a_ImportThalweg.py
Description:          Creates a thalweg point feature class from a field survey.  
Date:                 1/7/2024

Usage:


Parameters:
feature_dataset       -- Path to the feature dataset
thalweg               -- Path to the .csv of field survey points along the 
                         stream thalweg. This .csv must have the following 
                         fields:
                             - Point - Name of the point.
                             - Northing - The latitude coordinate. 
                             - Easting - The longitude coordinate. 
                             - Elevation - The elevation in NAVD88 feet. 
                             - Code - Field code representing the thalweg.
thalweg_srs           -- The spatial reference system of the thalweg survey.
reach_name            -- The reach name. 


Outputs:
stream_network        -- a new `thalweg_points` feature class
____________________________________________________________________________"""
 
import os
import arcpy

def ImportThalweg(feature_dataset, thalweg, thalweg_srs, reach_name):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    
    # Convert .csv to geodatabase table
    thalweg_table = os.path.join(os.path.dirname(feature_dataset), 
                                 "thalweg_table")
    arcpy.conversion.ExportTable(in_table = thalweg, 
                                 out_table = thalweg_table)
    
    # Convert geodatabase table to point feature class
    thalweg_points = os.path.join(feature_dataset, "thalweg_points")
    arcpy.management.XYTableToPoint(in_table = thalweg_table,
                                     out_feature_class = thalweg_points,
                                     x_field = "Easting",
                                     y_field = "Northing",
                                     z_field = "Elevation",
                                     coordinate_system = thalweg_srs)
    
    # Add the `ReachName` field
    # Check if the field already exists and if not add it
    field_names = [f.name for f in arcpy.ListFields(thalweg_points)]
    if "ReachName" not in field_names:
        arcpy.AddField_management(in_table = thalweg_points, 
                                  field_name = "ReachName", 
                                  field_type = "TEXT")
    
    expression = '"{}"'.format(str(reach_name))
    arcpy.management.CalculateField(in_table = thalweg_points, 
                                    field = "ReachName", 
                                    expression = expression, 
                                    expression_type = "PYTHON_9.3")
    
    # Return
    arcpy.SetParameter(4, thalweg_points)
    
    # Cleanup
    arcpy.management.Delete(in_data = thalweg_table)
    arcpy.AddMessage("Temp datasets deleted")
    
    
def main():
    # Call the function with command line parameters
    ImportThalweg(feature_dataset, thalweg, thalweg_srs, reach_name)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset = arcpy.GetParameterAsText(0)
    thalweg         = arcpy.GetParameterAsText(1)
    thalweg_srs     = arcpy.GetParameterAsText(2)
    reach_name      = arcpy.GetParameterAsText(3)

    main()

