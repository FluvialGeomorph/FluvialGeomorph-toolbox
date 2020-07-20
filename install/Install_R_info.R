#' @title R Install Info
#' 
#' @description Reports R installation information. 
#' 
#' @export
#' 
#' @return Reports R installation information. 
#'
tool_exec <- function(in_params, out_params) {
    print(sessionInfo())
    # Print R libsPath
    message(paste("R libsPath: ", .libPaths(), collapse = "\n"))
    
    # System environment variables
    print(Sys.getenv())
    
    return(out_params)
}