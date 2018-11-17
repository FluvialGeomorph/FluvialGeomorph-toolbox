# Introduction
This document describes how to perform tests of a python package of arcpy 
scripts.

# Package structure
FluvialGeomorph/
|   FluvialGeomorph.tbx
|   __init__.py
|   setup.py
|   _06_StreamProfilePoints.py
|   _12_XSWatershedArea.py
|   _13_XSAssignRiverPosition.py
|   _14_XSCreateStationPoints.py
|   ...
*-- tests/
    |   __init__.py
    |   fg_tests_utils.py
    |   test_06_StreamProfilePoints.py
    |   test_12_XSWatershedArea.py
    |   test_13_XSAssignRiverPosition.py
    |   test_14_XSCreateStationPoints.py
    |    ...
    *------ data/
                data.gdb

# Developing test code
* Test scripts are stored in the FluvialGeomorph/tests/ folder.
* For each srcipt in the FluvialGeomorph package there is a matching script in the /tests folder named for the script prepended with test_.
* Develop test code in ArcMap interactive python window:
    >>> sys.path.insert(0, "Z:\Work\Office\Regional\ERDC\EMRRP_Sediment\Methods\FluvialGeomorph")
    >>> from _06_StreamProfilePoints import StreamProfilePoints


# Configure test environment
* Determine python distrubution: `C:\Python27\ArcGIS10.4`
* Determine if pip is installed: `C:\Python27\ArcGIS10.4\Scripts\pip`
* install pytest using pip: `C:\Python27\ArcGIS10.4\Scripts\pip install -U pytest`
* pytest documentation: `https://docs.pytest.org`

# Running test code
* cd to FluvialGeomorph package folder
* run pytest: `C:\Python27\ArcGIS10.4\Scripts\pytest`