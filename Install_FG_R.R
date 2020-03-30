#' @title Install FluvialGeomorph R packages
#' 
#' @description  Installs the R packages needed by FluvialGeomorph to perform 
#'     the analysis and reporting. 
#' 
#' @export
#' @param reinstall logical; Forces installed packages to be reinstalled.
#' 
#' @return Nothing. Installs needed R packages. 
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    message(paste(objects()))
    #message(as.character(dirname))
    
    # gp tool parameters
    reinstall <- in_params[[1]]
    
    # Uninstall FluvialGeomorph R packages
    if (reinstall == TRUE) {
        uninstall_fluvgeo_packages()
    }
    
    # Load FluvialGeomorph R packages
    load_fluvgeo_packages()
    
    # Set pandoc
    set_pandoc()
    
    return(out_params)
}