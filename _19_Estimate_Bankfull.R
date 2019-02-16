#' @title Estimate bankfull report
#' 
#' @description Produces the bankfull estimate report.
#' 
#' @export
#' @param xs_points           point feature class; A cross section points 
#'                            feature class. 
#' @param regions             character; The regions that a dimension will be
#'                            calculated for. See the regional_curves$region
#'                            field for a complete list.
#' @param from_elevation      numeric; The detrended elevation (in feet) to 
#'                            begin calculating Goodness of Fit (GOF) measures.
#' @param to_elevation        numeric; The detrended elevation (in feet) to end
#'                            calculating Goodness of Fit (GOF) measures.
#' @param by_elevation        numeric; The detrended elevation (in feet) to 
#'                            step by for calculating Goodness of Fit (GOF) 
#'                            measures.
#' @param bf_estimate         numeric; The detrended bankfull elevation (in
#'                            feet) that is used to calculate hydraulic
#'                            geometry.
#' @param stat                character; The statistic to graph "RMSE", "MAE"
#'                            (the default).
#' @param output_dir          character; The output directory for the report.
#' @param output_format       character; The output format of the report. One
#'                            of "html_document", "word_document",
#'                            "pdf_document".
#'
#' @return A report written to the file system in the output fromat requested.
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr", "tibble", "tidyr", "Metrics", "ggplot2",
                    "ggrepel", "knitr", "rmarkdown", "kableExtra", "reshape2",
                    "assertthat"))
    # Load FluvialGeomorph R packages
    load_fgm_packages()
    # Set pandoc
    set_pandoc()
    
    # gp tool parameters
    xs_points_fc        <- in_params[[1]]
    regions             <- c(in_params[[2]], recursive = TRUE)
    from_elevation      <- in_params[[3]]
    to_elevation        <- in_params[[4]]
    by_elevation        <- in_params[[5]]
    bf_estimate         <- in_params[[6]]
    stat                <- in_params[[7]]
    output_dir          <- in_params[[8]]
    output_format       <- in_params[[9]]
    
    # Import fc to sp
    xs_points <- arc2sp(xs_points_fc)
    
    # Determine the stream names
    streams <- unique(xs_points$ReachName)
    
    # Bankfull elevations to examine for sensitivity analysis
    bankfull_elevations <- seq(from = from_elevation,
                               to = to_elevation,
                               by = by_elevation)
    
    # Convert xs_points to a data frame
    xs_pts <- xs_points@data
    
    # Call the estimate_bankfull function to create the report
    estimate_bankfull(xs_points = xs_pts,
                      streams = streams,
                      regions = regions,
                      bankfull_elevations = bankfull_elevations,
                      bf_estimate = bf_estimate,
                      stat = stat,
                      output_dir = output_dir,
                      output_format = output_format)
    
    return(out_params)
}