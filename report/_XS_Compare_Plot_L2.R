#' @title Cross Section Compare Plot, Level 2
#' 
#' @description Produces a cross section profile plot for the specified cross
#' section for the input surveys.
#'     
#' @export
#' @param stream          character; The name of the stream.
#' @param xs_number       integer; The cross section `Seq` number.
#' @param xs_points_1     character; Path to the cross section points feature 
#'                        class of the first survey.
#' @param xs_points_2     character; Path to the cross section points feature 
#'                        class of the second survey. 
#' @param xs_points_3     character; Path to the cross section points feature 
#'                        class of the third survey.
#' @param xs_points_4     character; Path to the cross section points feature 
#'                        class of the fourth survey.
#' @param survey_name_1   character; the label to use for the first survey.
#' @param survey_name_2   character; the label to use for the second survey.
#' @param survey_name_3   character; the label to use for the third survey.
#' @param survey_name_4   character; the label to use for the fourth survey.
#' @param bf_elevation    numeric; The detrended bankfull elevation (in
#'                        feet) that is used to calculate hydraulic
#'                        geometry.
#' @param aspect_ratio    numeric; The aspect ratio of the graph.
#' @param extent          character; The extent of the cross section to
#'                        plot. One of "all", "floodplain", or "channel".
#' 
#' @return A ggplot object
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("report/_XS_Compare_Plot_L2.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("dplyr", "purrr", "ggplot2"))
    
    # gp tool parameters
    stream          <- in_params[[1]]
    xs_number       <- in_params[[2]]
    xs_points_1     <- in_params[[3]]
    xs_points_2     <- in_params[[4]]
    xs_points_3     <- in_params[[5]]
    xs_points_4     <- in_params[[6]]
    survey_name_1   <- in_params[[7]]
    survey_name_2   <- in_params[[8]]
    survey_name_3   <- in_params[[9]]
    survey_name_4   <- in_params[[10]]
    bf_elevation    <- in_params[[11]]
    aspect_ratio    <- in_params[[12]]
    extent          <- in_params[[13]]
    
    # Create list of survey paths
    xs_points_paths <- list(xs_points_1, xs_points_2, xs_points_3, xs_points_4)
    
    # Name the survey paths list by their survey names
    survey_names <- c(survey_name_1, survey_name_2, survey_name_3, survey_name_4)
    xs_points_paths <- setNames(xs_points_paths, survey_names)
    
    # Eliminate empty surveys
    xs_points_paths <- purrr::discard(xs_points_paths, is.null)
    
    # Convert list of survey paths to list of sf objects
    xs_pts_sf_list <- purrr::map(xs_points_paths, fluvgeo::fc2sf)
    
    # Call the graph function
    print(fluvgeo::xs_compare_plot_L2(stream = stream,
                                      xs_number = xs_number,
                                      xs_pts_sf_list = xs_pts_sf_list,
                                      bankfull_elevation = bf_elevation,
                                      aspect_ratio = aspect_ratio,
                                      extent = extent))
    
    return(out_params)
}