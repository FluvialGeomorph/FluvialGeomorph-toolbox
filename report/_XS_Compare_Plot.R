#' @title Cross Section Compare Plot
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
    
    # Inputs for testing in RStudio
    # library(purrr)
    # library(arcgisbinding)
    # arc.check_product()
    # library(fluvgeo)
    # 
    # stream <- "Cole Creek R1"
    # xs_number <- 40
    # xs_points_1 <- "D:\\Workspace\\EMRRP_Sediment\\PapillionCreek_NE\\Reaches\\02_Cole_Creek\\y2004_R1.gdb\\xs_50_points"
    # xs_points_2 <- "D:\\Workspace\\EMRRP_Sediment\\PapillionCreek_NE\\Reaches\\02_Cole_Creek\\y2010_R1.gdb\\xs_50_points"
    # xs_points_3 <- "D:\\Workspace\\EMRRP_Sediment\\PapillionCreek_NE\\Reaches\\02_Cole_Creek\\y2016_R1.gdb\\xs_50_points"
    # xs_points_4 <- NULL
    # survey_name_1 <- "2004"
    # survey_name_2 <- "2010"
    # survey_name_3 <- "2016"
    # survey_name_4 <- NULL

    # Create list of survey paths
    print("Assembling survey events")
    xs_points_paths <- list(xs_points_1, xs_points_2, xs_points_3, xs_points_4)
    #xs_points_paths <- dplyr::na_if(xs_points_paths, "")
    
    # Name the survey paths list by their survey names
    survey_names <- c(survey_name_1, survey_name_2, survey_name_3, survey_name_4)
    #survey_names <- dplyr::na_if(survey_names, "")
    xs_points_paths <- setNames(xs_points_paths, survey_names)
    print(xs_points_paths)
    
    # Eliminate empty surveys
    print("Discarding empty items")
    xs_points_paths <- purrr::discard(xs_points_paths, is.null)
    
    # Convert list of survey paths to list of sp objects
    print("Converting to sp")
    xs_pts_sp <- purrr::map(xs_points_paths, fluvgeo::arc2sp)
    
    # Call the graph function
    print("Calling plot")
    print(fluvgeo::xs_compare_plot(stream = stream,
                                   xs_number = xs_number,
                                   xs_pts_list = xs_pts_sp))
    
    return(out_params)
}