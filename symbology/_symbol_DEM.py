"""____________________________________________________________________________
Script Name:          _symbol_dem.py
Description:          Symbolizes a Digital Elevation Model (DEM) raster.   
Date:                 04/10/2020

Parameters:
dem        -- A dem raster. 

Outputs:
Adds input raster to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("DEM added to TOC with standard symbolization")

if __name__ == "__main__":
    # Get input parameters
    dem = arcpy.GetParameterAsText(0)
    
    main()
