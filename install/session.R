#' @title R Session Info
#' 
#' @description Reports the R session info. 
#' 
#' @export
#' 
#' @return None.
#'  
tool_exec <- function(in_params, out_params) {
    require(fluvgeo)
    print(sessionInfo())
}