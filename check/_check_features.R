#' @title Check the validity of an `fluvgeo` `features` data structure
#'
#' @description Checks that the input data structure `features` meets
#' the requirements for this data structure.
#'
#' @export
#' @param features_fc   character; a `features` feature class used
#'                      by the fluvgeo package.
#'
#' @details This is a wrapper to the `fluvgeo::check_features` function.
#' 
#' @return Returns TRUE if the `features` data structure matches the
#' requirements. The function throws an error for a data structure not matching
#' the data specification. Returns errors describing how the the data structure
#' doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_features.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    
    # gp tool parameters
    features_fc  <- in_params[[1]]
    
    # Import fc to sf
    features_sf <- fc2sf(features_fc)
    
    fc_name <- basename(features_fc)
    
    # Check features and print messages
    check <- try(check_features(features_sf))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid features data structure."))
    }
    
    return(out_params)
}