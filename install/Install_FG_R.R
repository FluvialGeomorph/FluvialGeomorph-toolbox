#' @title Install FluvialGeomorph R packages
#' 
#' @description  Installs the R packages needed by FluvialGeomorph to perform 
#'     the analysis and reporting. 
#' 
#' @export
#' @param reinstall logical; Forces installed packages to be re-installed.
#' 
#' @return None. Installs needed R packages. 
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    source("FG_utils.R")
    message("Sourcing utility functions...")
    
    # gp tool parameters
    reinstall <- in_params[[1]]
    
    # Install needed packages
    message("Installing needed pacakges...")
    needed_pkgs <- c("assertthat",
                     "conicfit",
                     "dplyr",
                     "ggplot2",
                     "ggrepel",
                     "grDevices",
                     "here",
                     "methods",
                     "Metrics",
                     "maptiles",
                     "purrr",
                     "raster",
                     "reshape2",
                     "rlang",
                     "rmarkdown",
                     "scales",
                     "sf",
                     "stats",
                     "stringr",
                     "terra",
                     "terrainr",
                     "testthat",
                     "tidyr",
                     "tmap",
                     "utils")
    install_needed_packages(needed_pkgs)
    
    # Load FluvialGeomorph R packages
    message("Installing FluvialGeomorph packages...")
    install_fluvgeo_packages(force = reinstall)
    
    # load packages
    message("Loading packages...")
    load_packages("fluvgeo")
    
    # Set pandoc
    message("Setting pandoc directory...")
    set_pandoc()

    return(out_params)
}