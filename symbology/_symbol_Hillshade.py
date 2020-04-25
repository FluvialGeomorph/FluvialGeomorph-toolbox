"""____________________________________________________________________________
Script Name:          _symbol_Hillshade.py
Description:          Symbolizes a hillshade raster.   
Date:                 04/10/2020

Parameters:
hillshade        -- A hillshade raster. 

Outputs:
Adds input raster to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("Hillshade added to TOC with standard symbolization")

if __name__ == "__main__":
    # Get input parameters
    dem = arcpy.GetParameterAsText(0)
    
    main()
