#' @title Compare longitudinal profile plots from multiple surveys
#' 
#' @description Produces a longitudinal profile plot from the flowline_points
#' of a stream reach taken from different surveys.
#'     
#' @export
#' @param stream              character; The name of the stream.
#' @param flowline_pts_1      character; Path to the flowline points feature 
#'                            class of the first survey.
#' @param flowline_pts_2      character; Path to the flowline points feature 
#'                            class of the second survey.
#' @param flowline_pts_3      character; Path to the flowline points feature 
#'                            class of the third survey.
#' @param flowline_pts_4      character; Path to the flowline points feature 
#'                            class of the fourth survey.
#' @param survey_name_1       character; The label to use for the first survey.
#' @param survey_name_2       character; The label to use for the second survey.
#' @param survey_name_3       character; The label to use for the third survey.
#' @param survey_name_4       character; The label to use for the fourth survey.
#' @param features_fc         character; An infrastructure features feature 
#'                            class.
#' @param profile_units       character; The units of the longitudinal profile.
#'                            One of "kilometers", "meters", "miles", or "feet".
#'                            
#' @return A ggplot object
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("report/_Longitudinal_Profile_Compare.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("dplyr", "purrr", "ggplot2", "fluvgeo"))
    
    # Ensure pandoc can be found
    message("Setting pandoc directory...")
    set_pandoc()
    
    # gp tool parameters
    stream            <- in_params[[1]]
    flowline_points_1 <- in_params[[2]]
    flowline_points_2 <- in_params[[3]]
    flowline_points_3 <- in_params[[4]]
    flowline_points_4 <- in_params[[5]]
    survey_name_1     <- in_params[[6]]
    survey_name_2     <- in_params[[7]]
    survey_name_3     <- in_params[[8]]
    survey_name_4     <- in_params[[9]]
    features_fc       <- in_params[[10]]
    profile_units     <- unlist(in_params[[11]])
    
    # Verify parameters
    ## Create list of parameters (named using the parameter names)
    param_list <- tibble::lst(stream, 
                              flowline_points_1, flowline_points_2, 
                              flowline_points_3, flowline_points_4,
                              survey_name_1, survey_name_2, survey_name_3, 
                              survey_name_4, features_fc, profile_units)
    
    ## Get parameter verification table
    message("Compare input tool parameters")
    print(compare_params(in_params, param_list))
    
    # Create list of survey paths
    print("Assembling survey events")
    flowline_points_paths <- list(flowline_points_1, flowline_points_2, 
                                  flowline_points_3, flowline_points_4)
    
    # Name the survey paths list by their survey names
    survey_names <- c(survey_name_1, survey_name_2, survey_name_3, survey_name_4)
    flowline_points_paths <- setNames(flowline_points_paths, survey_names)
    
    # Eliminate empty surveys
    print("Discarding empty items")
    flowline_points_paths <- purrr::discard(flowline_points_paths, is.null)
    
    # Convert list of survey paths to list of sp objects
    print("Converting flowline_points to sf")
    flowline_pts_sf_list <- purrr::map(flowline_points_paths, fluvgeo::fc2sf)
    
    # Convert features_fc to an sp object
    print("Converting features to sf")
    features_sf <- fluvgeo::fc2sf(features_fc)
    
    # Call the graph function
    print("Calling plot")
    print(fluvgeo::compare_long_profile(stream = stream,
                                    flowline_pts_sf_list = flowline_pts_sf_list,
                                    features_sf = features_sf,
                                    profile_units = profile_units))
    
    return(out_params)
}