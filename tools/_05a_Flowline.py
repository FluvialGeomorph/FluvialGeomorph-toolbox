"""____________________________________________________________________________
Script Name:          _05a_Flowline.py
Description:          Creates a flowline from an edited stream network. 
Date:                 05/27/2020

Usage:
This tool requires a stream_network feature class created using the tool 
_04_StreamNetwork. 

Before running this tool, the stream_network feature class must be manually 
edited to remove all tributary streams that do not constitute the network that 
will be analyzed further in later steps of the study. 

During editing, the ReachName field must be populated to distinguish different 
stream reaches for further analysis. This tool will use the ReachName field to 
dissolve stream line segments into reaches. The resulting flowline feature 
class will have a record for each unique value in the ReachName field. 

Parameters:
feature_dataset (str) -- Path to the feature dataset.
stream_network (str)  -- Path to the edited stream network feature class.
smooth_tolerance (int)-- The PAEK smoothing tolerance that controls the 
                         calculating of new vertices. Acceptable smoothing 
                         occurs with values between 2 - 5.

Outputs:
flowline              -- a cleaned flowline feature class
____________________________________________________________________________"""

import os
import arcpy

def CleanFlowline(feature_dataset, stream_network, smooth_tolerance):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Stream Network: "
                     "{}".format(arcpy.Describe(stream_network).baseName))
    
    # Dissolve by `ReachName` field
    stream_network_dissolve = os.path.join(feature_dataset, 
                                           "stream_network_dissolve")
    arcpy.management.Dissolve(in_features = stream_network, 
                              out_feature_class = stream_network_dissolve,  
                              dissolve_field = ["ReachName"], 
                              unsplit_lines = "DISSOLVE_LINES")
    
    arcpy.AddMessage("Stream Network Dissolved")
    
    # Smooth the stream network
    flowline = os.path.join(feature_dataset, "flowline")
    arcpy.cartography.SmoothLine(in_features = stream_network_dissolve, 
                                 out_feature_class = flowline, 
                                 algorithm = "PAEK", 
                                 tolerance = smooth_tolerance)
    
    arcpy.AddMessage("Stream Network Smoothed")
    
    # Return
    arcpy.SetParameter(3, flowline)
    
    # Cleanup
    arcpy.management.Delete(in_data = stream_network_dissolve)

    
def main():
    CleanFlowline(feature_dataset, stream_network, smooth_tolerance)
    
if __name__ == "__main__":
    # Get input parameters
    feature_dataset  = arcpy.GetParameterAsText(0)
    stream_network   = arcpy.GetParameterAsText(1)
    smooth_tolerance = arcpy.GetParameterAsText(2)
    
    main()
