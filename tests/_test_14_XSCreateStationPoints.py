""" This file tests the outputs of the StreamProfilePoints function
"""
import os
import pytest
import arcpy

from fg_tests_utils import *
from _14_XSCreateStationPoints import XSCreateStationPoints

# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
cross_section    = os.path.join(output_workspace, "cross_section")
dem              = os.path.join(output_workspace, "dem")
detrend_dem      = os.path.join(output_workspace, "detrend")
station_distance = "0.5"


# Create test fixtures
@pytest.fixture(scope = "module")
def cross_section_points():
    # Call the XSCreateStationPoints function with test data
    XSCreateStationPoints(output_workspace, cross_section, dem, detrend_dem, 
                          station_distance)
    # Return the `cross_section_points` feature class
    xs_pts = arcpy.MakeFeatureLayer_management(
             in_features = os.path.join(output_workspace, 
                                        "cross_section_points"), 
             out_layer = "xs_pts")
    return xs_pts

@pytest.fixture(scope = "module")
def cross_section_stats(cross_section_points):
    stat_fields = [["DEM_Z", "MIN"], ["DEM_Z", "MAX"], 
                   ["Detrend_DEM_Z", "MIN"], ["Detrend_DEM_Z", "MAX"]]
    case_field = "Seq"
    fc_stat_table = fc_stats(workspace = output_workspace, 
                             fc = cross_section_points, 
                             stat_fields = stat_fields, 
                             case_field = case_field)
    yield fc_stat_table
    arcpy.Delete_management(
              in_data = os.path.join(output_workspace, "fc_stat_table"))

# Test if feature class exists
def test_fc_exists_xs(cross_section_points):
    assert "cross_section_points" in list_fcs(output_workspace)

# Test if fields exists
def test_field_exists_DEM_Z(cross_section_points):
    assert "DEM_Z" in list_fields(cross_section_points)

def test_field_exists_Detrend_DEM_Z(cross_section_points):
    assert "Detrend_DEM_Z" in list_fields(cross_section_points)

# Test attribute values
def test_DEM_Z_min(cross_section_stats):
    # The min `DEM_Z` field value of the first xs should be > 600ft. 
    assert field_stat(fc_stat_table = cross_section_stats, 
                      stat_field = "DEM_Z", 
                      stat = "MIN", 
                      route_id_field = "Seq", 
                      route_name = 1) > 600

def test_DEM_Z_max(cross_section_stats):
    # The max `DEM_Z` field value of the first xs should be < 800ft. 
    assert field_stat(fc_stat_table = cross_section_stats, 
                      stat_field = "DEM_Z", 
                      stat = "MAX", 
                      route_id_field = "Seq", 
                      route_name = 1) < 800

def test_Detrend_DEM_Z_min(cross_section_stats):
    # The min `Detrend_DEM_Z` field value of the first xs should be > 99ft. 
    assert field_stat(fc_stat_table = cross_section_stats, 
                      stat_field = "Detrend_DEM_Z", 
                      stat = "MIN", 
                      route_id_field = "Seq", 
                      route_name = 1) > 99

def test_Detrend_DEM_Z_max(cross_section_stats):
    # The max `Detrend_DEM_Z` field value of the first xs should be < 110ft. 
    assert field_stat(fc_stat_table = cross_section_stats, 
                      stat_field = "Detrend_DEM_Z", 
                      stat = "MAX", 
                      route_id_field = "Seq", 
                      route_name = 1) < 110

