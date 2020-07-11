#' @title Install FluvialGeomorph R packages
#' 
#' @description  Installs the R packages needed by FluvialGeomorph to perform 
#'     the analysis and reporting. 
#' 
#' @export
#' @param reinstall logical; Forces installed packages to be re-installed.
#' 
#' @return Nothing. Installs needed R packages. 
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    message(paste(objects()))
    
    # gp tool parameters
    reinstall <- in_params[[1]]
    
    # Install needed packages
    needed_pkgs <- c("assertthat", "dplyr", "ggplot2", "knitr", 
                     "purrr", "raster", "remotes", "rlang", "rmarkdown", 
                     "sf", "sp", "testthat", "tidyr", "tmap", "tmaptools")
    install_packages(needed_pkgs)
    
    # Load FluvialGeomorph R packages
    install_fluvgeo_packages(force = reinstall)
    
    # load packages
    load_packages("fluvgeo")
    
    # Set pandoc
    set_pandoc()
    
    return(out_params)
}