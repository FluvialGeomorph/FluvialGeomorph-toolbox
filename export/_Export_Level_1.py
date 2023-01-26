"""____________________________________________________________________________
Script Name:          _Export_Level_1.py
Description:          Exports the attrbute tables of Level 1 feature classes. 
Date:                 09/10/2020

Usage:
Exports the attrbute tables of requested Level 1 feature classes to a new 
folder in the parent directory of the file geodatabase. This folder is named 
using the name of the geodatabase. A .csv export of the 
attribute table is created for each requested level one feature class. 

Parameters:
feature_dataset       -- Path to the feature dataset.
flowline_points       -- Path to the flowline_points feature class.
xs                    -- Path to the cross section feature class.
xs_points             -- Path to the xs_points feature class.
features              -- Path to the features feature class.

Outputs:
Exports .csv files of the attribute tables of the requested feature classes. 
____________________________________________________________________________"""

import os
import arcpy
import shutil

def Export_Level_1(feature_dataset, flowline_points, xs, xs_points, features):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    
    # Create the output folder
    gdb_path = os.path.dirname(feature_dataset)
    parent_folder = os.path.dirname(gdb_path)
    gdb_basename = os.path.splitext(os.path.basename(gdb_path))[0]
    exports_folder = os.path.join(parent_folder, "exports")
    archive_folder = os.path.join(exports_folder, gdb_basename)
    
    arcpy.AddMessage("parent_folder: {}".format(parent_folder))
    arcpy.AddMessage("gdb_basename: {}".format(gdb_basename))
    arcpy.AddMessage("exports_folder: {}".format(exports_folder))
    arcpy.AddMessage("archive_folder: {}".format(archive_folder))
    
    if not os.path.exists(exports_folder):
        os.makedirs(exports_folder)
        arcpy.AddMessage("Created folder: {}".format(exports_folder))
        
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)
        arcpy.AddMessage("Created folder: {}".format(archive_folder))
        
    if flowline_points:
        arcpy.TableToTable_conversion(in_rows = flowline_points,
                                      out_path = archive_folder,
                                      out_name = "flowline_points.csv")
                                      
    if xs:
        xs_basename = os.path.basename(xs)
        xs_csv = "{}.csv".format(xs_basename)
        arcpy.TableToTable_conversion(in_rows = xs,
                                      out_path = archive_folder,
                                      out_name = xs_csv)
                                      
    if xs_points:
        xs_points_basename = os.path.basename(xs_points)
        xs_points_csv = "{}.csv".format(xs_points_basename)
        arcpy.TableToTable_conversion(in_rows = xs_points,
                                      out_path = archive_folder,
                                      out_name = xs_points_csv)
    
    if features:
        arcpy.TableToTable_conversion(in_rows = features,
                                      out_path = archive_folder,
                                      out_name = "features.csv")


def main():
    Export_Level_1(feature_dataset, flowline_points, xs, xs_points, features)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset  = arcpy.GetParameterAsText(0)
    flowline_points  = arcpy.GetParameterAsText(1)
    xs               = arcpy.GetParameterAsText(2)
    xs_points        = arcpy.GetParameterAsText(3)
    features         = arcpy.GetParameterAsText(4)
    
    main()
