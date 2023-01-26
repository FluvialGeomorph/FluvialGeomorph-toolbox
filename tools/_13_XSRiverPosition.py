"""____________________________________________________________________________
Script Name:          _13_XSRiverPosition.py
Description:          Adds a "distance to the mouth of the river" field to 
                      each cross section. 
Date:                 05/27/2020

Usage:
Calculates the river position of the input cross section. Writes the  
value to a new field. 

This tool assumes that there is a field in the cross section feature class 
called `Seq`, field type long integer, that uniquely identifies each cross 
section. 

This tool assumes that there is a field in the flowline feature class 
called `Name` that uniquely identifies each stream reach. 

This tool assumes that the stream flowline is digitized beginning from the 
downstream end of the stream. Open an edit session, select the flowline, 
choose to edit vertices, and ensure that the red endpoint is at the 
downstream end of the flowline. 

Parameters:
feature_dataset       -- Path to the feature_dataset
cross_section         -- Path to the cross section line feature class
flowline_points       -- Path to the flowline route feature class

Outputs:
Writes the river position to a new field `km_to_mouth` field in the cross 
section feature class.
____________________________________________________________________________"""
 
import os
import arcpy

def DeleteExistingFields(in_table, field):
    field_names = [f.name for f in arcpy.ListFields(in_table)]
    if field in field_names:
        arcpy.DeleteField_management(in_table = cross_section, 
                                     drop_field = [field])

def XSAssignRiverPosition(feature_dataset, cross_section, flowline_points):
    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(feature_dataset)
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Cross Section: "
                     "{}".format(arcpy.Describe(cross_section).baseName))
    arcpy.AddMessage("flowline: "
                     "{}".format(arcpy.Describe(flowline_points).baseName))
    
    # Check if the fields that will be joined to the cross section feature class 
    # exist from a previous run. If so, delete the fields before the joins. 
    DeleteExistingFields(cross_section, "km_to_mouth")
    DeleteExistingFields(cross_section, "POINT_X")
    DeleteExistingFields(cross_section, "POINT_Y")
    DeleteExistingFields(cross_section, "POINT_M")
    DeleteExistingFields(cross_section, "Z")
    
    # Spatial Join the cross sections with the closest flowline point
    cross_section_flowline_point = os.path.join(feature_dataset, 
                                                "cross_section_flowline_point")
    arcpy.SpatialJoin_analysis(target_features = cross_section, 
                               join_features = flowline_points, 
                               out_feature_class = cross_section_flowline_point,  
                               match_option = "CLOSEST")

    # Join fields from the `cross_section_flowline_point` table back to the 
    # `cross_section` feature class
    arcpy.JoinField_management(in_data = cross_section, 
                               in_field = "Seq", 
                               join_table = cross_section_flowline_point, 
                               join_field = "Seq", 
                               fields = ["POINT_X", "POINT_Y", "POINT_M", "Z"])
    
    # Calculate the "km_to_mouth" field
    arcpy.AddField_management(in_table = cross_section, 
                              field_name = "km_to_mouth", 
                              field_type = "DOUBLE")
    arcpy.CalculateField_management(in_table = cross_section, 
                                    field = "km_to_mouth",
                                    expression = "!POINT_M!", 
                                    expression_type = "PYTHON_9.3")
    
    # Return
    arcpy.SetParameter(3, cross_section)
    add_chart(cross_section)

    # Cleanup
    arcpy.Delete_management(in_data = cross_section_flowline_point)
    return

def add_chart(cross_section):
    if arcpy.GetInstallInfo()['ProductName'] == "ArcGISPro":
      aprx = arcpy.mp.ArcGISProject("current")
      map = aprx.listMaps()[0]
      cross_section_layer = map.addDataFromPath(cross_section)
      seq_m = arcpy.Chart('XS_Seq_by_POINT_M')
      seq_w = arcpy.Chart('XS_Seq_by_Watershed_Area_SqMile')
    
      seq_m.type = 'scatter'
      seq_m.title = 'XS Seq by km_to_mouth'
      seq_m.description = 'Ensure that XS numbering starts at the downstream end.'
      seq_m.xAxis.field = 'Seq'
      seq_m.yAxis.field = 'km_to_mouth'
      seq_m.xAxis.title = 'Seq'
      seq_m.yAxis.title = 'km_to_mouth'
      seq_m.addToLayer(cross_section_layer)
      
      seq_w.type = 'scatter'
      seq_w.title = 'XS Seq by Watershed Area (sq mile)'
      seq_w.description = 'Ensure that XS watershed areas increase downstream.'
      seq_w.xAxis.field = 'Seq'
      seq_w.yAxis.field = 'Watershed_Area_SqMile'
      seq_w.xAxis.title = 'Seq'
      seq_w.yAxis.title = 'Watershed_Area_SqMile'
      seq_w.addToLayer(cross_section_layer)

def main():
    # Call the XSAssignRiverPosition function with command line parameters
    XSAssignRiverPosition(feature_dataset, cross_section, flowline_points)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset  = arcpy.GetParameterAsText(0)
    cross_section    = arcpy.GetParameterAsText(1)
    flowline_points  = arcpy.GetParameterAsText(2)
    
    main()

