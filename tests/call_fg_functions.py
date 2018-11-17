""" This file is used to test FluvialGeomorph script functions.
"""
import sys, os
import arcpy
#sys.path.insert(0, "Z:\Work\Office\Regional\ERDC\EMRRP_Sediment\Methods\FluvialGeomorph")
sys.path.insert(0, os.path.abspath('./'))

from fg_tests_utils import *

"""
from _02_BurnCutlines import BurnCutlines
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
cutlines         = os.path.join(output_workspace, "cutlines")
dem              = os.path.join(output_workspace, "dem")
# Call the BurnCutlines function with test data
BurnCutlines(output_workspace, cutlines, dem)
"""

"""
from _03_ContributingArea import ContributingArea
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
dem              = os.path.join(output_workspace, "dem")
processes        = 10
# Call the ContributingArea function with test data
ContributingArea(output_workspace, dem, processes)
"""

"""
from _04_StreamNetwork import StreamNetwork
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 10000
processes        = 8
# Call the StreamNetwork function with test data
StreamNetwork(output_workspace, contrib_area, threshold, processes)
"""

"""
from _05_CreateFlowline import CreateFlowline
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
stream_network   = os.path.join(output_workspace, "stream_network_edited")
smooth_tolerance = 5
# Call the CreateFlowline function with test data
CreateFlowline(output_workspace, stream_network)
"""

"""
from _06_StreamProfilePoints import StreamProfilePoints
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
flowline         = os.path.join(output_workspace, "flowline")
km_to_mouth      = "0"
dem              = os.path.join(output_workspace, "dem")
station_distance = "5"
# Call the StreamProfilePoints function with test data
StreamProfilePoints(output_workspace, flowline, km_to_mouth, dem, 
                    station_distance)
"""

"""
from _07_DetrendDEM import DetrendDEM
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
flowline_points  = os.path.join(output_workspace, "flowline_points")
dem              = os.path.join(output_workspace, "dem")
buffer_distance  = "200"
# Call the DetrendDEM function with test data
DetrendDEM(output_workspace, flowline_points, dem, buffer_distance)
"""

"""
from _08_BankfullPolygon import BankfullPolygon
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
detrend_dem      = os.path.join(output_workspace, "detrend")
detrend_value    = 104.5
# Call the BankfullPolygon function with test data
BankfullPolygon(output_workspace, detrend_dem, detrend_value)
"""


from _09_ChannelSlope import ChannelSlope
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
dem              = os.path.join(output_workspace, "dem")
banks_poly       = os.path.join(output_workspace, "banks_104_5")
# Call the ChannelSlope function with test data
ChannelSlope(output_workspace, dem, banks_poly)


"""   
from _12_XSWatershedArea import XSWatershedArea
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
cross_section    = os.path.join(output_workspace, "cross_section")
flowline         = os.path.join(output_workspace, "flowline")
flow_accum       = os.path.join(output_workspace, "NHDPlus_FAC")
snap_distance    = "10"
# Call the XSWatershedArea function with test data
XSWatershedArea(output_workspace, cross_section, flowline, flow_accum, 
                    snap_distance)
"""

"""                 
from _13_XSAssignRiverPosition import XSAssignRiverPosition
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
cross_section    = os.path.join(output_workspace, "cross_section")
flowline_route   = os.path.join(output_workspace, "flowline_densify_route")
# Call the XSAssignRiverPosition function with test data
XSAssignRiverPosition(output_workspace, cross_section, flowline_route)
"""

"""
from _14_XSCreateStationPoints import XSCreateStationPoints
# Define test parameters
output_workspace = "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorph/tests/data/test.gdb"
cross_section    = os.path.join(output_workspace, "cross_section")
dem              = os.path.join(output_workspace, "dem")
detrend_dem      = os.path.join(output_workspace, "detrend")
station_distance = "0.5"
# Call the XSCreateStationPoints function with test data
XSCreateStationPoints(output_workspace, cross_section, dem, detrend_dem, 
                          station_distance)
"""

# Use these steps to run this file
# cd to this folder \\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Methods\FluvialGeomorph
# C:\Python27\ArcGIS10.4\python tests\call_fg_functions.py