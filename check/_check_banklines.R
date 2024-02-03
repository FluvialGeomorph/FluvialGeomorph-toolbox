#' @title Check the validity of a `fluvgeo` `banklines` data structure
#'
#' @description Checks that the input data structure `banklines` meets
#' the requirements for this data structure.
#'
#' @export
#' @param banklines_fc   character; a `banklines` feature class used
#'                       by the fluvgeo package.
#' 
#' @details This is a wrapper to the `fluvgeo::check_banklines` function.
#' 
#' @return Returns TRUE if the `banklines` data structure matches the
#' requirements. The function throws an error for a data structure not matching
#' the data specification. Returns errors describing how the the data structure
#' doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_banklines.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    
    # gp tool parameters
    banklines_fc  <- in_params[[1]]
    
    # Import fc to sp
    banklines_sf <- fc2sf(banklines_fc)
    
    fc_name <- basename(banklines_fc)
    
    # Check banklines and print messages
    check <- try(check_banklines(banklines_sf))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid banklines data structure."))
    }
    
    return(out_params)
}