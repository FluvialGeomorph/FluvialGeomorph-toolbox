"""____________________________________________________________________________
Script Name:          _Point_Landcover.py
Description:          Calculates NLCD landcover areas for the input points. 
Date:                 4/5/2018

Usage:
Calculates the area for each NLCD landcover class for each input point. Writes 
the values to a set of new fields in the input point feature class. 

Parameters:
output_workspace      -- Path to the output workspace
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

def PointLandcover(output_workspace, points, point_ID_field, nlcd, 
                   flow_accum, fdr, snap_distance):

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Cast rasters
    FAC  = arcpy.Raster(flow_accum)
    FDR = arcpy.Raster(fdr)
    NLCD = arcpy.Raster(nlcd)
    
    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    arcpy.env.extent = flow_accum
    arcpy.env.snapRaster = flow_accum
    arcpy.env.mask = flow_accum
    arcpy.env.cellSize = 30
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Points: "
                     "{}".format(arcpy.Describe(points).baseName))
    arcpy.AddMessage("Point_ID: {}".format(point_ID_field))
    arcpy.AddMessage("NLCD: {}".format(arcpy.Describe(NLCD).baseName))
    arcpy.AddMessage("FAC: {}".format(arcpy.Describe(FAC).baseName))
    arcpy.AddMessage("Snap distance: {}".format(snap_distance))
    
    # Iterate through `points` fc and calculate watershed landcover area
    with arcpy.da.UpdateCursor(in_table = points,
                               field_names = [point_ID_field],
                               sql_clause = (None, 'ORDER BY ' + point_ID_field)) as cursor:
        for row in cursor:
            # Create a feature layer from the points feature class
            # for the current point
            OID = point_ID_field + " = " + str(row[0])
            arcpy.MakeFeatureLayer_management(
                      in_features = points,
                      out_layer = "point",
                      where_clause = OID)
            arcpy.AddMessage("Created point: {}".format(str(row[0])))

            # Snap pour point to flow accumulation raster
            snapPour = arcpy.sa.SnapPourPoint(in_pour_point_data = "point",
                                in_accumulation_raster = flow_accum,
                                snap_distance = snap_distance,
                                pour_point_field = point_ID_field)
            arcpy.AddMessage("    Snap complete")

            # Create watershed raster
            watershed = arcpy.sa.Watershed(
                        in_flow_direction_raster = fdr,
                        in_pour_point_data = snapPour,
                        pour_point_field = "Value")

            # Convert watershed to polygon
            arcpy.RasterToPolygon_conversion(in_raster = watershed,
                            out_polygon_features = "watershed_" + str(row[0]))
            arcpy.AddMessage("    Watershed complete")

            # Tabulate area
            arcpy.sa.TabulateArea(in_zone_data = watershed,
                                  zone_field = "Value",
                                  in_class_data = NLCD,
                                  class_field = "Value",
                                  out_table = "nlcd_table_" + str(row[0]),
                                  processing_cell_size = 30)
            arcpy.AddMessage("    Tabulate area complete")
            
    # Merge tabulate area tables
    nlcd_tables = arcpy.ListTables(wild_card = "nlcd_table_*")
    arcpy.AddMessage("NLCD Tables: " + str(nlcd_tables))
    arcpy.Merge_management(inputs = nlcd_tables, 
                           output = "nlcd_table")
    # Delete nlcd tables
    for table in nlcd_tables:
        arcpy.Delete_management(table)
    arcpy.AddMessage("Merged NLCD area tables")
    
    # Merge watershed polygons
    watershed_fcs = arcpy.ListFeatureClasses("watershed_*")
    arcpy.AddMessage("Watershed polygons: " + str(watershed_fcs))
    arcpy.Merge_management(inputs = watershed_fcs,
                           output = "watersheds")
    # Delete watershed FCs
    for fc in watershed_fcs:
        arcpy.Delete_management(fc)
    arcpy.AddMessage("Merged watershed polygons")


def main():
    # Call the Point Landcover with command line parameters
    PointLandcover(output_workspace, points, point_ID_field, nlcd, 
                   flow_accum, fdr, snap_distance)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    points           = arcpy.GetParameterAsText(1)
    point_ID_field   = arcpy.GetParameterAsText(2)
    nlcd             = arcpy.GetParameterAsText(3)
    flow_accum       = arcpy.GetParameterAsText(4)
    fdr              = arcpy.GetParameterAsText(5)
    snap_distance    = arcpy.GetParameterAsText(6)
    
    main()
