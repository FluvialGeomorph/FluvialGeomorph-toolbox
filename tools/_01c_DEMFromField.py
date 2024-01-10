"""____________________________________________________________________________
Script Name:          _01c_DEMFromField.py
Description:          Creates a DEM from field survey points.  
Date:                 1/9/2024

Usage:

Parameters:
feature_dataset       -- Path to the feature dataset
thalweg_points        -- Path to the thalweg_points feature class. 
field_xs_points       -- Path to the field_xs_points feature class. 

Outputs:
stream_network        -- a new `field_xs_points` feature class
____________________________________________________________________________"""
 
import os
import arcpy

def DEMFromField(feature_dataset, field_xs_csv, field_xs_srs, reach_name):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    
    # Combine thalweg and cross sections into elevation points
    
    # Interpolate elevation points to DEM
    
    # Return
    arcpy.SetParameter(4, field_xs_points)
    
    # Cleanup
    arcpy.Delete_management(in_data = field_xs_table)
    arcpy.AddMessage("Temp datasets deleted")
    
    
def main():
    # Call the function with command line parameters
    ImportThalweg(feature_dataset, field_xs_csv, field_xs_srs, reach_name)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset = arcpy.GetParameterAsText(0)
    field_xs_csv    = arcpy.GetParameterAsText(1)
    field_xs_srs    = arcpy.GetParameterAsText(2)
    reach_name      = arcpy.GetParameterAsText(3)

    main()
