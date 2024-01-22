# Utility R functions for the ArcGIS FluvialGeomorph toolbox. 

# Declare location of script within the toolbox
here::i_am("install/FG_utils.R")

#' @title Load needed packages
#' 
#' @description Loads specified packages. 
#' 
#' @export
#' @param need_pkgs      A character vector of package names.
#' 
#' @return Loads the requested packages.
#' 
load_packages <- function(need_pkgs) {
    # Load all needed packages
    lapply(need_pkgs, require, character.only = TRUE)
}


#' @title Install needed packages
#' 
#' @description Tests if packages are installed and if not installs them.
#' 
#' @export
#' @param need_pkgs      A character vector of package names.
#' 
#' @return Installs the requested packages.
#' 
install_needed_packages <- function(need_pkgs) {
    # Set CRAN repository
    message("Setting CRAN repository...")
    r <- getOption("repos")
    r["CRAN"] <- "https://cran.rstudio.com/"
    options(repos = r)
    
    # Don't compile from source
    #options(install.packages.check.source = "no")
    
    # Update existing packages
    message("Updating packages...")
    update.packages(lib.loc = .libPaths()[1], 
                    ask = FALSE, 
                    checkBuilt = TRUE,
                    type = "win.binary")
    
    # Determine the uninstalled packages from need_pkgs
    uninst_pkgs <- need_pkgs[!(need_pkgs %in% installed.packages()[, "Package"])]
    
    # Install uninstalled packages
    if (length(uninst_pkgs)) {
        message("Installing missing packages...")
        install.packages(uninst_pkgs, 
                         Ncpus = 5,
                         dependencies = TRUE,
                         type = "win.binary")
    }
}


#' @title Install FluvialGeomorph R packages
#' 
#' @description Installs the required R packages for the ArcGIS FluvialGeomorph
#'     toolbox. 
#' 
#' @export
#' @param force      logical; Force installation? Defaults to FALSE.
#'  
#' @return Installs the required ArcGIS FluvialGeomorph R packages. 
#' 
#' @details This function installs the \code{RegionalCurve} R package from 
#'     GitHub and the \code{fluvgeo} R package from a local source tarball. 
#' 
install_fluvgeo_packages <- function(force = FALSE) {
    # Install remotes
    if (!require("remotes")) { 
        install.packages("remotes", dependencies = TRUE)
        if ("remotes" %in% rownames(installed.packages()) == TRUE) {
            message("The `remotes` package was installed.")
        }
    }
    
    # Install `RegionalCurve` from GitHub
    message("Installing RegionaCurve from GitHub...")
    remotes::install_github(repo = "FluvialGeomorph/RegionalCurve@*release",
                            force = force,
                            upgrade = TRUE,
                            dependencies = TRUE,
                            type = "win.binary")
    
    # Install `fluvgeo` from from GitHub
    message("Installing fluvgeo from GitHub...")
    remotes::install_github(repo = "FluvialGeomorph/fluvgeo@*release",
                            force = force,
                            upgrade = TRUE, 
                            dependencies = TRUE,
                            type = "win.binary")
}


#' @title Set pandoc path
#' 
#' @export
#' 
#' @description Determine if \code{pandoc} is installed and set an R environment
#'     variable and tell rmarkdown. 
#' 
#' @details This function is needed to be able to use pandoc outside of an 
#'     RStudio session. It detects the pandoc installation path and sets the 
#'     R environment variable \code{RSTUDIO_PANDOC} to the installation path. 
#'     It also tells rmarkdown where to find pandoc. 
#' 
set_pandoc <- function() {
    if (rmarkdown::pandoc_available()) {
        # pandoc already available
        message(paste("Pandoc available: ", rmarkdown::pandoc_available()))
        message("pandoc version: ", rmarkdown::pandoc_version())
        message("Find pandoc: ",  rmarkdown::find_pandoc()$dir)
    } else if (!Sys.which("pandoc") == "") {
        # Check if pandoc location detectable by Sys.which
        # Set R environment variable
        Sys.setenv(RSTUDIO_PANDOC = dirname(Sys.which("pandoc")))
        # Tell rmarkdown directly
        rmarkdown::find_pandoc(dir = dirname(Sys.which("pandoc")))
        message("pandoc discovery method: Sys.which")
        message("Using pandoc: ", dirname(Sys.which("pandoc")))
        message("Find pandoc: ",  rmarkdown::find_pandoc()$dir)
    } else if (file.exists("C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools/pandoc.exe")) {
        # Check if pandoc is installed by RStudio, current RStudio
        # Set R environment variable
        Sys.setenv(RSTUDIO_PANDOC  = "C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools")
        # Tell rmarkdown directly
        rmarkdown::find_pandoc(dir = "C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools")
        message("pandoc discovery method: RStudio Quarto")
        message("Using pandoc: C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools" )
        message("Find pandoc: ",  rmarkdown::find_pandoc()$dir)
    } else if (file.exists("C:/Program Files/Quarto/bin/tools/pandoc.exe")) {
        # Check if pandoc is installed by Quarto, current quarto
        # Set R environment variable
        Sys.setenv(RSTUDIO_PANDOC  = "C:/Program Files/Quarto/bin/tools")
        # Tell rmarkdown directly
        rmarkdown::find_pandoc(dir = "C:/Program Files/Quarto/bin/tools")
        message("pandoc discovery method: Quarto")
        message("Using pandoc: C:/Program Files/Quarto/bin/tools" )
        message("Find pandoc: ",  rmarkdown::find_pandoc()$dir)
    } else if (file.exists("C:/Program Files/RStudio/bin/quarto/bin/pandoc.exe")) {
        # Check if pandoc is installed by RStudio, early RStudio Quarto
        # Set R environment variable
        Sys.setenv(RSTUDIO_PANDOC  = "C:/Program Files/RStudio/bin/quarto/bin")
        # Tell rmarkdown directly
        rmarkdown::find_pandoc(dir = "C:/Program Files/RStudio/bin/quarto/bin")
        message("pandoc discovery method: Early RStudio Quarto")
        message("Using pandoc: C:/Program Files/RStudio/bin/quarto/bin" )
        message("Find pandoc: ",  rmarkdown::find_pandoc()$dir)
    } else if (file.exists("C:/Program Files/RStudio/bin/pandoc/pandoc.exe")) {
        # Check if pandoc is installed by RStudio, pre quarto
        # Set R environment variable
        Sys.setenv(RSTUDIO_PANDOC  = "C:/Program Files/RStudio/bin/pandoc")
        # Tell rmarkdown directly
        rmarkdown::find_pandoc(dir = "C:/Program Files/RStudio/bin/pandoc")
        message("pandoc discovery method: RStudio Pre Quarto")
        message("Using pandoc: C:/Program Files/RStudio/bin/pandoc" )
        message("Find pandoc: ",  rmarkdown::find_pandoc()$dir)
    } else {
        message("pandoc installation not detected.")
    }
}


#' @title Parameter information
#' 
#' @description Calculates the characteristics of a parameter. 
#' 
#' @param param        character; The parameter.
#' @param param_name   character; The name of the parameter. 
#' 
#' @return A single-row data frame containing the characteristics of a parameter.
#' 
param_info <- function(param, param_name) {
    # Calculate param info fields
    type <- typeof(param)
    
    # Convert into a data frame
    param_row <- tibble(param_name, type)
}


#' @title Parameters information table
#' 
#' @description Calculates a table of parameter characteristics for a set of 
#' parameters. 
#' 
#' @param param_list   list; A list of named parameter values.
#' 
#' @return A data frame of parameters and their characteristics. 
#' 
param_table <- function(param_list) {
    # Get a list of parameter names
    param_names <- as.list(names(param_list))
    
    # Get info on each parameter
    param_info_table <- purrr::map2(.x = param_list, .f = param_info, 
                                    .y = param_names)
    
    # Combine all parameters into a single data frame
    info_table <- dplyr::bind_rows(param_info_table)
}


#' @title Compare tool parameters
#' 
#' @description Compares the parameters passed by ESRI to R. The table returned 
#' helps to troubleshoot data types conversion between ESRI and R. 
#' 
#' @param in_params    list; List of parameter values created by an ESRI 
#'                     script tool.
#' @param param_list   list; List of parameter values in R. List items should 
#'                     be named by the names of the parameters. 
#'                     
#' @return A data frame of parameters and their characteristics. 
#' 
compare_params <- function(in_params, param_list) {
    # Set parameter names for in_params
    param_names <- as.list(names(param_list))
    in_params <- setNames(in_params, param_names)
    
    # Get parameters from ESRI and rename fields
    params_esri <- param_table(in_params)
    params_esri <- dplyr::rename(params_esri, esri_type = type)
    
    # Get parameters in R and rename fields
    params_r <- param_table(param_list)
    params_r <- dplyr::rename(params_r, r_type = type)
    
    # Build a table to comapre the two
    param_table <- dplyr::left_join(params_esri, params_r,
                                    by = "param_name")
    # param_table <- merge(params_esri, params_r, 
    #                      by = "param_name")
}
