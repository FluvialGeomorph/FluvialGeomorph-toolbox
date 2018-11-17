""" This file tests the outputs of the XSWatershedArea function
"""
import os
import pytest
import arcpy

from fg_tests_utils import *
from _12_XSWatershedArea import XSWatershedArea

# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
cross_section    = os.path.join(output_workspace, "cross_section")
flowline         = os.path.join(output_workspace, "flowline")
flow_accum       = os.path.join(output_workspace, "NHDPlus_FAC")
snap_distance    = "10"

# Create test fixtures
@pytest.fixture(scope = "module")
def cross_section_watershed_area():
    # Call the XSWatershedArea function with test data
    XSWatershedArea(output_workspace, cross_section, flowline, flow_accum, 
                    snap_distance)
    # Return the `cross_section` feature class
    xs = arcpy.MakeFeatureLayer_management(in_features = cross_section, 
                                           out_layer = "xs")
    return xs

@pytest.fixture(scope = "module")
def cross_section_stats(cross_section_watershed_area):
    stat_fields = [["Watershed_Area_SqMile", "MIN"], 
                   ["Watershed_Area_SqMile", "MAX"]]
    case_field = "Seq"
    fc_stat_table = fc_stats(workspace = output_workspace, 
                             fc = cross_section_watershed_area, 
                             stat_fields = stat_fields, 
                             case_field = case_field)
    yield fc_stat_table
    arcpy.Delete_management(
              in_data = os.path.join(output_workspace, "fc_stat_table"))

# Test if feature class exists
def test_fc_exists_xs(cross_section_watershed_area):
    assert "cross_section" in list_fcs(output_workspace)

# Test if field exists
def test_field_exists_Watershed_Area(cross_section_watershed_area):
    assert "Watershed_Area_SqMile" in list_fields(
                                            cross_section_watershed_area)

# Test attribute values
def test_Watershed_Area_SqMile_min(cross_section_stats):
    # `Watershed_Area_SqMile` should be > 40sq miles for the test watershed 
    assert field_stat(fc_stat_table = cross_section_stats, 
                      stat_field = "Watershed_Area_SqMile", 
                      stat = "MIN", 
                      route_id_field = "Seq", 
                      route_name = 1) > 40