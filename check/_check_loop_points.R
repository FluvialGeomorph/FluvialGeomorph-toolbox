#' @title Check the validity of an `fluvgeo` `loop_points` data structure
#'
#' @description Checks that the input data structure `loop_points` meets
#' the requirements for this data structure.
#'
#' @export
#' @param loop_points_fc   character; a `loop_points` feature class data 
#'                         structure used by the fluvgeo package.
#'
#' @details This is a wrapper to the `fluvgeo::check_loop_points` function.
#' 
#' Cross section feature classes evolve as different steps are
#' performed on them. The `step` parameter allows a `loop_points` data
#' structure to be checked throughout its lifecycle. Each step defines a
#' changing set of requirements for the `loop_points` data structure.
#'
#' @return Returns TRUE if the `loop_points` data structure matches the
#' requirements. The function throws an error for a data structure not matching
#' the data specification. Returns errors describing how the the data structure
#' doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_loop_points.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    
    # gp tool parameters
    loop_points_fc  <- in_params[[1]]
    
    # Import fc to sp
    loop_points_sf <- fc2sf(loop_points_fc)
    
    fc_name <- basename(loop_points_fc)
    
    # Check loop_points and print messages
    check <- try(check_loop_points(loop_points_sf))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid loop_points data structure."))
    }
    
    return(out_params)
}