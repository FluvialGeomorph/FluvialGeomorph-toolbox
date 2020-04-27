"""____________________________________________________________________________
Script Name:          _symbol_Flowline_Points.py
Description:          Symbolizes a flowline_points feature class.   
Date:                 04/24/2020

Parameters:
flowline_points      -- A flowline_points feature class. 

Outputs:
Adds input feature class to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("Feature class added to TOC with standard symbolization")
    
    # Return
    arcpy.SetParameter(1, flowline_points)

if __name__ == "__main__":
    # Get input parameters
    flowline_points = arcpy.GetParameterAsText(0)
    
    main()
