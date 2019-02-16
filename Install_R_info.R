#' @title R Install Info
#' 
#' @description Reports R installation information. 
#' 
#' @export
#' 
#' @return Reports R installation information. 
#'
tool_exec <- function(in_params, out_params) {
    # Get R session info
    if("devtools" %in% installed.packages()[, "Package"]) {
        print(devtools::session_info())
    } else {
        print(sessionInfo())
        
        # Print R libsPath
        message(paste("R libsPath: ", .libPaths(), collapse = "\n"))
    }
    
    # System environment variables
    print(Sys.getenv())
    
    # Determine if pandoc is available
    print(rmarkdown::pandoc_available())
    
    return(out_params)
}