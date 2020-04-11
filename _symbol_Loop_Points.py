"""____________________________________________________________________________
Script Name:          _symbol_Loop_Points.py
Description:          Symbolizes the loop_points feature class.   
Date:                 04/10/2020

Parameters:
loop_points        -- A loop_points feature class. 

Outputs:
Adds input feature class to TOC and applies standard symbolization. 
____________________________________________________________________________"""

import arcpy

def main():
    arcpy.AddMessage("Feature class added to TOC with standard symbolization")

if __name__ == "__main__":
    # Get input parameters
    loop_points = arcpy.GetParameterAsText(0)
    
    main()
