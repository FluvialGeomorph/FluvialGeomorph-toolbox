""" This file tests the outputs of the StreamProfilePoints function
"""
import os
import pytest
import arcpy

from fg_tests_utils import *
from _06_StreamProfilePoints import StreamProfilePoints

# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
flowline         = os.path.join(output_workspace, "flowline")
km_to_mouth      = "0"
dem              = os.path.join(output_workspace, "dem")
station_distance = "5"

# Create test fixtures
@pytest.fixture(scope = "module")
def flowline_points():
    # Call the StreamProfilePoints function with test data
    StreamProfilePoints(output_workspace, flowline, km_to_mouth, dem, 
                        station_distance)
    # Return the flowline_points feature class
    flowline_pts = arcpy.MakeFeatureLayer_management(
                   in_features = os.path.join(output_workspace, 
                                              "flowline_points"), 
                   out_layer = "flowline_pts")
    return flowline_pts

@pytest.fixture(scope = "module")
def flowline_points_stats(flowline_points):
    stat_fields = [["POINT_M", "MIN"], ["POINT_M", "MAX"], 
                   ["Z", "MIN"], ["Z", "MAX"]]
    case_field = "Name"
    fc_stat_table = fc_stats(workspace = output_workspace, 
                             fc = flowline_points, 
                             stat_fields = stat_fields, 
                             case_field = case_field)
    yield fc_stat_table
    arcpy.Delete_management(
                  in_data = os.path.join(output_workspace, "fc_stat_table"))

# Test if feature class exists
def test_fc_exists_flowline_points(flowline_points):
    assert "flowline_points" in list_fcs(output_workspace)

# Test if field exists
def test_field_exists_Name(flowline_points):
    assert "Name" in list_fields(flowline_points)

def test_field_exists_POINT_X(flowline_points):
    assert "POINT_X" in list_fields(flowline_points)

def test_field_exists_POINT_Y(flowline_points):
    assert "POINT_Y" in list_fields(flowline_points)

def test_field_exists_Z(flowline_points):
    assert "Z" in list_fields(flowline_points)

# Test attribute values
def test_POINT_M_min(flowline_points_stats):
    # The minimum POINT_M should be equal to the km_to_mouth parameter value
    assert field_stat(fc_stat_table = flowline_points_stats, 
                      stat_field = "POINT_M", 
                      stat = "MIN", 
                      route_id_field = "Name", 
                      route_name = "Sinsinawa") == float(km_to_mouth)

def test_Z_min(flowline_points_stats):
    # The minimum Z elevation should be at least greater than 600 feet
    assert field_stat(fc_stat_table = flowline_points_stats, 
                      stat_field = "Z", 
                      stat = "MIN", 
                      route_id_field = "Name", 
                      route_name = "Sinsinawa") > 600