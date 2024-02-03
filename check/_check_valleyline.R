#' @title Check the validity of an `fluvgeo` `valleyline` data structure
#'
#' @description Checks that the input data structure `valleyline` meets
#' the requirements for this data structure.
#'
#' @export
#' @param valleyline_fc   character: a `valleyline` feature class data structure
#'                        used by the fluvgeo package.
#'
#' @return Returns TRUE if the `valleyline` data structure matches the
#' requirements. The function throws an error for a data structure not matching
#' the data specification. Returns errors describing how the the data structure
#' doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_valleyline.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    
    # gp tool parameters
    valleyline_fc  <- in_params[[1]]
    
    # Import fc to sf
    valleyline_sf <- fc2sf(valleyline_fc)
    
    fc_name <- basename(valleyline_fc)
    
    # Check valleyline and print messages
    check <- try(check_valleyline(valleyline_sf))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid valleyline data structure."))
    }
    
    return(out_params)
}