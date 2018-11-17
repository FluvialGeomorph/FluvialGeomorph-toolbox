""" This file tests the outputs of the CleanFlowline function
"""
import os
import pytest
import arcpy

from fg_tests_utils import *
from _05_CleanFlowline import CleanFlowline

# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
stream_network   = os.path.join(output_workspace, "stream_network_edited")

# Create test fixtures
@pytest.fixture(scope = "module")
def flowline():
    # Call the CleanFlowline function with test data
    CleanFlowline(output_workspace, stream_network)
    # Return the flowline feature class
    flowline = arcpy.MakeFeatureLayer_management(
                   in_features = os.path.join(output_workspace, 
                                              "flowline"), 
                   out_layer = "flowline")
    return flowline

@pytest.fixture(scope = "module")
def flowline_stats(flowline):
    stat_fields = [["Name", "FIRST"]]
    case_field = "Name"
    fc_stat_table = fc_stats(workspace = output_workspace, 
                             fc = flowline, 
                             stat_fields = stat_fields, 
                             case_field = case_field)
    yield fc_stat_table
    arcpy.Delete_management(
                  in_data = os.path.join(output_workspace, "fc_stat_table"))
    
# Test if feature class exists
def test_fc_exists_flowline(flowline):
    assert "flowline" in list_fcs(output_workspace)
    
# Test if field exists
def test_field_exists_Name(flowline):
    assert "Name" in list_fields(flowline)

# Test attribute values
def test_Name_first(flowline_stats):
    # The value of `Name` should be "Sinsinawa"
    assert field_stat(fc_stat_table = flowline_stats, 
                      stat_field = "Name", 
                      stat = "FIRST", 
                      route_id_field = "Name", 
                      route_name = "Sinsinawa") == "Sinsinawa"