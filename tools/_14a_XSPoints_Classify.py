"""____________________________________________________________________________
Script Name:          _14a_XSPoints_Classify.py
Description:          Classifies cross section points according to the 
                      floodplain features into which they occur.
Date:                 04/03/2024

Usage:


Parameters:
feature_dataset       -- Path to the feature dataset
xs_points             -- Path to the xs_points feature class
channel_polygon       -- Path to the channel_polygon feature class
floodplain_polygon    -- Path to the floodplain_polygon feature class
buffer_distance       -- Buffer distance around the channel and floodplain 
                         polygon. Use linear units of feature dataset. 

Outputs:
<xs_name>_points      -- the input cross section feature class with new 
                         classification fields added.
                         
____________________________________________________________________________"""
 
import os
import uuid
import arcpy


def _geometry_problem_count(in_features, label):
    scratch_gdb = arcpy.env.scratchGDB
    if not scratch_gdb or not arcpy.Exists(scratch_gdb):
        message = ("Cannot validate the {} polygon because the ArcGIS scratch "
                   "geodatabase is unavailable. Configure a valid scratch "
                   "geodatabase and run the tool again.".format(label))
        arcpy.AddError(message)
        raise RuntimeError(message)

    check_table = os.path.join(
        scratch_gdb, "{}_geometry_check_{}".format(label, uuid.uuid4().hex))
    try:
        arcpy.management.CheckGeometry(in_features, check_table)
        problem_count = int(arcpy.management.GetCount(check_table)[0])
    except arcpy.ExecuteError:
        message = ("Check Geometry failed for the {} polygon '{}'. "
                   "Verify that the input is a readable polygon feature "
                   "class. {}".format(
                       label, in_features,
                       arcpy.GetMessages(2)))
        arcpy.AddError(message)
        raise
    finally:
        if arcpy.Exists(check_table):
            try:
                arcpy.management.Delete(check_table)
            except arcpy.ExecuteError:
                arcpy.AddWarning(
                    "Could not delete geometry check table '{}': {}".format(
                        check_table, arcpy.GetMessages(2)))
    return problem_count


def prepare_polygon_for_buffer(in_features, label):
    """Return a clean polygon input or a repaired copy in the scratch GDB."""
    source_count = int(arcpy.management.GetCount(in_features)[0])
    if source_count == 0:
        message = ("The {} polygon '{}' contains no features. Supply a "
                   "nonempty polygon before classifying XS points.".format(
                       label, in_features))
        arcpy.AddError(message)
        raise RuntimeError(message)
    problem_count = _geometry_problem_count(in_features, label)
    if problem_count == 0:
        arcpy.AddMessage(
            "{} polygon geometry is valid; using the original input.".format(
                label.capitalize()))
        return in_features

    scratch_gdb = arcpy.env.scratchGDB
    repaired_copy = os.path.join(
        scratch_gdb, "{}_repaired_{}".format(label, uuid.uuid4().hex))
    arcpy.AddWarning(
        "{} polygon has {} geometry problem(s); repairing a scratch copy "
        "and leaving the source unchanged.".format(
            label.capitalize(), problem_count))

    try:
        arcpy.management.CopyFeatures(in_features, repaired_copy)
        arcpy.management.RepairGeometry(
            repaired_copy, delete_null="KEEP_NULL")
    except arcpy.ExecuteError:
        message = ("Could not repair the {} polygon '{}' in the scratch "
                   "geodatabase. The source was not modified. {}".format(
                       label, in_features,
                       arcpy.GetMessages(2)))
        arcpy.AddError(message)
        raise

    remaining_problems = _geometry_problem_count(repaired_copy, label)
    if remaining_problems:
        message = ("The {} polygon still has {} geometry problem(s) after "
                   "repair. Buffering was stopped; the source was not "
                   "modified. Recreate or manually repair the polygon."
                   .format(label.capitalize(), remaining_problems))
        arcpy.AddError(message)
        raise RuntimeError(message)

    repaired_count = int(arcpy.management.GetCount(repaired_copy)[0])
    if repaired_count != source_count:
        message = ("Repair changed the {} polygon feature count from {} to "
                   "{}. Buffering was stopped; the source was not modified. "
                   "Review the scratch copy '{}' and repair the polygon "
                   "manually.".format(
                       label, source_count, repaired_count, repaired_copy))
        arcpy.AddError(message)
        raise RuntimeError(message)

    arcpy.AddMessage(
        "{} polygon repaired in scratch workspace: {}".format(
            label.capitalize(), repaired_copy))
    return repaired_copy


def XSPointsClassify(feature_dataset, xs_points, channel_polygon, 
                     floodplain_polygon, buffer_distance):

    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("xs_points: {}".format(arcpy.Describe(xs_points).baseName))
    arcpy.AddMessage("channel_polygon: {}".format(arcpy.Describe(channel_polygon).baseName))
    arcpy.AddMessage("floodplain_polygon: {}".format(arcpy.Describe(floodplain_polygon).baseName))
    arcpy.AddMessage("buffer distance: {}".format(buffer_distance))

    # Validate both polygons before changing the cross-section points.
    channel_polygon_for_buffer = prepare_polygon_for_buffer(
        channel_polygon, "channel")
    floodplain_polygon_for_buffer = prepare_polygon_for_buffer(
        floodplain_polygon, "floodplain")

    # Buffer before changing the cross-section points so failures leave them
    # untouched.
    try:
        arcpy.analysis.Buffer(
            in_features=channel_polygon_for_buffer,
            out_feature_class="channel_polygon_buffer",
            buffer_distance_or_field=buffer_distance)
    except arcpy.ExecuteError:
        arcpy.AddError(
            "Buffer failed for the channel polygon after geometry preflight. "
            "Inspect the ArcGIS Buffer messages and the input geometry.")
        raise

    try:
        arcpy.analysis.Buffer(
            in_features=floodplain_polygon_for_buffer,
            out_feature_class="floodplain_polygon_buffer",
            buffer_distance_or_field=buffer_distance)
    except arcpy.ExecuteError:
        arcpy.AddError(
            "Buffer failed for the floodplain polygon after geometry "
            "preflight. Inspect the ArcGIS Buffer messages and the input "
            "geometry.")
        raise
    arcpy.AddMessage("Floodplain and channel buffered.")
    
    # Add a field to hold the classification flag fields
    # Check if the field already exists and if not add it
    field_names = [f.name for f in arcpy.ListFields(xs_points)]
    if "channel" not in field_names:
        arcpy.management.AddField(in_table = xs_points, 
                                  field_name = "channel", 
                                  field_type = "SHORT")
    
    arcpy.management.CalculateField(in_table = xs_points, 
                                    field = "channel", 
                                    expression = "0", 
                                    expression_type = "PYTHON3")
    
    field_names = [f.name for f in arcpy.ListFields(xs_points)]
    if "floodplain" not in field_names:
        arcpy.management.AddField(in_table = xs_points, 
                                  field_name = "floodplain", 
                                  field_type = "SHORT")
    
    arcpy.management.CalculateField(in_table = xs_points, 
                                    field = "floodplain", 
                                    expression = "0", 
                                    expression_type = "PYTHON3")
    arcpy.AddMessage("Added classification flag fields.")
    
    # Create xs_points feature layer to use for selecting
    arcpy.MakeFeatureLayer_management(xs_points, "xs_points")
    
    # Select xs_points overlaping floodplain
    arcpy.management.SelectLayerByLocation(in_layer = "xs_points",
                                           overlap_type = "INTERSECT", 
                                           select_features = "floodplain_polygon_buffer", 
                                           selection_type = "NEW_SELECTION")
    
    # Set floodplain flag
    arcpy.management.CalculateField(in_table = "xs_points", 
                                    field = "floodplain", 
                                    expression = "1", 
                                    expression_type = "PYTHON3")
    arcpy.AddMessage("xs_points in floodplain set.")
    
    # Select xs_points overlaping channel
    arcpy.management.SelectLayerByLocation(in_layer = "xs_points",
                                           overlap_type = "INTERSECT", 
                                           select_features = "channel_polygon_buffer", 
                                           selection_type = "NEW_SELECTION")
    
    # Set channel flag
    arcpy.management.CalculateField(in_table = "xs_points", 
                                    field = "channel", 
                                    expression = "1", 
                                    expression_type = "PYTHON3")
    arcpy.AddMessage("xs_points in channel set.")
    
    # Clear layer selection
    arcpy.management.SelectLayerByAttribute(in_layer_or_view = "xs_points", 
                                            selection_type = "CLEAR_SELECTION")
    
    # Return
    arcpy.SetParameter(5, xs_points)
    
    return
    
def main():
    XSPointsClassify(feature_dataset, xs_points, channel_polygon, 
                     floodplain_polygon, buffer_distance)

if __name__ == "__main__":
    feature_dataset    = arcpy.GetParameterAsText(0)
    xs_points          = arcpy.GetParameterAsText(1)
    channel_polygon    = arcpy.GetParameterAsText(2)
    floodplain_polygon = arcpy.GetParameterAsText(3)
    buffer_distance    = arcpy.GetParameterAsText(4)

    main()
