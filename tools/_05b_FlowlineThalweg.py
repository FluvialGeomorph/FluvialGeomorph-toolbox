"""____________________________________________________________________________
Script Name:          _05b_FlowlineThalweg.py
Description:          Creates a flowline from a thalweg_points feature class. 
Date:                 01/13/2024

Usage:
This tool requires a thalweg_points feature class created using the tool 
_01a_ImportThalweg. 

The ReachName field must be populated to distinguish different 
stream reaches for further analysis. This tool will use the ReachName field to 
dissolve stream line segments into reaches. The resulting flowline feature 
class will have a record for each unique value in the ReachName field. 

Parameters:
feature_dataset       -- Path to the feature dataset.
thalweg_points        -- Path to the edited stream network feature class.

Outputs:
flowline              -- a flowline feature class
____________________________________________________________________________"""

import os
import arcpy

def FlowlineThalweg(feature_dataset, thalweg_points):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    arcpy.env.outputZFlag = "Enabled"
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    
    # Create flowline from thalweg_points
    flowline = os.path.join(feature_dataset, "flowline")
    arcpy.management.PointsToLine(Input_Features = thalweg_points, 
                                  Output_Feature_Class = flowline, 
                                  Line_Field = "ReachName", 
                                  Sort_Field = "Point", 
                                  Transfer_Fields = ["ReachName"])
    
    # Return
    arcpy.SetParameter(2, flowline)


def main():
    FlowlineThalweg(feature_dataset, thalweg_points)
    
if __name__ == "__main__":
    # Get input parameters
    feature_dataset  = arcpy.GetParameterAsText(0)
    thalweg_points   = arcpy.GetParameterAsText(1)

    main()
