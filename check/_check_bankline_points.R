#' Checks the `bankline_points` feature class.
#'
#' Args:
#'    bankline_points_fc  character; the full path to an ESRI bankline_points 
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
    bankline_points_fc  <- in_params[[1]]
    
    # Import fc to sp
    bankline_points_sp <- arc2sp(bankline_points_fc)
    
    fc_name <- basename(bankline_points_fc)
    
    # Check bankline_points and print messages
    check <- try(check_bankline_points(bankline_points_sp))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid bankline_points data structure."))
    }
    
    return(out_params)
}