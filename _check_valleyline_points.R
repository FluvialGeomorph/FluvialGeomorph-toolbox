#' Checks the `valleyline_points` feature class.
#'
#' Args:
#'    valleyline_points_fc  character; the full path to an ESRI 
#'                          valleyline_points feature class
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
    valleyline_points_fc  <- in_params[[1]]
    
    # Import fc to sp
    valleyline_points_sp <- arc2sp(valleyline_points_fc)
    
    fc_name <- basename(valleyline_points_fc)
    
    # Check valleyline_points and print messages
    check <- try(check_valleyline_points(valleyline_points_sp))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid valleyline_points data structure."))
    }
    
    return(out_params)
}