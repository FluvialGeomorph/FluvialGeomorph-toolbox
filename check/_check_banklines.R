#' Checks the `banklines` feature class.
#'
#' Args:
#'    banklines_fc  character; the full path to an ESRI banklines 
#'                        feature class
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr", "raster", "fluvgeo"))
    
    # gp tool parameters
    banklines_fc  <- in_params[[1]]
    
    # Import fc to sp
    banklines_sp <- arc2sp(banklines_fc)
    
    fc_name <- basename(banklines_fc)
    
    # Check banklines and print messages
    check <- try(check_banklines(banklines_sp))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid banklines data structure."))
    }
    
    return(out_params)
}