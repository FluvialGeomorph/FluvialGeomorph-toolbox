#' Checks the `loop_points` feature class.
#'
#' Args:
#'    loop_points_fc      character; the full path to an ESRI loop_points 
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
    loop_points_fc  <- in_params[[1]]
    
    # Import fc to sp
    loop_points_sp <- arc2sp(loop_points_fc)
    
    fc_name <- basename(loop_points_fc)
    
    # Check loop_points and print messages
    check <- try(check_loop_points(loop_points_sp))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid loop_points data structure."))
    }
    
    return(out_params)
}