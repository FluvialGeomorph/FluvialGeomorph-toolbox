"""____________________________________________________________________________
Script Name:          _01a_ImportFieldXS.py
Description:          Creates a cross section (XS) point feature class from a
                      field survey.  
Date:                 1/9/2024

Usage:

Parameters:
feature_dataset       -- Path to the feature dataset
field_xs_csv          -- Path to the .csv of field xs survey points along the 
                         stream. This .csv must have the following fields:
                            - Point - Name of the point.
                            - Northing - The latitude coordinate. 
                            - Easting - The longitude coordinate. 
                            - Elevation - The elevation in NAVD88 feet. 
                            - Station - The station distance of the point along 
                              the cross section.  
                            - Code - Field code representing the thalweg. 
                            - XSName - The unique identifier of the surveyed 
                              cross section. 
field_xs_srs          -- The spatial reference system of the field xs survey.
reach_name            -- The reach name. 

Outputs:
stream_network        -- a new `field_xs_points` feature class
____________________________________________________________________________"""
 
import os
import arcpy

def ImportFieldXS(feature_dataset, field_xs_csv, field_xs_srs, reach_name):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    
    # Convert .csv to geodatabase table
    field_xs_table = os.path.join(os.path.dirname(feature_dataset), 
                                 "field_xs_table")
    arcpy.conversion.ExportTable(in_table  = field_xs_csv, 
                                 out_table = field_xs_table)
    
    # Convert geodatabase table to point feature class
    field_xs_points = os.path.join(feature_dataset, "field_xs_points")
    arcpy.management.XYTableToPoint(in_table = field_xs_table,
                                     out_feature_class = field_xs_points,
                                     x_field = "Easting",
                                     y_field = "Northing",
                                     z_field = "Elevation",
                                     coordinate_system = field_xs_srs)
    
    # Add the `ReachName` field
    # Check if the field already exists and if not add it
    field_names = [f.name for f in arcpy.ListFields(field_xs_points)]
    if "ReachName" not in field_names:
        arcpy.AddField_management(in_table = field_xs_points, 
                                  field_name = "ReachName", 
                                  field_type = "TEXT")
    
    expression = '"{}"'.format(str(reach_name))
    arcpy.management.CalculateField(in_table = field_xs_points, 
                                    field = "ReachName", 
                                    expression = expression, 
                                    expression_type = "PYTHON_9.3")
    
    # Return
    arcpy.SetParameter(4, field_xs_points)
    
    # Cleanup
    arcpy.management.Delete(in_data = field_xs_table)
    arcpy.AddMessage("Temp datasets deleted")
    
    
def main():
    # Call the function with command line parameters
    ImportFieldXS(feature_dataset, field_xs_csv, field_xs_srs, reach_name)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset = arcpy.GetParameterAsText(0)
    field_xs_csv    = arcpy.GetParameterAsText(1)
    field_xs_srs    = arcpy.GetParameterAsText(2)
    reach_name      = arcpy.GetParameterAsText(3)

    main()
