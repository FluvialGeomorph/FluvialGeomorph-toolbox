#' @title Check the validity of a `fluvgeo` `bankline_points` data structure
#'
#' @description Checks that the input data structure `bankline_points` meets
#' the requirements for this data structure.
#'
#' @export
#' @param bankline_points_fc  character; a `bankline_points` feature class
#'                            used by the fluvgeo package.
#' 
#' @details This is a wrapper to the `fluvgeo::check_bankline_points` function.
#' 
#' @return Returns TRUE if the `bankline_points` data structure matches the
#' requirements. The function throws an error for a data structure not matching
#' the data specification. Returns errors describing how the the data structure
#' doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_bankline_points.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    
    # gp tool parameters
    bankline_points_fc  <- in_params[[1]]
    
    # Import fc to sf
    bankline_points_sf <- fc2sf(bankline_points_fc)
    
    fc_name <- basename(bankline_points_fc)
    
    # Check bankline_points and print messages
    check <- try(check_bankline_points(bankline_points_sf))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid bankline_points data structure."))
    }
    
    return(out_params)
}