"""____________________________________________________________________________
Script Name:          _02_HydroDEM.py
Description:          Burn cutlines into DEM to create a new hydro modified DEM. 
Date:                 05/27/2020

Usage:
This script is based on the Agricultural Conservation Planning Framework (ACPF)
http://northcentralwater.org/acpf/ RepairFlowPaths_ManualCutter.py tool. 

This tool assumes that all input datasets are in the same coordinate system. 

Parameters:
output_workspace (str)-- Path to the output workspace
cutlines (str)        -- Path to the cutlines feature class
dem (str)             -- Path to the digital elevation model (DEM)
widen_cells (int)     -- Number of cells to widen the cutline by

Outputs:
dem_hydro             -- a hydro modified dem
____________________________________________________________________________"""

import os
import arcpy

def BurnCutlines(output_workspace, cutlines, dem, widen_cells):
    # Check out the extension license 
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    arcpy.env.extent = dem
    arcpy.env.snapRaster = dem
    arcpy.env.cellSize = arcpy.Describe(dem).meanCellHeight
    arcpy.env.compression = "LZ77"
    arcpy.env.outputCoordinateSystem = dem    
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Cutlines: "
                     "{}".format(arcpy.Describe(cutlines).baseName))
    arcpy.AddMessage("DEM: {}".format(arcpy.Describe(dem).baseName))
    arcpy.AddMessage("widen_cells: {}".format(str(widen_cells)))
    
    # Determine the resolution of dem
    cellsize = float(arcpy.GetRasterProperties_management(
                                         dem, "CELLSIZEX").getOutput(0))
    
    # Create a list of cutline OIDs
    cutlines_desc = arcpy.Describe(cutlines)
    cutlines_oid = cutlines_desc.OIDFieldName
    
    oidList = [] 
    with arcpy.da.SearchCursor(cutlines, [cutlines_oid]) as cursor: 
        for row in cursor: 
            id = row[0] 
            oidList.append(id)
    arcpy.AddMessage("Cutline OIDs: {}".format(oidList))
    
    # Convert cutlines to raster
    cutline_ras = os.path.join(output_workspace, "cutline_ras")
    OID = arcpy.Describe(cutlines).OIDFieldName
    arcpy.PolylineToRaster_conversion(
                       in_features = cutlines, 
                       value_field = OID, 
                       out_rasterdataset = cutline_ras, 
                       cellsize = cellsize)
    
    # Increase width of each cutline
    if int(widen_cells) > 0:
      arcpy.AddMessage("Expanding cutlines...")
      cutline_ras = arcpy.sa.Expand(cutline_ras, int(widen_cells), oidList)
    
    # Determine the minimum elevation along each cutline
    arcpy.AddMessage("Calculating minumum elevation for each cutline...")
    cutline_min = arcpy.sa.ZonalStatistics(in_zone_data = cutline_ras, 
                                           zone_field = "VALUE", 
                                           in_value_raster = dem, 
                                           statistics_type = "MINIMUM")
                                    
    # Con operation to burn cutline_ext into DEM
    arcpy.AddMessage("Burning cutlines into DEM...")
    dem_hydro = arcpy.sa.Con(arcpy.sa.IsNull(cutline_min), 
                             dem, 
                             cutline_min)
    
    # Save dem_hydro to the output_workspace
    dem_hydro_path = os.path.join(output_workspace, "dem_hydro")
    arcpy.CopyRaster_management(in_raster = dem_hydro, 
                                out_rasterdataset = dem_hydro_path)
    arcpy.AddMessage("Saved hydro modified DEM.")
    
    # Calculate raster statistics and build pyramids
    arcpy.CalculateStatistics_management(dem_hydro_path)
    arcpy.BuildPyramids_management(dem_hydro_path)
    arcpy.AddMessage("Calculated raster statistics and pyramids.")
    
    # Return
    arcpy.SetParameter(4, dem_hydro_path)
    
    # Cleanup
    arcpy.Delete_management(in_data = cutline_ras)


def main():
    # Call the BurnCutlines function with command line parameters
    BurnCutlines(output_workspace, cutlines, dem, widen_cells)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    cutlines         = arcpy.GetParameterAsText(1)
    dem              = arcpy.GetParameterAsText(2)
    widen_cells      = arcpy.GetParameterAsText(3)
    
    main()
