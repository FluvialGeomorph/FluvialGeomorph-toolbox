#' Checks a `cross_section` feature class.
#'
#' Args:
#'    cross_section_fc  character; the full path to an ESRI cross_section 
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
    cross_section_fc  <- in_params[[1]]
    
    # Import fc to sp
    cross_section_sp <- arc2sp(cross_section_fc)
    
    fc_name <- basename(cross_section_fc)
    
    # Check cross_section and print messages
    check <- try(check_cross_section(cross_section_sp))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid cross_section data structure."))
    }
    
    return(out_params)
}