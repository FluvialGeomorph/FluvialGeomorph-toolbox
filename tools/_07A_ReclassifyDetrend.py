"""____________________________________________________________________________
Script Name:          ReclassifyDetrend.py
Description:          Reclassifies detrended rasters at defined intervals between values 100 and 120. 
Date:                 11/20/2017

Usage:


Parameters:
output_workspace      -- Path to the output workspace
detrend	              -- Path to the detrended raster

Outputs:
detrend_everyft		 -- a new raster reclassified at one foot intervals

____________________________________________________________________________"""
import os
import arcpy
from arcpy.sa import *


#Define the ReclassifyDetrend function
 
def ReclassifyDetrend(output_workspace, detrend):
  #Check out the extension lisence
  arcpy.CheckOutExtension("Spatial")

  # Set environment variables 
  arcpy.env.overwriteOutput = True
  arcpy.env.workspace = output_workspace
  arcpy.env.extent = detrend
  arcpy.env.snapRaster = detrend
  arcpy.env.cellSize = arcpy.Describe(detrend).meanCellHeight
  arcpy.env.compression = "LZ77"
  arcpy.env.outputCoordinateSystem = detrend 

  # List parameter values
  arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
  arcpy.AddMessage("detrend: {}".format(arcpy.Describe(detrend).baseName))

  detrend_everyft = Reclassify(in_raster = detrend, 
                               reclass_field = "VALUE",
                               remap = RemapRange([[0,100,100],[100,101,101],[101,102,102],[102,103,103],[103,104,104],[104,105,105],[105,106,106],[106,107,107],[107,108,108],[108,109,109],[109,110,110],[110,111,111],[111,112,112],[112,500,"NODATA"]]))
  detrend_everyft.save(os.path.join(output_workspace, "detrend_everyft"))
  return(detrend_everyft)
  
def main():
  #Call the ReclassifyDetrend function with command line parameters
  ReclassifyDetrend(output_workspace, detrend)

if __name__ == "__main__":
  # Get input parameters
  output_workspace = arcpy.GetParameterAsText(0)
  detrend          = arcpy.GetParameterAsText(1)
  
  main()