""" This file tests the outputs of the XSAssignRiverPosition function
"""
import os
import pytest
import arcpy

from fg_tests_utils import *
from _13_XSAssignRiverPosition import XSAssignRiverPosition

# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
cross_section    = os.path.join(output_workspace, "cross_section")
flowline_route   = os.path.join(output_workspace, "flowline_densify_route")

# Create test fixtures
@pytest.fixture(scope = "module")
def cross_section_km_to_mouth():
    # Call the XSAssignRiverPosition function with test data
    XSAssignRiverPosition(output_workspace, cross_section, flowline_route)
    # Return the `cross_section` feature class
    xs = arcpy.MakeFeatureLayer_management(in_features = cross_section, 
                                           out_layer = "xs")
    return xs

@pytest.fixture(scope = "module")
def cross_section_stats(cross_section_km_to_mouth):
    stat_fields = [["km_to_mouth", "MIN"], 
                   ["km_to_mouth", "MAX"]]
    case_field = "Seq"
    fc_stat_table = fc_stats(workspace = output_workspace, 
                             fc = cross_section_km_to_mouth, 
                             stat_fields = stat_fields, 
                             case_field = case_field)
    yield fc_stat_table
    arcpy.Delete_management(
              in_data = os.path.join(output_workspace, "fc_stat_table"))

# Test if feature class exists
def test_fc_exists_xs(cross_section_km_to_mouth):
    assert "cross_section" in list_fcs(output_workspace)

# Test if field exists
def test_field_exists_Watershed_Area(cross_section_km_to_mouth):
    assert "km_to_mouth" in list_fields(cross_section_km_to_mouth)

# Test attribute values
def test_Watershed_Area_SqMile_min(cross_section_stats):
    # The `km_to_mouth` field value of the first xs should be less than  
    # 1 km from the `test_06_StreamProfilePoints.py` test run. 
    assert field_stat(fc_stat_table = cross_section_stats, 
                      stat_field = "km_to_mouth", 
                      stat = "MIN", 
                      route_id_field = "Seq", 
                      route_name = 1) < 1

def test_Watershed_Area_SqMile_max(cross_section_stats):
    # The `km_to_mouth` field value of the last xs should be greater than  
    # 1 km  from the `test_06_StreamProfilePoints.py` test run.
    assert field_stat(fc_stat_table = cross_section_stats, 
                      stat_field = "km_to_mouth", 
                      stat = "MAX", 
                      route_id_field = "Seq", 
                      route_name = 5) > 1