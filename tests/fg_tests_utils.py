""" This module contains utility functions needed for testing tools in the 
FluvialGeomorph package. 
"""
import os
import arcpy

def list_fcs(workspace):
    """Returns a list of feature classes in the specified workspace.
    
    Args:
        workspace (str):  the path to the workspace
      
    Returns:
        list of arcpy feature class objects:  a list of feature classes in 
        the workspace
    """
    arcpy.env.workspace = workspace
    fcs = arcpy.ListFeatureClasses()
    return fcs

def list_fields(fc):
    """Returns a list of fields for the specified feature class.
    
    Args:
        fc (string):  feature class or table object
    
    Returns: 
        list of arcpy field objects:  list of fields in the feature class
    """
    field_names = [f.baseName for f in arcpy.ListFields(fc)]
    return field_names

def fc_stats(workspace, fc, stat_fields, case_field):
    """Returns a table of statistics for the specifed feature class, fields, 
    and cases.
    
    Usage:
    Uses the arcpy "Summary Statistics" tool. See this tool's help for a list 
    of statistics. 
    
    Args:
        workspace (str):    the path to the workspace
        fc (str):           a feature class object
        stat_fields (list): a list of field, stat pairs i.e., [["Z", "MIN"], 
                            ["Z", "MAX"]]
        case_field (str):   the case field that will be used to calculate 
                            summary statistics for
    
    Returns:
        arcpy table object: 
    """
    arcpy.Statistics_analysis(
              in_table = fc, 
              out_table = os.path.join(workspace, "fc_stat_table"), 
              statistics_fields = stat_fields, case_field = case_field)
    fc_stat_table = arcpy.MakeTableView_management(
              in_table = os.path.join(workspace, "fc_stat_table"), 
              out_view = "fc_stat_table")
    return fc_stat_table
    
def field_stat(fc_stat_table, stat_field, stat, route_id_field, route_name):
    """Returns the statistic for the specified feature class, field, 
    statistic, and route. 
    
    Args:
        fc_stat_table (str):  an arcpy table object
        stat_field (str):     the name of the field that the statistics will
                              be returned for
        stat (str):           the statistic to be returned
        route_id_field (str): the name of the route field
        route_name (str):     the value of the route for which the statistic
                              will be returned for
    
    Returns:
        numeric: the value of the requested statistic
    """
    # List the fields for the fc_stat_table
    fields = arcpy.ListFields(fc_stat_table)
    # Select the field object whose field.name == route_name
    route_name_field_obj = next(field for field in fields if field.name == route_id_field)
    # Check if the route_name field type is string
    if route_name_field_obj.type == "String":
        where_clause = "{0} = '{1}'".format(route_id_field, route_name)
    # Check if the route_name field type is integer
    if route_name_field_obj.type == "Integer":
        where_clause = "{0} = {1}".format(route_id_field, route_name)
    # Select the row where the route_id_field == route_name
    rows = arcpy.SearchCursor(dataset = fc_stat_table, 
                              where_clause = where_clause)
    # Get the value of the stat_field
    for row in rows:
        field_name = "{0}_{1}".format(stat, stat_field)
        stat = row.getValue(field_name)
    return stat