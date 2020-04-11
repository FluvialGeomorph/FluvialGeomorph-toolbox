"""____________________________________________________________________________
Script Name:          _symbol_Banklines.py
Description:          Symbolizes a banklines feature class.   
Date:                 04/10/2020

Parameters:
banklines        -- A banklines feature class. 

Outputs:
Adds input feature class to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("Feature class added to TOC with standard symbolization")

if __name__ == "__main__":
    # Get input parameters
    banklines = arcpy.GetParameterAsText(0)
    
    main()
