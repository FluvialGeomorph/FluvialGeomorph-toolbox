#' @title Update the `regions` parameter's value list
#' 
#' @description Use this code to update the `regions` parameter's value list 
#' with the latest list of values from the `RegionalCurve` R package.
#' 
#' @export
#' 
#' @usage Run the code in this script to get the updated list of regions from 
#' the `RegionalCurve` R package. Then, copy the console output to the 
#' `validate_Estimate_Bankfull.py` and `validate_Level_2_Report.py` 
#' initializeParameters method for the region parameter's value.list. 
#' 
update_regions <- function() {
    require(RegionalCurve)
    
    # Get the list of regions
    regional_curve <- RegionalCurve::regional_curve
    
    # Extract the region names 
    region_names <- levels(regional_curve$region_name)
    
    # Convert the vector of region names into a comma separated list with each 
    # region listed on a new line.
    region_csv <- cat(paste(shQuote(region_names, type="cmd"), 
                            collapse=", \n"))
    return(region_csv)
}