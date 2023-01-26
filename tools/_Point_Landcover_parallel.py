"""____________________________________________________________________________
Script Name:          _Point_Landcover_parallel.py
Description:          Calculates NLCD landcover areas for the input points. 
Date:                 4/10/2018

Usage:
Calculates the area for each NLCD landcover class for each input point. Writes 
the values to a set of new fields in the input point feature class. 

Parameters:
feature_dataset       -- Path to the feature dataset
points                -- Path to the points feature class
point_ID_field        -- Field that contains the point IDs
nlcd                  -- Path to the NLCD raster
flow_accum            -- Path to the flow accumulation model
fdr                   -- Path to the flow direction model
snap_distance         -- The distance the point will be snapped to find the 
                         cell of highest flow accumulation

Outputs:
Writes the land cover values to a set of new fields in the input point 
feature class.  
____________________________________________________________________________"""
 
import arcpy

def main():
    # Call the Point Landcover with command line parameters
    PointLandcover(feature_dataset, points, point_ID_field, nlcd, 
                   flow_accum, fdr, snap_distance)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset  = arcpy.GetParameterAsText(0)
    points           = arcpy.GetParameterAsText(1)
    point_ID_field   = arcpy.GetParameterAsText(2)
    nlcd             = arcpy.GetParameterAsText(3)
    flow_accum       = arcpy.GetParameterAsText(4)
    fdr              = arcpy.GetParameterAsText(5)
    snap_distance    = arcpy.GetParameterAsText(6)
    
    main()
