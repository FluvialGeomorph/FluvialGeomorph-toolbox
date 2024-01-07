"""____________________________________________________________________________
Script Name:          _04d_StreamNetwork.py
Description:          Creates a flow network from a field survey.  
Date:                 11/17/2023

Usage:


Parameters:
feature_dataset       -- Path to the feature dataset
thalweg               -- Path to the table of field survey points along the 
                         stream thalweg. This table must have the following 
                         fields:
                             - Point - Name of the point.
                             - Northing - The latitude coordinate. 
                             - Easting - The longitude coordinate. 
                             - Elevation - The elevation in NAVD88 feet. 
                             - Code - Field code representing the thalweg.
thalweg_srs           -- The spatial reference system of the thalweg survey.


Outputs:
stream_network        -- a new polyline feature class of the stream
                         network
____________________________________________________________________________"""
 
import os
import arcpy

def StreamNetworkField(feature_dataset, ):
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    
    # Convert table to points
    thalweg_points = os.path.join(feature_dataset, "thalweg_points")
    arcpy.mamagement.XYTableToPoints(in_table = thalweg,
                                     out_feature_class = thlaweg_points,
                                     x_coords = "Easting",
                                     y_coords = "Northing",
                                     z_coords = "Elevation",
                                     coordinate_system = thalweg_srs)
    
    # Convert points to polyline
    stream_network = os.path.join(feature_dataset, "stream_network")
    
    
    # Add the `ReachName` field
    # Check if the field already exists and if not add it
    field_names = [f.name for f in arcpy.ListFields(stream_network)]
    if "ReachName" not in field_names:
        arcpy.AddField_management(in_table = stream_network, 
                                  field_name = "ReachName", 
                                  field_type = "TEXT")
    
    # Return
    arcpy.SetParameter(4, stream_network)
    
    # Cleanup
    
    arcpy.AddMessage("Temp datasets deleted")
    
    
def main():
    # Call the StreamNetwork function with command line parameters
    StreamNetwork(feature_dataset, contrib_area, threshold, processes)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset = arcpy.GetParameterAsText(0)
    contrib_area     = arcpy.GetParameterAsText(1)
    threshold        = arcpy.GetParameterAsText(2)
    processes        = arcpy.GetParameterAsText(3)

    main()

