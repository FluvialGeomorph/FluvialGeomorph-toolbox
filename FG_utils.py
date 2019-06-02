"""____________________________________________________________________________
Script Name:          FG_utils.py
Description:          Contains a set of Python functions used by 
                      FluvialGeomorph tools. 
Date:                 02/25/2019

Functions:
line_route_points     -- Converts an input line feature class into a route, 
                         densifies its vertices, and returns a point feature 
                         class.  
add_elevation         -- Adds elevation fields to the input feature class.
____________________________________________________________________________"""

import arcpy

def add_elevation(points, dem = "", detrend_dem = ""):
    """
    Adds elevation fields to the input feature class.
    
    Writes all outputs to the environment workspace. 
    
    Args:             
    points            -- Path to a point feature class
    dem               -- Path to the digital elevation model (DEM)
    detrend_dem       -- Path to the detrended digital elevation model (DEM)
    
    Outputs:
    elevation attributes written to the input feature class
    """
    # Add elevations to the `points` feature class
    if dem:
        arcpy.AddSurfaceInformation_3d(in_feature_class = points, 
                                       in_surface = dem, 
                                       out_property = "Z", 
                                       z_factor = 1.0)
        # Change `Z` field name to `DEM_Z`
        arcpy.AlterField_management(in_table = points, 
                                   field = "Z", 
                                   new_field_name = "DEM_Z")
        arcpy.AddMessage("Added DEM elevations")
    else:
        arcypy.AddMessage("DEM not supplied")
    
    # Add detrended elevations to the `points` feature class
    if detrend_dem:
        arcpy.AddSurfaceInformation_3d(in_feature_class = points, 
                                       in_surface = detrend_dem, 
                                       out_property = "Z", 
                                       z_factor = 1.0)
        # Change `Z` field name to `Detrend_DEM_Z`
        arcpy.AlterField_management(in_table = points, 
                                    field = "Z", 
                                    new_field_name = "Detrend_DEM_Z")
        arcpy.AddMessage("Added Detrended DEM elevations")
    else: 
        arcpy.AddMessage("Detrended DEM not supplied")



def line_route_points(line, station_distance, route_id_field, fields):
    """
    Converts an input line feature class into a route, densifies its vertices, 
    and returns a point feature class.
    
    Writes all outputs to the environment workspace. 
    
    Args:
    line              -- Path to a line feature class
    station_distance  -- (numeric) Distance between output line station points 
                         (in the linear units of the line feature class)
    route_id_field    -- (string) of the field name of the route identifier
    fields            -- (string) a list of fields from the line feature class
                         to join to the output line_points feature class (e.g., 
                         ["bank","ReachName"]). 
    
    Outputs:
    <line>_points     -- a point feature class named the same as the line 
                         input feature class written to the current workspace
    """
    # Set line name
    line_name = arcpy.Describe(line).baseName
    
    # Add a field to hold the linear referencing route `from_measure`
    # Check if the field already exists and if not add it
    field_names = [f.name for f in arcpy.ListFields(line)]
    if "from_measure" not in field_names:
        arcpy.AddField_management(in_table = line, 
                                  field_name = "from_measure", 
                                  field_type = "DOUBLE")
    
    # Set the value of the line `from_measure` to zero in units meters
    arcpy.CalculateField_management(in_table = line, 
                                    field = "from_measure", 
                                    expression = "0", 
                                    expression_type = "PYTHON_9.3")

    # Add a field to hold the linear referencing route `to_measure`
    if "to_measure" not in field_names:
        arcpy.AddField_management(in_table = line, 
                                  field_name = "to_measure", 
                                  field_type = "DOUBLE")
    
    # Set the value of the line `to_measure` to the length of the 
    # line in units meters
    arcpy.CalculateField_management(in_table = line, 
                                    field = "to_measure", 
                                    expression = "!shape.length@meters!", 
                                    expression_type = "PYTHON_9.3")
    arcpy.AddMessage("Added route 'from_measure' and 'to_measure' fields to " 
                     + str(line_name))
    
    # Densify vertices of the line feature class using the Densify tool. 
    line_densify = line_name + "_densify"
    arcpy.CopyFeatures_management(in_features = line, 
                                  out_feature_class = line_densify)
    arcpy.Densify_edit(in_features = line_densify, 
                       densification_method = "DISTANCE", 
                       distance = station_distance)

    # Convert the line feature class to a route
    line_densify_route = line_name + "_densify_route"
    arcpy.CreateRoutes_lr(in_line_features = line_densify, 
                          route_id_field = route_id_field, 
                          out_feature_class = line_densify_route, 
                          measure_source = "TWO_FIELDS", 
                          from_measure_field = "from_measure", 
                          to_measure_field = "to_measure")
    arcpy.AddMessage("Converted " + str(line_name) + " to a route")

    # Convert line feature vertices to points
    line_points = line_name + "_points"
    arcpy.FeatureVerticesToPoints_management(
                     in_features = line_densify_route, 
                     out_feature_class = line_points)
    arcpy.AddMessage("Converted " + str(line_name) + " to points")
    
    # Add x, y, z, and m values to the `line_points` feature class
    arcpy.AddGeometryAttributes_management(
                     Input_Features = line_points, 
                     Geometry_Properties = "POINT_X_Y_Z_M", 
                                           Length_Unit = "METERS")
    
    # Set the first m-value for each line to zero. The `create route`
    # tool sets the first record to NULL. 
    mNull_wc = """{0} IS NULL""".format(
        arcpy.AddFieldDelimiters(line_points, "POINT_M"))
    
    with arcpy.da.UpdateCursor(line_points, "POINT_M", 
                               where_clause = mNull_wc) as cursor:
         for row in cursor:
             row[0] = 0
             cursor.updateRow(row)
    
    # Delete un-needed fields
    arcpy.DeleteField_management(in_table = line_points, 
                                 drop_field = ["ORIG_FID","POINT_Z"])
    
    # Join fields from the `line` to the `line_points` feature class
    arcpy.JoinField_management(
               in_data = line_points, 
               in_field = route_id_field, 
               join_table = line, 
               join_field = route_id_field,
               fields = fields)
    arcpy.AddMessage("Joined fields from " + str(line_name))
    
    # Cleanup
    arcpy.Delete_management(in_data = line_densify)
    arcpy.Delete_management(in_data = line_densify_route)
    
    arcpy.AddMessage("Converted " + str(line_name) + " to points")


