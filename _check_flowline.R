#' Checks the `flowline` feature class.
#'
#' Args:
#'    flowline_fc  character; the full path to an ESRI flowline 
#'                        feature class
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr", "raster"))
    # Load FluvialGeomorph R packages
    load_fluvgeo_packages()
    
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