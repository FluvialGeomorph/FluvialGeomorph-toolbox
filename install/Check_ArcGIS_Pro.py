"""____________________________________________________________________________
Script Name:          Check_ArcGIS_Pro.py
Description:          Checks if Python scripts are compatible with ArcGIS Pro. 
Date:                 05/14/2020

Usage:
This script uses the ArcGIS Pro `Analyze Tools for Pro` tool to determine 
compatiblity with ArcGIS Pro. Therefore, this tool will only run in ArcGIS Pro. 

Parameters:
input_folder          -- Path to the folder of Python scripts to be checked. 

Outputs:
A new folder `ArcGIS_Pro_tests` is created in the `input_folder` and is filled
with a report for each .py file found. Each report lists any ArcGIS Pro 
compatibility problems found. 
____________________________________________________________________________"""

import os
from os import listdir
from os.path import isfile, join
import arcpy

def just_filename(file_with_ext):
    # Remove extension from strings like 'filename.ext'
    filename = os.path.splitext(file_with_ext)[0]
    return filename

def CheckArcGISPro(input_folder):
    # Get a list of .py files in the input folder
    py_files = [f for f in listdir(input_folder) if isfile(join(input_folder, f)) and  f.endswith(".py")]
    # Strip extensions from .py files
    py_file_names = [just_filename(file_) for file_ in py_files]
    arcpy.AddMessage(".py files: {}".format(py_file_names))
    
    # Create report folder
    report_folder = os.path.join(input_folder, "ArcGIS_Pro_reports")
    if not os.path.exists(report_folder):
        os.mkdir(report_folder)
    
    arcpy.AddMessage("Report folder: {}".format(report_folder))
    
    # Loop through .py files a analyze
    for i in range(0, len(py_files)):
        # Create paths for the specific .py file and report
        input_py_file = os.path.join(input_folder, py_files[i])
        report_file  = os.path.join(report_folder, py_file_names[i])
        
        # Call the analysis tool
        arcpy.AnalyzeToolsForPro_management(input_py_file, 
                                            report = report_file)
        arcpy.AddMessage("    Analyzed: {}".format(py_files[i]))
    
def main():
    CheckArcGISPro(input_folder)

if __name__ == "__main__":
    # Get input parameters
    input_folder = arcpy.GetParameterAsText(0)

    main()
