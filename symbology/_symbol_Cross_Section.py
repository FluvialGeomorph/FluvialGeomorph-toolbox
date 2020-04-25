"""____________________________________________________________________________
Script Name:          _symbol_cross_section.py
Description:          Symbolizes a cross section feature class.   
Date:                 04/10/2020

Parameters:
cross_section        -- A cross section feature class. 

Outputs:
Adds input feature class to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("Feature class added to TOC with standard symbolization")

if __name__ == "__main__":
    # Get input parameters
    cross_section = arcpy.GetParameterAsText(0)
    
    main()
