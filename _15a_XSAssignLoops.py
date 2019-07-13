"""____________________________________________________________________________
Script Name:          _15a_XS_Assign_Loops.py
Description:          Assigns loops and bends to cross sections. 
Date:                 07/06/2019

Usage:
Assigns loops and bends to cross section features by finding the closest 
bankline_points feature. 

This tool assumes that there is a field in the bankline feature class 
called `ReachName` that uniquely identifies each stream reach. 

Parameters:
output_workspace      -- Path to the output workspace
cross_section         -- Path to the cross section feature class
bankline_points       -- Path to the bankline_points feature class                         

Outputs:
Updates the cross_section feature class with new fields for loop and bend. 
____________________________________________________________________________"""
 
import arcpy
import os

def XSAssignLoops(output_workspace, cross_section, bankline_points):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("cross_section: {}".format(arcpy.Describe(cross_section).baseName))
    arcpy.AddMessage("bankline_points: {}".format(arcpy.Describe(bankline_points).baseName))
    
    # Remove Null loop records from bankline_points
    loop_bl_pts = arcpy.MakeFeatureLayer_management(bankline_points, "loop_bl_pts",
                            where_clause = "loop IS NOT NULL")
    
    # Path to new cross_section feature class
    xs_fc_name = arcpy.Describe(cross_section).baseName
    xs_fc = os.path.join(arcpy.env.workspace, xs_fc_name + "_loops")
    
    # Spatial Join bankline_points with the closest (within 5m) loop_point
    arcpy.SpatialJoin_analysis(target_features = cross_section, 
                               join_features = "loop_bl_pts", 
                               out_feature_class = xs_fc,  
                               match_option = "CLOSEST",
                               search_radius = 5)
                               
    # Delete unneeded fields
    


def main():
    XSAssignLoops(output_workspace, cross_section, bankline_points)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    cross_section    = arcpy.GetParameterAsText(1)
    bankline_points  = arcpy.GetParameterAsText(2)
    
    main()
