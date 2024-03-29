"""____________________________________________________________________________
Script Name:          _12_XSWatershedArea.py
Description:          Adds watershed area to each cross section.
Date:                 01/26/2024

Usage:
Calculates the watershed area upstream of the input cross section. Writes the
value to a new field in the flowline feature class.

This tool assumes that there is a field in the cross section feature class
called `Seq` (long) that uniquely identifies each cross section.

This tool also adds the stream `ReachName` field from the flowline feature 
class.

This tool runs much faster if the regional flow accumulation raster is clipped 
to the flowline extent. 

Parameters:
feature_dataset       -- Path to the feature dataset
cross_section         -- Path to the cross section line feature class
flowline              -- Path to the flowline feature class
flow_accum            -- Path to the flow accumulation model
snap_distance         -- The distance the cross section-flowline intersection
                         point will be snapped to find the cell of highest
                         flow accumulation

Outputs:
Writes the watershed area to a new field `Watershed_Area_SqMile` in the
cross_section feature class.
____________________________________________________________________________"""

import os
import arcpy

def XSWatershedArea(feature_dataset, cross_section, flowline, flow_accum,
                    snap_distance):
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    arcpy.env.scratchWorkspace = os.path.dirname(feature_dataset)

    # Cast flow_accum as a raster
    FAC = arcpy.Raster(flow_accum)

    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Cross Section: "
                     "{}".format(arcpy.Describe(cross_section).baseName))
    arcpy.AddMessage("Flowline: "
                     "{}".format(arcpy.Describe(flowline).baseName))
    arcpy.AddMessage("FAC: {}".format(arcpy.Describe(FAC).baseName))
    arcpy.AddMessage("Snap distance: {}".format(snap_distance))

    # Get spatial reference of FAC
    spatial_ref = arcpy.Describe(FAC).spatialReference

    # Check if the ReachName field exists in the cross_section fc. If so delete
    # it so that it can be updated. It must be deleted so that it does not get
    # confused with the ReachName field in the flowline fc during Intersect.
    field_names = [f.name for f in arcpy.ListFields(cross_section)]
    if "ReachName" in field_names:
        arcpy.management.DeleteField(in_table = cross_section,
                                     drop_field = ["ReachName"])

    # Intersect cross_section with flowline
    xs_flowline_pt = os.path.join(feature_dataset, "xs_flowline_pt")
    arcpy.analysis.Intersect(in_features = [cross_section, flowline],
                             out_feature_class = xs_flowline_pt,
                             output_type = "POINT")

    # Add a field to to the cross_section fc to hold watershed area
    # Check if the field already exists and if not add it
    field_names = [f.name for f in arcpy.ListFields(cross_section)]
    if "Watershed_Area_SqMile" not in field_names:
        arcpy.management.AddField(cross_section, "Watershed_Area_SqMile",
                                  "DOUBLE")

    # Add a field to the cross section feature class to hold the name of the
    # reach from the flowline feature class
    arcpy.AddField_management(cross_section, "ReachName", "TEXT")

    # Add a field to cross_section fc to hold flowline_elevation

    # Iterate through `cross_section` fc and calculate watershed area
    with arcpy.da.UpdateCursor(in_table = cross_section,
                               field_names = ['Seq',
                                              'Watershed_Area_SqMile',
                                              'ReachName'],
                               sql_clause = (None, 'ORDER BY Seq')) as cursor:
        for row in cursor:
            # Create a feature layer from the xs_flowline_pt feature class
            # for the current cross section
            OID = "Seq = {}".format(str(row[0]))
            arcpy.management.MakeFeatureLayer(
                      in_features = xs_flowline_pt,
                      out_layer = "xs_flowln_pt",
                      where_clause = OID)

            # Set the stream `ReachName` field
            whr_cls = "Seq = {}".format(str(row[0]))
            xs_fl_pts = arcpy.SearchCursor(dataset = "xs_flowln_pt",
                                           fields = "Seq; ReachName",
                                           where_clause = whr_cls)

            for xs in xs_fl_pts:
                seq        = xs.getValue("Seq")
                reach_name = xs.getValue("ReachName")
                arcpy.AddMessage("Seq: {0}, ReachName: {1}".format(seq,
                                 reach_name))
                row[2] = reach_name

            # Calculate Watershed Area
            ## Snap pour point to flow accumulation raster
            snapPour = arcpy.sa.SnapPourPoint(
                                in_pour_point_data = "xs_flowln_pt",
                                in_accumulation_raster = FAC,
                                snap_distance = snap_distance,
                                pour_point_field = "Seq")
            arcpy.AddMessage("    Snap complete")
            
            ## Sample the flow accum raster to determine # of upstream cells
            watershed_area = os.path.join(arcpy.env.workspace, "watershed_area")
            arcpy.sa.Sample(in_rasters = [FAC],
                            in_location_data = snapPour,
                            out_table = watershed_area,
                            resampling_type = "NEAREST",
                            unique_id_field = "Value")
            arcpy.AddMessage("    Sample complete")

            flds = arcpy.ListFields(watershed_area)
            for f in flds:
                arcpy.AddMessage("        Field: {0}".format(f.name))
            
            ## Extract cell count from watershed_area table
            cell_count = 0
            FACname     = flds[4].name
            fields      = flds[1].name + "; " + flds[4].name
            whereClause = flds[1].name + " = " + str(row[0])
            counts = arcpy.SearchCursor(dataset = watershed_area,
                                        fields = fields,
                                        where_clause = whereClause)
            for count in counts:
                cell_count = count.getValue(FACname)
                arcpy.AddMessage("    Cell Count: " + str(cell_count))
                # Calculate the area in square miles
                cell_size = str(
                            arcpy.GetRasterProperties_management(
                                  FAC, "CELLSIZEX"))
                arcpy.AddMessage("    Cell Size: " + cell_size)
                
                # Linear unit = meter
                if spatial_ref.linearUnitName == "Meter":
                    # 1 sq m = 0.0000003861 sq mile
                    area_sq_mile = ((float(cell_size) * float(cell_size)) *
                                    0.0000003861) * cell_count
                    if area_sq_mile < 0.25:
                        # Error, valid watershed area should be larger
                        arcpy.AddMessage("Watershed area is less than one quarter"
                            " of a square mile. Try increasing the snap distance.")
                    else:
                        arcpy.AddMessage("    Area: " + str(area_sq_mile))
                
                # Linear unit = feet
                elif spatial_ref.linearUnitName == "Feet":
                    # 1 sq ft = 0.00000003587 sq mile
                    area_sq_mile = ((float(cell_size) * float(cell_size)) *
                                    0.00000003587) * cell_count
                    if area_sq_mile < 0.25:
                        # Error, valid watershed area should be larger
                        arcpy.AddMessage("Watershed area is less than one quarter"
                            " of a square mile. Try increasing the snap distance.")
                    else:
                        arcpy.AddMessage("    Area: " + str(area_sq_mile))
                
                else:
                    # Error
                    arcpy.AddError("    Watershed linear unit not recognized."
                          " Area not calculated")
                
                # Write the watershed area to the cross section table
                row[1] = area_sq_mile
            # Update cross_section row
            cursor.updateRow(row)

    # Return
    arcpy.SetParameter(5, cross_section)
    
    # Cleanup
    arcpy.management.Delete(in_data = xs_flowline_pt)
    arcpy.management.Delete(in_data = watershed_area)


def main():
    XSWatershedArea(feature_dataset, cross_section, flowline, flow_accum,
                    snap_distance)

if __name__ == "__main__":
    feature_dataset  = arcpy.GetParameterAsText(0)
    cross_section    = arcpy.GetParameterAsText(1)
    flowline         = arcpy.GetParameterAsText(2)
    flow_accum       = arcpy.GetParameterAsText(3)
    snap_distance    = arcpy.GetParameterAsText(4)

    main()

