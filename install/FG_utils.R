# Utility R functions for the ArcGIS FluvialGeomorph toolbox. 

#' @title Install and load needed packages
#' 
#' @description Tests if packages are installed and if not installs them. Once
#'     packages are installed it loads them. 
#' 
#' @export
#' @param need_pkgs      A character vector of package names.
#' 
#' @return Installs and loads the requested packages.
#' 
#' @details Replaces the `pacman::p_load` function that requires the latest R 
#'     version. This function uses only base R functions. This function only 
#'     installs packages from the currently set repositories (e.g., CRAN, 
#'     CRANextra). 
#' 
load_packages <- function(need_pkgs) {
    # Determine the uninstalled packages from need_pkgs
    uninst_pkgs <- need_pkgs[!(need_pkgs %in% installed.packages()[, "Package"])]
    # Install uninstalled packages
    if (length(uninst_pkgs)) install.packages(uninst_pkgs, dependencies = TRUE)
    # Load all needed packages
    lapply(need_pkgs, require, character.only = TRUE)
}


#' @title Uninstall FluvialGeomorph R packages
#' 
#' @description Uninstalls the the required R packages for the ArcGIS FluvialGeomorph
#'     toolbox. 
#'     
#' @export
#' 
#' @return None
#' 
#' @details This function installs the \code{RegionalCurve} R package from 
#'     GitHub and the \code{fluvgeo} R package from a local source tarball. 
#'     
uninstall_fluvgeo_packages <- function() {
    # Test if RegionalCurve is installed
    if ("RegionalCurve" %in% rownames(installed.packages()) == TRUE) {
        remove.packages(pkgs = "RegionalCurve")
        message("The RegionalCurve package was uninstalled")
    }
    # Test if fluvgeo is installed
    if ("fluvgeo" %in% rownames(installed.packages()) == TRUE) {
        remove.packages(pkgs = "fluvgeo")
        message("The fluvgeo package was uninstalled")
    }
}


#' @title Load FluvialGeomorph R packages
#' 
#' @description Installs the required R packages for the ArcGIS FluvialGeomorph
#'     toolbox. 
#' 
#' @export
#'  
#' @return Installs the required ArcGIS FluvialGeomorph R packages. 
#' 
#' @details This function installs the \code{RegionalCurve} R package from 
#'     GitHub and the \code{fluvgeo} R package from a local source tarball. 
#' 
load_fluvgeo_packages <- function() {
    # Install devtools
    if (!require("devtools")) { 
        install.packages("devtools", dependencies = TRUE)
        if ("devtools" %in% rownames(installed.packages()) == TRUE) {
            message("The `devtools` package was installed.")
        }
    }
    
    # Install `RegionalCurve` from github
    if (!require("RegionalCurve")) {
        devtools::install_github(repo = "FluvialGeomorph/RegionalCurve",
                                 force = TRUE,
                                 upgrade = TRUE,
                                 dependencies = TRUE,
                                 options(install.packages.check.source = "no"))
        if ("RegionalCurve" %in% rownames(installed.packages()) == TRUE) {
            message("The `RegionalCurve` package was installed.")
        }
    } else {
        if ("RegionalCurve" %in% rownames(installed.packages()) == TRUE) {
            message("The `RegionalCurve` package was already installed.")
        }
    }
    
    # Install `fluvgeo` from a local source tarball
    if (!require("fluvgeo")) {
        devtools::install_local("//mvrdfs//egis//Work//Office//Regional//ERDC/EMRRP_Sediment//Methods//fluvgeo_0.1.12.zip",
                                force = TRUE,
                                upgrade = TRUE, 
                                dependencies = TRUE,
                                options(install.packages.check.source = "no"))
        if ("fluvgeo" %in% rownames(installed.packages()) == TRUE) {
           message("The `fluvgeo` package was installed.")
        }
    } else {
        if ("fluvgeo" %in% rownames(installed.packages()) == TRUE) {
           message("The `fluvgeo` package was already installed.")
        }
    }
}


#' @title Set pandoc path
#' 
#' @export
#' 
#' @description Determine if \code{pandoc} is installed and set the path.
#' 
#' @details This function is needed to be able to use pandoc outside of an 
#'     RStudio session. It detects the pandoc installation path and sets the 
#'     R environment variable \code{RSTUDIO_PANDOC} to the installation path. 
#' 
set_pandoc <- function() {
    if (!Sys.which("pandoc") == "") {
        # Check if pandoc is on the path
        # Set R environment variable
        Sys.setenv(RSTUDIO_PANDOC = dirname(Sys.which("pandoc")))
        message("Using pandoc: ", dirname(Sys.which("pandoc")))
    } else if (file.exists("C:\\Program Files\\RStudio\\bin\\pandoc\\pandoc.exe")) {
        # Check if pandoc is installed by RStudio
        # Set R environment variable
        Sys.setenv(RSTUDIO_PANDOC = "C:/Program Files/RStudio/bin/pandoc")
        message("Using pandoc: C:/Program Files/RStudio/bin/pandoc" )
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


#' @title Convert Windows path to forward slashes
#' 
#' @description Convert a Windows file path from double backslashes to single 
#' forward slash file seperators suitable for use in R. 
#' 
#' @param path        character; A windows file path containing escaped 
#'                    backslashs (i.e., \\)
#' 
forward_slash <- function(path) {
    path <- gsub("\\\\", "/", path)
}