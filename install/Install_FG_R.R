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
    
    # gp tool parameters
    reinstall <- in_params[[1]]
    
    # Install needed packages
    message("Installing needed pacakges...")
    needed_pkgs <- c("assertthat", "backports", "dplyr", "ggplot2", "knitr", 
                     "purrr", "raster", "remotes", "rlang", "rmarkdown", 
                     "sf", "sp", "testthat", "tidyr", "tmap", "tmaptools",
                     "ceramic", "grDevices")
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
    
    # Set Mapbox API key
    message("Setting Mapbox API key...")
    Sys.setenv(MAPBOX_API_KEY="pk.eyJ1IjoibWlrZWRvYyIsImEiOiJja2VwcThtcm4wbHMxMnJxdm1wNjE5eXhmIn0.WE_PG_GiKhpqr6JIJbTsmQ")
    
    # Set ceramic cache
    message("Setting ceramic cache folder...")
    ceramic::ceramic_cache(force = TRUE)
    
    # Mute warnings of possible GDAL/OSR exportToProj4() degradation
    options("rgdal_show_exportToProj4_warnings"="none")
    return(out_params)
}