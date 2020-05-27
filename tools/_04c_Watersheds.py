"""____________________________________________________________________________
Script Name:          _04c_Watersheds.py
Description:          Calculates the watershed for each input point. 
Date:                 05/27/2020

Usage:
Calculates the drainage area watershed for each input point. Optionally 
calculates the area within the delineated watershed for each land cover class 
for each input point.  

The flow direction raster must be calculated using the D8 method. 

The flow accumulation raster can be calculated using any method (D8, D-infinity, 
etc.).

If specified, the landcover raster can be any catagorical raster (integer) 
describing classes of land cover. For each watershed in the output watershed 
feature class, the area of each landcover class (in the linear units of the 
landcover raster) will be calculated in a field named for the landcover class 
integer value. 

Parameters:
output_workspace      -- Path to the output workspace.
points                -- Path to the points feature class.
point_ID_field        -- Field in the points feature class that contains the 
                         point IDs.
flow_accumulation     -- Path to the flow accumulation model.
flow_direction_d8     -- Path to the flow direction model (must use D8 method).
snap_distance         -- The distance the point will be snapped to find the 
                         cell of highest flow accumulation.
landcover             -- Path to a categorical land cover raster (optional).

Outputs:
watersheds  -- Creates a new polygon features class representing the drainage 
area with a record for each input point (labeled with point_ID_field). 
Optionally summarizes land cover from a categorical (integer) raster, such as 
the NLCD by adding fields containing the area of each land cover class for each 
watershed. 
____________________________________________________________________________"""
 
import os
import arcpy

def PointLandcover(output_workspace, points, point_ID_field, 
                   flow_accumulation, flow_direction_d8, snap_distance, 
                   landcover):

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Cast rasters
    FAC = arcpy.Raster(flow_accumulation)
    FDR = arcpy.Raster(flow_direction_d8)
    if landcover:
        LC = arcpy.Raster(landcover)
    
    # Get landcover cell size
    if landcover:
        lc_cell_size = arcpy.Describe(LC).meanCellHeight
    
    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    arcpy.env.extent = flow_accumulation
    arcpy.env.snapRaster = flow_accumulation
    arcpy.env.mask = flow_accumulation
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Points: "
                     "{}".format(arcpy.Describe(points).baseName))
    arcpy.AddMessage("Point_ID: {}".format(point_ID_field))
    arcpy.AddMessage("Flow accumulation: {}".format(arcpy.Describe(FAC).baseName))
    arcpy.AddMessage("Flow direction D8: {}".format(arcpy.Describe(FDR).baseName))
    arcpy.AddMessage("Snap distance: {}".format(snap_distance))
    if landcover:
        arcpy.AddMessage("Landcover: {}".format(arcpy.Describe(LC).baseName))
    
    # Iterate through `points` fc and calculate watershed landcover area
    sql_postfix = "ORDER BY {}".format(point_ID_field)
    with arcpy.da.UpdateCursor(in_table = points,
                               field_names = [point_ID_field],
                               sql_clause = (None, sql_postfix)) as cursor:
        for row in cursor:
            # Create a feature layer from the points feature class
            # for the current point
            OID = "\"{0}\" = '{1}'".format(point_ID_field, str(row[0]))
            arcpy.AddMessage("Creating point: {}".format(str(OID)))
            arcpy.MakeFeatureLayer_management(in_features = points,
                                              out_layer = "point",
                                              where_clause = OID)
            arcpy.AddMessage("    Created point: {}".format(str(row[0])))

            # Snap pour point to flow accumulation raster
            
            snapPour = arcpy.sa.SnapPourPoint(in_pour_point_data = "point",
                                              in_accumulation_raster = FAC,
                                              snap_distance = snap_distance)
            arcpy.AddMessage("    Snap pour point complete")

            # Create watershed raster
            watershed = arcpy.sa.Watershed(in_flow_direction_raster = FDR,
                                           in_pour_point_data = snapPour,
                                           pour_point_field = "Value")

            # Convert watershed to polygon
            watershed_name = "watershed_{}".format(str(row[0]).replace(" ", "_"))
            out_poly = os.path.join(output_workspace, watershed_name)
            arcpy.RasterToPolygon_conversion(in_raster = watershed,
                                             out_polygon_features = out_poly)
            arcpy.AddMessage("    Delineate watershed complete")

            # Tabulate landcover area
            if landcover:
                table_name = "lc_table_{}".format(str(row[0]).replace(" ", "_"))
                out_table = os.path.join(output_workspace, table_name)
                arcpy.sa.TabulateArea(in_zone_data = watershed,
                                      zone_field = "Value",
                                      in_class_data = LC,
                                      class_field = "Value",
                                      out_table = out_table,
                                      processing_cell_size = lc_cell_size)
                arcpy.AddMessage("    Tabulate landcover area complete")
            
    # Merge tabulate landcover area tables
    if landcover:
        lc_tables = arcpy.ListTables(wild_card = "lc_table_*")
        arcpy.AddMessage("landcover tables: {}".format(str(lc_tables)))
        lc_table = os.path.join(output_workspace, "lc_table")
        arcpy.Merge_management(inputs = lc_tables, 
                               output = lc_table)
        # Delete landcover lc_tables
        for table in lc_tables:
            arcpy.Delete_management(table)
        arcpy.AddMessage("Merged landcover area tables")
    
    # Merge watershed polygons
    watershed_fcs = arcpy.ListFeatureClasses("watershed_*")
    arcpy.AddMessage("Watershed polygons: {}".format(str(watershed_fcs)))
    watersheds = os.path.join(output_workspace, "watersheds")
    arcpy.Merge_management(inputs = watershed_fcs,
                           output = watersheds)
    
    # Delete watershed FCs
    for fc in watershed_fcs:
        arcpy.Delete_management(fc)
    arcpy.AddMessage("Merged watershed polygons")
    
    # Add point_ID_field to watersheds
    arcpy.MakeTableView_management(in_table = points, 
                                   out_view = "points_table")
    
    arcpy.JoinField_management(in_data = watersheds,
                               in_field = "gridcode",
                               join_table = "points_table",
                               join_field = "OBJECTID")
    arcpy.AddMessage("Added points fields to watersheds fc")
    
    # Join Landcover table to watersheds
    if landcover:
        arcpy.JoinField_management(in_data = watersheds,
                                   in_field = "gridcode",
                                   join_table = lc_table,
                                   join_field = "VALUE")
        arcpy.AddMessage("Added landcover fields to watersheds fc")
    
    # Return
    arcpy.SetParameter(7, watersheds)
    
    # Clean up
    if landcover:
        arcpy.Delete_management(in_data = lc_table)


def main():
    # Call the Point Landcover with command line parameters
    PointLandcover(output_workspace, points, point_ID_field, 
                   flow_accumulation, flow_direction_d8, snap_distance, 
                   landcover)

if __name__ == "__main__":
    # Get input parameters
    output_workspace     = arcpy.GetParameterAsText(0)
    points               = arcpy.GetParameterAsText(1)
    point_ID_field       = arcpy.GetParameterAsText(2)
    flow_accumulation    = arcpy.GetParameterAsText(3)
    flow_direction_d8    = arcpy.GetParameterAsText(4)
    snap_distance        = arcpy.GetParameterAsText(5)
    landcover            = arcpy.GetParameterAsText(6)
    
    main()
