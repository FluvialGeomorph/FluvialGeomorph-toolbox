"""____________________________________________________________________________
Script Name:          _symbol_Flowline.py
Description:          Symbolizes a flowline feature class.   
Date:                 04/10/2020

Parameters:
flowline        -- A flowline feature class. 

Outputs:
Adds input feature class to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("Feature class added to TOC with standard symbolization")

if __name__ == "__main__":
    # Get input parameters
    flowline = arcpy.GetParameterAsText(0)
    
    main()
