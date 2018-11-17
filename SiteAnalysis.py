""" This file is used to run analysis for sites
"""

import sys, os
import arcpy

from _02_BurnCutlines import BurnCutlines
from _03_ContributingArea import ContributingArea
from _04_StreamNetwork import StreamNetwork

"""
# GalenaBuncombBridge_05415000
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\GalenaBuncomb_05415000\GalenaBuncombBridge_05415000.gdb"
contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 10000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)


# SouthForkAppleRiver_05418750
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\SouthForkAppleRiver_05418750\SouthForkAppleRiver_05418750.gdb"
contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 10000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)


# NorthForkBadAxe_05387100
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\NorthForkBadAxe_05387100\NorthForkBadAxe_05387100.gdb"
contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 10000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)


# EastBranchPecatonica_05433000
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\EastBranchPecatonica_05433000\EastBranchPecatonica_05433000.gdb"
cutlines         = os.path.join(output_workspace, "cutlines")
dem              = os.path.join(output_workspace, "dem")
BurnCutlines(output_workspace, cutlines, dem)

dem              = os.path.join(output_workspace, "dem_hydro")
processes        = 8
ContributingArea(output_workspace, dem, processes)

contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 10000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)


# EastForkGalenaRiver_05415500
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\EastForkGalenaRiver_05415500\EastForkGalenaRiver.gdb"
cutlines         = os.path.join(output_workspace, "cutlines")
dem              = os.path.join(output_workspace, "dem")
BurnCutlines(output_workspace, cutlines, dem)

dem              = os.path.join(output_workspace, "dem_hydro")
processes        = 8
ContributingArea(output_workspace, dem, processes)

contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 10000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)


# BloodyRunMarquette_05389400
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\BloodyRunMarquette_05389400\BloodyRunMarquette_05389400.gdb"
cutlines         = os.path.join(output_workspace, "cutlines")
dem              = os.path.join(output_workspace, "dem")
BurnCutlines(output_workspace, cutlines, dem)

dem              = os.path.join(output_workspace, "dem_hydro")
processes        = 8
ContributingArea(output_workspace, dem, processes)

contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 10000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)


# GillCreek_05436200
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\GillCreek_05436200\GillCreek_05436200.gdb"
cutlines         = os.path.join(output_workspace, "cutlines")
dem              = os.path.join(output_workspace, "dem")
BurnCutlines(output_workspace, cutlines, dem)

dem              = os.path.join(output_workspace, "dem_hydro")
processes        = 8
ContributingArea(output_workspace, dem, processes)

contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 10000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)


# ElkRiver_05420300
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\ElkRiver_05420300\ElkRiver_05420300.gdb"
dem              = os.path.join(output_workspace, "dem")
processes        = 8
ContributingArea(output_workspace, dem, processes)

contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 50000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)

# GrantRiver05413500
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\GrantRiver05413500\GrantRiver_05413500.gdb"
dem              = os.path.join(output_workspace, "dem")
processes        = 8
ContributingArea(output_workspace, dem, processes)

contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 50000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)
"""

# LittleMakoquetaDubuque_05414600
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\LittleMakoquetaDubuque_05414600\LittleMakoquetaDubuque_05414600.gdb"
cutlines         = os.path.join(output_workspace, "cutlines")
dem              = os.path.join(output_workspace, "dem")
BurnCutlines(output_workspace, cutlines, dem)

dem              = os.path.join(output_workspace, "dem_hydro")
processes        = 8
ContributingArea(output_workspace, dem, processes)

contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 100000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)

# LittleMakoquetaDurango_05414500
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\LittleMakoquetaDurango_05414500\LittleMakoquetaDurango_05414500.gdb"
dem              = os.path.join(output_workspace, "dem")
processes        = 8
ContributingArea(output_workspace, dem, processes)

contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 100000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)

# LittleMakoquetaGraf_05414350
output_workspace = r"\\mvrdfs\egis\Work\Office\Regional\ERDC\EMRRP_Sediment\Sites2\LittleMakoquetaGraf_05414350\LittleMakoquetaGraf_05414350.gdb"
dem              = os.path.join(output_workspace, "dem")
processes        = 8
ContributingArea(output_workspace, dem, processes)

contrib_area     = os.path.join(output_workspace, "contributing_area")
threshold        = 100000
processes        = 8
StreamNetwork(output_workspace, contrib_area, threshold, processes)
