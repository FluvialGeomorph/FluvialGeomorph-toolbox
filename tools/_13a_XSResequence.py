"""____________________________________________________________________________
Script Name:          _13a_XSResequence.py
Description:          Resequences the `Seq` field after cross sections have been
                      added or deleted.  
Date:                 05/16/2020

Usage:
This tool resequences the `Seq` field after cross sections have been added or 
deleted. This ensures that there are no duplicate, missing, or nonsequentially
ordered `Seq` field values. 

This tool solves the following problems:
* Orders cross section `Seq` field values in ascending `POINT_M` field values, 
    therefore eliminating mis-ordered cross sections.
* Eliminates duplicate `Seq` field values.
* Eliminates gaps in `Seq` field values.

This tool assumes:
* Cross sections are ordered beginning at the downstream end of a reach. Ensure 
    the flowline feature class was digitized in the correct direction (endpoint
    at upstream end of the reach). 
* The fields `POINT_M` and `Seq` exist in the input cross section feature class.

Parameters:
output_workspace (str)-- Path to the output workspace.
xs_fc (str)           -- Path to a cross section feature class.
start_seq (int)       -- The starting value of the `Seq` field.

Outputs:
xs_fc                 -- Updates the `Seq` field of the input xs_fc
____________________________________________________________________________"""
 
import os
import sys
import arcpy

def BankfullPolygon(output_workspace, xs_fc, start_seq):
    # Check out the extension license 
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace

    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("xs_fc: "
                     "{}".format(arcpy.Describe(xs_fc).baseName))
    arcpy.AddMessage("start_seq: {}".format(str(start_seq)))
    
    # Check prerequsites
    field_names = [f.name for f in arcpy.ListFields(xs_fc)]
    if "Seq" not in field_names:
        arcpy.AddError("Seq field missing")
            
    if "POINT_M" not in field_names:
        arcpy.AddError("POINT_M field missing")
    
    # Set fields to use for update
    fields = ["Seq", "POINT_M"]
    
    # Set first cross section `Seq` field value
    xs_num = int(start_seq)
    
    # Set sql_clause
    sql_clause = (None, "ORDER BY POINT_M ASC")
    
    with arcpy.da.UpdateCursor(xs_fc, fields, sql_clause = sql_clause) as cursor:
        for row in cursor:
            arcpy.AddMessage("Seq: {0} M: {1}".format(xs_num, str(round(row[1], 4))))
            row[0] = xs_num
            cursor.updateRow(row)
            xs_num += 1
    
    # Return
    arcpy.SetParameter(3, xs_fc)


def main():
    # Call the BankfullPolygon function with command line parameters
    BankfullPolygon(output_workspace, xs_fc, start_seq)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    xs_fc            = arcpy.GetParameterAsText(1)
    start_seq        = arcpy.GetParameterAsText(2)
    
    main()

