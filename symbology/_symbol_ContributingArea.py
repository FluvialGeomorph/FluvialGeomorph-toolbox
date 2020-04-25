"""____________________________________________________________________________
Script Name:          _symbol_ContributingArea.py
Description:          Symbolizes a contributing area raster.   
Date:                 04/10/2020

Parameters:
contributing_area     -- A contributing area raster. 

Outputs:
Adds input raster to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("Contributing area added to TOC with standard symbolization")

if __name__ == "__main__":
    # Get input parameters
    contributing_area = arcpy.GetParameterAsText(0)
    
    main()
