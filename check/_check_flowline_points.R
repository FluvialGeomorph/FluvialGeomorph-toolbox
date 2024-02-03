#' @title Check the validity of an `fluvgeo` `flowline_points` data structure
#'
#' @description Checks that the input data structure `flowline_points` meets
#' the requirements for this data structure.
#'
#' @export
#' @param flowline_points   character; a `flowline_points` feature class data
#'                          structure used by the fluvgeo package.
#'
#' @details This is a wrapper to the `fluvgeo::check_flowline_points` function.
#' 
#' @return Returns TRUE if the `flowline_points` data structure matches the
#' requirements. The function throws an error for a data structure not matching
#' the data specification. Returns errors describing how the the data structure
#' doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_flowline_points.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    
    # gp tool parameters
    flowline_points_fc  <- in_params[[1]]
    
    # Import fc to sf
    flowline_points_sf <- fc2sf(flowline_points_fc)
    
    fc_name <- basename(flowline_points_fc)
    
    # Check flowline_points and print messages
    check <- try(check_flowline_points(flowline_points_sf))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid flowline_points data structure."))
    }
    
    return(out_params)
}