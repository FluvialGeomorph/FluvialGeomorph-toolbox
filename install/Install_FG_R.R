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
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    
    # gp tool parameters
    reinstall <- in_params[[1]]
    
    # Install needed packages
    message("Installing needed pacakges...")
    needed_pkgs <- c("remotes",
                     "assertthat",
                     "conicfit",
                     "dplyr",
                     "ggplot2",
                     "ggrepel", 
                     "grDevices",
                     "maptiles",
                     "methods",
                     "Metrics",
                     "purrr",
                     "raster",
                     "reshape2",
                     "rgdal",
                     "rlang",
                     "rmarkdown",
                     "scales",
                     "sf",
                     "sp",
                     "stats",
                     "stringr",
                     "terra",
                     "terrainr",
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

    # Mute warnings of possible GDAL/OSR exportToProj4() degradation
    options("rgdal_show_exportToProj4_warnings"="none")
    return(out_params)
}