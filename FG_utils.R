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
#'     GitHub and the \code{fgm} R package from a local source tarball. 
#'     
uninstall_fgm_packages <- function() {
    # Test if RegionalCurve is installed
    if ("RegionalCurve" %in% rownames(installed.packages()) == TRUE) {
        remove.packages(pkgs = "RegionalCurve")
        message("The RegionalCurve package was uninstalled")
    }
    # Test if fgm is installed
    if ("fgm" %in% rownames(installed.packages()) == TRUE) {
        remove.packages(pkgs = "fgm")
        message("The fgm package was uninstalled")
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
#'     GitHub and the \code{fgm} R package from a local source tarball. 
#' 
load_fgm_packages <- function() {
    # Install devtools
    if (!require("devtools")) { 
        install.packages("devtools", dependencies = TRUE)
        if ("devtools" %in% rownames(installed.packages()) == TRUE) {
            message("The `devtools` package was installed.")
        }
    }
    
    # Install `RegionalCurve` from github
    if (!require("RegionalCurve")) {
        devtools::install_github(repo = "mpdougherty/RegionalCurve",
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
    
    # Install `fgm` from a local source tarball
    if (!require("fgm")) {
        devtools::install_local("//mvrdfs//egis//Work//Office//Regional//ERDC/EMRRP_Sediment//Methods//fgm_0.1.0.zip",
                                force = TRUE,
                                upgrade = TRUE, 
                                dependencies = TRUE,
                                options(install.packages.check.source = "no"))
        if ("fgm" %in% rownames(installed.packages()) == TRUE) {
           message("The `fgm` package was installed.")
        }
    } else {
        if ("fgm" %in% rownames(installed.packages()) == TRUE) {
           message("The `fgm` package was already installed.")
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

