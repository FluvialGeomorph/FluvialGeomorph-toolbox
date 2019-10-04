#' Checks the `valleyline` feature class.
#'
#' Args:
#'    valleyline_fc  character; the full path to an ESRI valleyline 
#'                        feature class
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr", "raster"))
    # Load FluvialGeomorph R packages
    load_fgm_packages()
    
    # gp tool parameters
    valleyline_fc  <- in_params[[1]]
    
    # Import fc to sp
    valleyline_sp <- arc2sp(valleyline_fc)
    
    fc_name <- basename(valleyline_fc)
    
    # Check valleyline and print messages
    check <- try(check_valleyline(valleyline_sp))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid valleyline data structure."))
    }
    
    return(out_params)
}