#' Checks the `flowline` feature class.
#'
#' Args:
#'    flowline_fc  character; the full path to an ESRI flowline 
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
    flowline_fc  <- in_params[[1]]
    
    # Import fc to sp
    flowline_sp <- arc2sp(flowline_fc)
    
    fc_name <- basename(flowline_fc)
    
    # Check flowline and print messages
    check <- try(check_flowline(flowline_sp))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid flowline data structure."))
    }
    
    return(out_params)
}