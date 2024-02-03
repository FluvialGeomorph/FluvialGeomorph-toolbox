#' @title Check the validity of a `fluvgeo` `flowline` data structure
#'
#' @description Checks that the input data structure `flowline` meets
#' the requirements for this data structure.
#'
#' @export
#' @param flowline        character: a `flowline` feature class data structure
#'                        used by the fluvgeo package.
#' @param step            character; last completed processing step. One of
#'                        "create_flowline", "profile_points"
#'
#' @details This is a wrapper to the `fluvgeo::check_flowline` function.
#'
#' @return Returns TRUE if the `flowline` data structure matches the
#' requirements. The function throws an error for a data structure not matching
#' the data specification. Returns errors describing how the the data structure
#' doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_flowline.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    
    # gp tool parameters
    flowline_fc  <- in_params[[1]]
    
    # Import fc to sf
    flowline_sf <- fc2sf(flowline_fc)
    
    fc_name <- basename(flowline_fc)
    
    # Check flowline and print messages
    check <- try(check_flowline(flowline_sf))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid flowline data structure."))
    }
    
    return(out_params)
}