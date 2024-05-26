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
    # Ensure package `here` is installed and updated
    if(c("here") %in% installed.packages()[, "Package"]) {
        message("Updating `here` package...")
        update.packages(oldPkgs = c("here"), 
                        ask = FALSE, 
                        checkBuilt = TRUE,
                        type = "win.binary")
    } else {
        message("Installing `here` package...")
        install.packages("here",
                         dependencies = TRUE,
                         type = "win.binary")
    }
    # Declare location of script within the toolbox
    here::i_am("install/Install_FG_R.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    
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