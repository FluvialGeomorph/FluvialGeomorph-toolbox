"""____________________________________________________________________________
Script Name:          _symbol_features.py
Description:          Symbolizes an infrastructure features feature class.   
Date:                 04/10/2020

Parameters:
features        -- An infrastructure features feature class. 

Outputs:
Adds input feature class to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("Feature class added to TOC with standard symbolization")

if __name__ == "__main__":
    # Get input parameters
    features = arcpy.GetParameterAsText(0)
    
    main()
