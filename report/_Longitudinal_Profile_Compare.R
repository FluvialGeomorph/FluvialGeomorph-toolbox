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
#'                            class of the secind survey.
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
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("dplyr", "purrr", "sp", "ggplot2"))
    # Load FluvialGeomorph R packages
    load_fluvgeo_packages()
    
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
    
    # Inputs for testing in RStudio
    # library(dplyr)
    # library(tibble)
    # library(purrr)
    # library(arcgisbinding)
    # arc.check_product()
    # library(fluvgeo)
    # 
    # stream <- "Cole Creek R1"
    # flowline_points_1 <- "D:\\Workspace\\EMRRP_Sediment\\PapillionCreek_NE\\Reaches\\02_Cole_Creek\\y2004_R1.gdb\\flowline_points"
    # flowline_points_2 <- "D:\\Workspace\\EMRRP_Sediment\\PapillionCreek_NE\\Reaches\\02_Cole_Creek\\y2010_R1.gdb\\flowline_points"
    # flowline_points_3 <- "D:\\Workspace\\EMRRP_Sediment\\PapillionCreek_NE\\Reaches\\02_Cole_Creek\\y2016_R1.gdb\\flowline_points"
    # flowline_points_4 <- NULL
    # survey_name_1 <- "2004"
    # survey_name_2 <- "2010"
    # survey_name_3 <- "2016"
    # survey_name_4 <- NULL
    # features_fc <- "D:\\Workspace\\EMRRP_Sediment\\PapillionCreek_NE\\Reaches\\02_Cole_Creek\\y2016_R1.gdb\\features"
    # profile_units <- "feet"
    # in_params <- list(stream, flowline_points_1, flowline_points_2,
    #                   flowline_points_3, flowline_points_4, survey_name_1,
    #                   survey_name_2, survey_name_3, survey_name_4,
    #                   features_fc, profile_units)
    
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
    print("Converting features to sp")
    features_sf <- fluvgeo::fc2sf(features_fc)
    
    # Call the graph function
    print("Calling plot")
    print(fluvgeo::compare_long_profile(stream = stream,
                                        flowline_pts_sf_list = flowline_pts_sf_list,
                                        features_sf = features_sf,
                                        profile_units = profile_units))
    
    return(out_params)
}