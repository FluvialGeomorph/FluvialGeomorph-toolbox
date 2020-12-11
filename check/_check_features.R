#' Checks the `features` feature class.
#'
#' Args:
#'    features_fc  character; the full path to an ESRI features 
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
    features_fc  <- in_params[[1]]
    
    # Import fc to sp
    features_sp <- arc2sp(features_fc)
    
    fc_name <- basename(features_fc)
    
    # Check features and print messages
    check <- try(check_features(features_sp))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid features data structure."))
    }
    
    return(out_params)
}