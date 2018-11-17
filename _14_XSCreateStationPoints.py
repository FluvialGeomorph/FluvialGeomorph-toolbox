"""____________________________________________________________________________
Script Name:          _14_XSCreateStationPoints.py
Description:          Creates a new station points feature class from a 
                      stream cross section feature class.  
Date:                 4/20/2018

Usage:
Use this tool to create a new cross section station points feature class 
from a stream cross section feature class.

This tool assumes that there is a field in the cross section feature class 
called `Seq` that uniquely identifies each cross section. 

This tool assumes that cross sections are digitized beginning at the left 
descending bank. In an edit session, use the flip tool to ensure the proper 
direction. A red vertex denotes the end of a line segment. 

The station distance parameter is specified in the linear units of the 
flowline feature class.

This tool names the output feature class using the base name of the input 
cross section feature class. 

Parameters:
output_workspace      -- Path to the output workspace
cross_section         -- Path to the cross section line feature class
dem                   -- Path to the digital elevation model (DEM)
detrend_dem           -- Path to the detrended digital elevation model (DEM)
station_distance      -- Distance between output flowline station points (in 
                         the linear units of the flowline feature class)

Outputs:
<xs_name>_points      -- a new feature class of densified vertices 
                         along the cross section
____________________________________________________________________________"""
 
import arcpy

def XSCreateStationPoints(output_workspace, cross_section, dem, detrend_dem, 
                          station_distance):
    # Check out the extension licenses
    arcpy.CheckOutExtension("3D")
    
    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Cross Section: "
                     "{}".format(arcpy.Describe(cross_section).baseName))
    arcpy.AddMessage("DEM: {}".format(arcpy.Describe(dem).baseName))
    arcpy.AddMessage("Detrended DEM: "
                     "{}".format(arcpy.Describe(detrend_dem).baseName))
    arcpy.AddMessage("Station distance: {0}".format(str(station_distance)))
    
    # Set cross_section name
    xs_name = arcpy.Describe(cross_section).baseName
    
    # Add a field to hold the linear referencing route `from_measure`
    # Check if the field already exists and if not add it
    field_names = [f.name for f in arcpy.ListFields(cross_section)]
    if "from_measure" not in field_names:
        arcpy.AddField_management(in_table = cross_section, 
                                  field_name = "from_measure", 
                                  field_type = "DOUBLE")

    # Set the value of the cross section `from_measure` to zero in units meters
    arcpy.CalculateField_management(in_table = cross_section, 
                                    field = "from_measure", 
                                    expression = "0", 
                                    expression_type = "PYTHON_9.3")

    # Add a field to hold the linear referencing route `to_measure`
    if "to_measure" not in field_names:
        arcpy.AddField_management(in_table = cross_section, 
                                  field_name = "to_measure", 
                                  field_type = "DOUBLE")

    # Set the value of the cross section `to_measure` to the length of the 
    # cross section in units meters
    arcpy.CalculateField_management(in_table = cross_section, 
                                    field = "to_measure", 
                                    expression = "!shape.length@meters!", 
                                    expression_type = "PYTHON_9.3")

    # Densify vertices of the cross_section feature class using the Densify tool. 
    xs_densify = xs_name + "_densify"
    arcpy.CopyFeatures_management(in_features = cross_section, 
                                  out_feature_class = xs_densify)
    arcpy.Densify_edit(in_features = xs_densify, 
                       densification_method = "DISTANCE", 
                       distance = station_distance)

    # Convert the cross_section feature class to a route
    xs_densify_route = xs_name + "_densify_route"
    arcpy.CreateRoutes_lr(in_line_features = xs_densify, 
                          route_id_field = "Seq", 
                          out_feature_class = xs_densify_route, 
                          measure_source = "TWO_FIELDS", 
                          from_measure_field = "from_measure", 
                          to_measure_field = "to_measure")

    # Convert cross section feature vertices to points
    xs_points = xs_name + "_points"
    arcpy.FeatureVerticesToPoints_management(
                     in_features = xs_densify_route, 
                     out_feature_class = xs_points)

    # Add x, y, z, and m values to the `cross_section_points` feature class
    arcpy.AddGeometryAttributes_management(
                     Input_Features = xs_points, 
                     Geometry_Properties = "POINT_X_Y_Z_M", 
                                           Length_Unit = "METERS")

    # Set the first m-value for each cross section to zero. The `create route`
    # tool sets it to NULL. 
    arcpy.CalculateField_management(in_table = xs_points, 
                                    field = "POINT_M", 
                                    expression = "setNull2Zero(!POINT_M!)", 
                                    code_block = """def setNull2Zero(m):
                                                        if m is None: 
                                                            return 0
                                                        else:
                                                            return m""",
                                    expression_type = "PYTHON_9.3")

    # Delete un-needed fields
    arcpy.DeleteField_management(in_table = xs_points, 
                                 drop_field = ["ORIG_FID","POINT_Z"])

    # Join fields from the `cross_section` feature class to the 
    # `cross_section_points` feature class
    arcpy.JoinField_management(
               in_data = xs_points, 
               in_field = "Seq", 
               join_table = cross_section, 
               join_field = "Seq", 
               fields = ["ReachName","Watershed_Area_SqMile","km_to_mouth"])

    # Add elevations to the `cross_section_points` feature class
    arcpy.AddSurfaceInformation_3d(in_feature_class = xs_points, 
                                   in_surface = dem, 
                                   out_property = "Z",
                                   z_factor = 1.0)

    # Change `Z` field name to `DEM_Z`
    arcpy.AlterField_management(in_table = xs_points, 
                                field = "Z", 
                                new_field_name = "DEM_Z")

    # Add detrended elevations to the `cross_section_points` feature class
    arcpy.AddSurfaceInformation_3d(in_feature_class = xs_points, 
                                   in_surface = detrend_dem, 
                                   out_property = "Z",
                                   z_factor = 1.0)

    # Change `Z` field name to `Detrend_DEM_Z`
    arcpy.AlterField_management(in_table = xs_points, 
                                field = "Z", 
                                new_field_name = "Detrend_DEM_Z")

    # Cleanup
    arcpy.Delete_management(in_data = xs_densify)
    arcpy.Delete_management(in_data = xs_densify_route)
    return

def main():
    # Call the XSCreateStationPoints function with command line parameters
    XSCreateStationPoints(output_workspace, cross_section, dem, detrend_dem, 
                          station_distance)

if __name__ == "__main__":
    # Get input parameters
    output_workspace = arcpy.GetParameterAsText(0)
    cross_section    = arcpy.GetParameterAsText(1)
    dem              = arcpy.GetParameterAsText(2)
    detrend_dem      = arcpy.GetParameterAsText(3)
    station_distance = arcpy.GetParameterAsText(4)
    
    main()
