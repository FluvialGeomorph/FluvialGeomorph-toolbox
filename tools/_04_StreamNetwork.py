"""____________________________________________________________________________
Script Name:          _04_StreamNetwork.py
Description:          Creates a synthetic flow network from a contributing 
                      area raster and a stream initiation threshold.  
Date:                 11/22/2017

Usage:
This tool requires TauDEM (http://hydrology.usu.edu/taudem/taudem5/) to be 
installed before running this tool. 

Parameters:
output_workspace      -- Path to the output workspace
contrib_area          -- Path to the contributing area raster created in the
                         previous step
threshold (long)      -- Flow accumulation threshold to initiate a stream 
                         expressed in the units of the source DEM used to 
                         accumulate the flow.
processes (long)      -- The number of stripes that the domain will be divided
                         into and the number of MPI parallel processes that will
                         be spawned to evaluate each of the stripes.

Outputs:
stream_network        -- a new polyline feature class of the synthetic stream
                         network
____________________________________________________________________________"""
 
import os
import subprocess
import arcpy

def StreamNetwork(output_workspace, contrib_area, threshold, processes):
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Contributing Area: " 
                     "{}".format(arcpy.Describe(contrib_area).baseName))
    arcpy.AddMessage("Threshold: {}".format(str(threshold)))
    arcpy.AddMessage("Processes: {}".format(str(processes)))
    
    # Convert the GDB contrib_area raster to .tif _____________________________
    # TauDEM needs an uncompressed raster. Create in GDB because CopyRaster 
    # cannot control compression when exporting to .tif
    arcpy.env.compression = "NONE"
    contrib_area_nocompression = os.path.join(output_workspace,
                            os.path.basename(contrib_area) + "_nocompression")
    arcpy.CopyRaster_management(in_raster = contrib_area, 
                                out_rasterdataset = contrib_area_nocompression)
    arcpy.AddMessage("Uncompressed contrib_area created")
    contrib_area_tif = os.path.join(os.path.dirname(output_workspace), 
                                    "contrib_area.tif")
    arcpy.CopyRaster_management(in_raster = contrib_area_nocompression, 
                                out_rasterdataset = contrib_area_tif)
    arcpy.AddMessage("Uncompressed contrib_area_tif created")

    # TauDEM Stream definition by threshold - Threshold _______________________
    # output thresholded stream raster
    stream_grid = os.path.join(os.path.dirname(output_workspace), 
                               "stream_grid.tif")
    # Construct command
    cmd = 'mpiexec -n ' + str(processes) + ' Threshold -ssa ' + '"' + contrib_area_tif + '"' + ' -src ' + '"' + stream_grid + '"' + ' -thresh ' + str(threshold)
    arcpy.AddMessage("\nTauDEM command: " + cmd)
    # Submit command to operating system
    os.system(cmd)
    # Capture contents of shell and print it to the arcgis dialog box
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    arcpy.AddMessage('\nProcess started:\n')
    for line in process.stdout.readlines():
        arcpy.AddMessage(line)

    # Thin stream network - arcpy.sa.Thin _____________________________________
    stream_thin = arcpy.sa.Thin(in_raster = stream_grid, 
                                corners = "SHARP")
    stream_thin.save(os.path.join(os.path.dirname(output_workspace), 
                                  "stream_thin.tif"))
    
    # Convert raster stream to polyline _______________________________________
    # output vector stream network
    stream_network = os.path.join(output_workspace, "stream_network")
    # Convert the `stream_thin` raster to a polyline
    arcpy.RasterToPolyline_conversion(in_raster = stream_thin, 
                                      out_polyline_features = stream_network)
    arcpy.AddMessage("Stream network created")
    
    # Add the `ReachName` field
    # Check if the field already exists and if not add it
    field_names = [f.name for f in arcpy.ListFields(stream_network)]
    if "ReachName" not in field_names:
        arcpy.AddField_management(in_table = stream_network, 
                                  field_name = "ReachName", 
                                  field_type = "TEXT")
    
    # Return
    arcpy.SetParameter(4, "stream_network")
    
    # Cleanup
    arcpy.Delete_management(in_data = contrib_area_nocompression)
    arcpy.Delete_management(in_data = contrib_area_tif)
    arcpy.Delete_management(in_data = stream_grid)
    arcpy.Delete_management(in_data = stream_thin)
    arcpy.AddMessage("Temp datasets deleted")
    
    
def main():
    # Call the StreamNetwork function with command line parameters
    StreamNetwork(output_workspace, contrib_area, threshold, processes)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    contrib_area     = arcpy.GetParameterAsText(1)
    threshold        = arcpy.GetParameterAsText(2)
    processes        = arcpy.GetParameterAsText(3)

    main()

