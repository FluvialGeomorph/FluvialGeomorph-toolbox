"""____________________________________________________________________________
Script Name:          _01c_DEMFromField.py
Description:          Creates a DEM from field survey points.  
Date:                 1/9/2024

Usage:
The output DEM will have the spatial reference system of the input field survey
points. 

Parameters:
feature_dataset       -- Path to the feature dataset
thalweg_points        -- Path to the thalweg_points feature class. 
field_xs_points       -- Path to the field_xs_points feature class. 
method                -- DEM creation method (one of "Spline" or "TIN"). 
cell_size             -- The cell size of the output DEM (expressed in the 
                         horizontal units of the field survey points). 
spline_type           -- Type of spline to be used (REGULARIZED or TENSION). 
weight                -- Spline weight parameter. 
number_points         -- The number of points used for spline local 
                         approximation. 

Outputs:
DEM_field             -- a new DEM raster saved to the geodatabase
____________________________________________________________________________"""
 
import os
import arcpy

def DEMFromField(feature_dataset, thalweg_points, field_xs_points, method, 
                 cell_size, spline_type, weight, number_points):
    # Check out the extension license 
    arcpy.CheckOutExtension("Spatial")
    
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    arcpy.env.compression = "LZ77"
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    
    # Combine thalweg and cross sections into elevation points fc
    elevation_points = os.path.join(feature_dataset, "elevation_points")
    arcpy.management.Merge(inputs = [thalweg_points, field_xs_points], 
                           output = elevation_points)
    
    # Set DEM cell size
    arcpy.env.cellSize = cell_size
    
    # Set DEM SRS
    srs = arcpy.Describe(elevation_points).spatialReference
    arcpy.env.outputCoordinateSystem = srs
    
    # Create buffer
    min_convex_hull = os.path.join(feature_dataset, "min_convex_hull")
    arcpy.management.MinimumBoundingGeometry(
                              in_features = elevation_points, 
                              out_feature_class = min_convex_hull,
                              geometry_type = "CONVEX_HULL")
    mch_buffer = os.path.join(feature_dataset, "mch_buffer")
    arcpy.analysis.Buffer(in_features = min_convex_hull, 
                          out_feature_class = mch_buffer, 
                          buffer_distance_or_field = "1 Meters")
    arcpy.AddMessage("Created buffer")
    
    if method == "Spline":
        # Set Interpolation Extent, Mask
        arcpy.env.extent = mch_buffer
        arcpy.env.mask = mch_buffer
         
        # Interpolate elevation points to DEM
        dem_spline = arcpy.sa.Spline(in_point_features = elevation_points,
                                     z_field = "Elevation",
                                     cell_size = cell_size,
                                     spline_type = spline_type,
                                     weight = weight,
                                     number_points = number_points)
        arcpy.AddMessage("Interpolation: Spline")
        DEM_field = os.path.join(arcpy.env.workspace, "DEM_field")
        dem_spline.save(DEM_field)
        arcpy.AddMessage("Created DEM using Spline")
    
    if method == "TIN":
        # Create TIN
        parent_gdb_folder = os.path.dirname(arcpy.env.workspace)
        DEM_field_tin = os.path.join(parent_gdb_folder, "DEM_field_tin")
        expression = elevation_points + " Elevation Mass_Points <None>;" + \
                     mch_buffer + " <None> Hard_Clip <None>"
        arcpy.ddd.CreateTin(out_tin = DEM_field_tin, 
                            spatial_reference = srs,
                            in_features = expression, 
                            constrained_delaunay = "DELAUNAY")
        arcpy.AddMessage("Created TIN")
        
        # Export TIN to raster
        DEM_field = os.path.join(arcpy.env.workspace, "DEM_field")
        arcpy.ddd.TinRaster(in_tin = DEM_field_tin, 
                            out_raster = DEM_field, 
                            data_type = "FLOAT", 
                            method = "LINEAR", 
                            sample_distance = "CELLSIZE", 
                            z_factor = 1,
                            sample_value = cell_size)
        arcpy.AddMessage("Created DEM using TIN")
        
        # Cleanup
        arcpy.management.Delete(DEM_field_tin)
    
    # Calculate DEM_field raster statistics
    arcpy.management.CalculateStatistics(in_raster_dataset = DEM_field, 
                                         x_skip_factor = 1,
                                         y_skip_factor = 1, 
                                         ignore_values = [], 
                                         skip_existing = "OVERWRITE")
    arcpy.AddMessage("Calculated raster statistics")
    
    # Create QA fields
    field_names = [f.name for f in arcpy.ListFields(elevation_points)]
    if "Z" not in field_names:
        arcpy.AddField_management(in_table = elevation_points, 
                                  field_name = "Z", 
                                  field_type = "DOUBLE")
    
    if "field_dem_diff" not in field_names:
        arcpy.AddField_management(in_table = elevation_points, 
                                  field_name = "field_dem_diff", 
                                  field_type = "DOUBLE")
    
    # Calculate DEM Z value at elevation_points
    arcpy.sa.AddSurfaceInformation(in_feature_class = elevation_points, 
                                   in_surface = DEM_field, 
                                   out_property = "Z")
    
    # Calculate difference between DEM Z and field survey
    arcpy.management.CalculateField(in_table = elevation_points, 
                                    field = "field_dem_diff", 
                                    expression = "!Elevation! - !Z!", 
                                    expression_type = "PYTHON3")
    
    # Return
    arcpy.SetParameter(8, DEM_field)
    arcpy.SetParameter(9, elevation_points)
    
    # Cleanup
    arcpy.management.Delete(min_convex_hull)
    arcpy.management.Delete(mch_buffer)

    
def main():
    DEMFromField(feature_dataset, thalweg_points, field_xs_points, method, 
                 cell_size, spline_type, weight, number_points)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset = arcpy.GetParameterAsText(0)
    thalweg_points  = arcpy.GetParameterAsText(1)
    field_xs_points = arcpy.GetParameterAsText(2)
    method          = arcpy.GetParameterAsText(3)
    cell_size       = arcpy.GetParameterAsText(4)
    spline_type     = arcpy.GetParameterAsText(5)
    weight          = arcpy.GetParameterAsText(6)
    number_points   = arcpy.GetParameterAsText(7)

    main()
