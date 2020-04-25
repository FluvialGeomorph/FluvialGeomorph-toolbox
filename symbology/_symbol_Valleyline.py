"""____________________________________________________________________________
Script Name:          _symbol_Valleyline.py
Description:          Symbolizes a valleyline feature class.   
Date:                 04/10/2020

Parameters:
valleyline        -- A valleyline feature class. 

Outputs:
Adds input feature class to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("Feature class added to TOC with standard symbolization")

if __name__ == "__main__":
    # Get input parameters
    valleyline = arcpy.GetParameterAsText(0)
    
    main()
