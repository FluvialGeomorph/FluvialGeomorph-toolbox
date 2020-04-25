"""____________________________________________________________________________
Script Name:          Test_RPy2.py

cross_section         -- Path to the cross section line feature class
____________________________________________________________________________"""

import arcpy
import arcgis

import pandas as pd

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
pandas2ri.activate()
#from rpy2.robjects import default_converter
#from rpy2.robjects.conversion import localconverter


fluvgeo = importr('fluvgeo', lib_loc = r"C:\Users\B5PMMMPD\Documents\R\win-library\3.6")


def do_stuff(cross_section):
    path_xs = r"Z:\Work\Office\Regional\ERDC\EMRRP_Sediment\Methods\fluvgeo\inst\extdata\testing_data.gdb\loop_points"
    
    # Convert `cross_section` to a spatially Enabled (Pandas) DataFrame (SEDF)
    # https://developers.arcgis.com/python/guide/introduction-to-the-spatially-enabled-dataframe/
    xs_sdf = pd.DataFrame.spatial.from_featureclass(path_xs)
    
    # Convert pandas to R
    #with localconverter(default_converter + pandas2ri.converter):
    #  xs_rdf = conversion.py2rpy(xs_sdf)
      
    # Test R output
    print(robjects.r('is.data.frame(xs_sdf)'))

def main():
    # Call the do_stuff function with command line parameters
    do_stuff(cross_section)

if __name__ == "__main__":
    # Get input parameters
    cross_section    = arcpy.GetParameterAsText(0)
    
    main()
