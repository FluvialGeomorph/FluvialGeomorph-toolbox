"""____________________________________________________________________________
Script Name:          _03_ContributingArea.py
Description:          Calculates the contributing area from an input DEM. 
Date:                 05/5/2020

Usage:
This tool requires TauDEM (http://hydrology.usu.edu/taudem/taudem5/) to be 
installed before running this tool. 

Parameters:
output_workspace (str)-- Path to the output workspace. 
dem (str)             -- Path to the digital elevation model (DEM). 
processes (long)      -- The number of stripes that the domain will be divided
                         into and the number of MPI parallel processes that 
                         will be spawned to evaluate each of the stripes.

Outputs:
contrib_area          -- a TauDEM contributing area raster. Units are the 
                         linear units of the input DEM.
flow_direction        -- A TauDEM flow direction raster. 
____________________________________________________________________________"""
 
import os
import subprocess
import arcpy

def ContributingArea(output_workspace, dem, processes):
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("DEM: {}".format(arcpy.Describe(dem).baseName))
    arcpy.AddMessage("Processes: {}".format(str(processes)))
        
    # Export DEM to dem.tif file for use by TauDEM ____________________________
    # TauDEM needs an uncompressed dem. Create in GDB because CopyRaster 
    # cannot control compression when exporting to .tif
    arcpy.env.compression = "NONE"
    dem_nocompression = os.path.join(output_workspace,
                                     os.path.basename(dem) + "_nocompression")
    arcpy.CopyRaster_management(in_raster = dem, 
                                out_rasterdataset = dem_nocompression)
    arcpy.AddMessage("Uncompressed DEM created")
    
    # Create .tif version of dem (TauDEM only accepts .tif input). Stored at 
    # the folder above the output_workspace
    demfile = os.path.join(os.path.dirname(output_workspace), 
                           "dem.tif")
    arcpy.CopyRaster_management(in_raster = dem_nocompression, 
                                out_rasterdataset = demfile)
    arcpy.AddMessage("Temporary `dem.tif` created")
        
    # TauDEM Remove pits - PitRemove __________________________________________
    # output elevation with pits filled
    felfile = os.path.join(os.path.dirname(output_workspace), "dem_fel.tif")
    # Construct the taudem command line
    cmd = 'mpiexec -n ' + str(processes) + ' pitremove -z ' + '"' + demfile + '"' + ' -fel ' + '"' + felfile + '"'
    arcpy.AddMessage("\nTauDEM command: " + cmd)
    # Submit command to operating system
    os.system(cmd)
    # Capture contents of shell and print it to the arcgis dialog box
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    arcpy.AddMessage('\nProcess started:\n')
    for line in process.stdout.readlines():
        arcpy.AddMessage(line)
    arcpy.AddMessage("Pits Removed Calculated")
        
    # TauDEM D Infinity flow direction - DinfFlowDir __________________________
    # output flow direction (ang) and slope (slp) rasters
    angfile = os.path.join(os.path.dirname(output_workspace), "dem_ang.tif")
    slpfile = os.path.join(os.path.dirname(output_workspace), "dem_slp.tif")
    # Construct command 
    cmd = 'mpiexec -n ' + str(processes) + ' DinfFlowDir -fel ' + '"' + felfile + '"' + ' -ang ' + '"' + angfile + '"' + ' -slp ' + '"' + slpfile + '"'
    arcpy.AddMessage("\nTauDEM command: " + cmd)
    # Submit command to operating system
    os.system(cmd)
    # Capture contents of shell and print it to the arcgis dialog box
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    arcpy.AddMessage('\nProcess started:\n')
    for line in process.stdout.readlines():
        arcpy.AddMessage(line)
    arcpy.AddMessage("Flow Direction Calculated")

    # TauDEM D-infinity Contributing Area - AreaDinf __________________________
    # output specific area (sca) 
    scafile = os.path.join(os.path.dirname(output_workspace), "sca.tif")
    # Construct command
    # No outlet file, weight file, or edge contanimation checking
    cmd = 'mpiexec -n ' + str(processes) + ' AreaDinf -ang ' + '"' + angfile + '"' + ' -sca ' + '"' + scafile + '"' + ' -nc '
    arcpy.AddMessage("\nTauDEM command: " + cmd)
    # Submit command to operating system
    os.system(cmd)
    # Capture contents of shell and print it to the arcgis dialog box
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    arcpy.AddMessage('\nProcess started:\n')
    for line in process.stdout.readlines():
        arcpy.AddMessage(line)

    # Copy contributing area raster to output_workspace
    contributing_area = os.path.join(output_workspace, "contributing_area")
    arcpy.env.compression = "LZ77"
    arcpy.CopyRaster_management(in_raster = scafile, 
                                out_rasterdataset = contributing_area)
    arcpy.AddMessage("Contributing Area Calculated")
    
    # Copy flow direction raster to output_workspace
    flow_direction = os.path.join(output_workspace, "flow_direction")
    arcpy.env.compression = "LZ77"
    arcpy.CopyRaster_management(in_raster = felfile, 
                                out_rasterdataset = flow_direction)
    arcpy.AddMessage("Flow Direction Calculated")
    
    # Return
    arcpy.SetParameter(3, "contributing_area")
    
    # Cleanup
    arcpy.Delete_management(in_data = dem_nocompression)
    arcpy.Delete_management(in_data = demfile)
    arcpy.Delete_management(in_data = felfile)
    arcpy.Delete_management(in_data = angfile)
    arcpy.Delete_management(in_data = slpfile)
    arcpy.Delete_management(in_data = scafile)
    arcpy.AddMessage("Temp datasets deleted")

def main():
    # Call the ContributingArea function with command line parameters
    ContributingArea(output_workspace, dem, processes)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    dem              = arcpy.GetParameterAsText(1)
    processes        = arcpy.GetParameterAsText(2)

    main()

