#' @title Level 3 Report
#' 
#' @description  Creates the FluvialGeomorph Level 3 report.
#'
#' @export
#' @param stream             character; The stream name. The stream name must
#'                           match a stream name in `ReachName` field in the
#'                           other parameters.
#' @param flowline_fc        character; The path to a `flowline` feature class.
#' @param xs_fc              character; The path to the cross section feature
#'                           class.
#' @param xs_dims_fc         character; The path to a "*_dims_L3" feature class.
#' @param xs_points_1        character; The path to a `xs_points` feature
#'                           class for the "base year".
#' @param xs_points_2        character; The path to a `xs_points` feature
#'                           class for the second time period.
#' @param xs_points_3        character; The path to a `xs_points` feature
#'                           class for the third time period.
#' @param xs_points_4        character; The path to a `xs_points` feature
#'                           class for the fourth time period.
#' @param survey_name_1      character: The name or date of the "base year"
#'                           survey.
#' @param survey_name_2      character: The name or date of the second survey.
#' @param survey_name_3      character: The name or date of the third survey.
#' @param survey_name_4      character: The name or date of the fourth survey.
#' @param dem                character; The path to the DEM raster.
#' @param banklines_fc       character: The path to the banklines feature class.
#' @param features_fc        character; The path to a `features` feature class.
#' @param bf_estimate        numeric; Detrended bankfull estimate (units:
#'                           detrended feet).
#' @param regions            character vector; Regions to calculate hydraulic
#'                           dimensions for. See the `RegionalCurve` package for
#'                           a list of regions.
#' @param label_xs           logical; Label cross sections?
#' @param show_xs_map        logical; Add the cross section maps to the report?
#' @param profile_units      character; The units of the longitudinal profile.
#'                           One of "kilometers", "meters", "miles", or "feet".
#' @param aerial             logical; Display an overview map with an aerial
#'                           photo background?
#' @param elevation          logical; Display an overview map with an elevation
#'                           background?
#' @param xs_label_freq      numeric; An integer indicating the frequency of
#'                           cross section labels.
#' @param exaggeration       numeric; The degree of terrain exaggeration.
#' @param extent_factor      numeric; The amount the extent is expanded around
#'                           the cross section feature class. Values greater
#'                           than one zoom out, values less than one zoom in.
#' @param output_dir         character; The path to the folder in which to
#'                           write the report.
#' @param output_format      character; The file format of the report. One of
#'                           "html_document", "word_document", "pdf_document".
#'
#' @return Produces a FluvialGeomorph Level 2 Report in the `output_dir` in the
#' requested file format.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("report/_Level_3_Report.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("sp", "sf", "tmap","terra","maptiles","terrainr", 
                    "rmarkdown", "ggplot2", "tibble", "fluvgeo"))
    
    # Ensure pandoc can be found
    message("Setting pandoc directory...")
    set_pandoc()
    
    # gp tool parameters
    stream             <- in_params[[1]]
    flowline_fc        <- in_params[[2]]
    xs_fc              <- in_params[[3]]
    xs_dims_fc         <- in_params[[4]]
    xs_points_1        <- in_params[[5]]
    xs_points_2        <- in_params[[6]]
    xs_points_3        <- in_params[[7]]
    xs_points_4        <- in_params[[8]]
    survey_name_1      <- in_params[[9]]
    survey_name_2      <- in_params[[10]]
    survey_name_3      <- in_params[[11]]
    survey_name_4      <- in_params[[12]]
    dem                <- in_params[[13]]
    banklines_fc       <- in_params[[14]]
    features_fc        <- in_params[[15]]
    bf_estimate        <- in_params[[16]]
    regions            <- c(in_params[[17]], recursive = TRUE)
    label_xs           <- in_params[[18]]
    show_xs_map        <- in_params[[19]]
    profile_units      <- in_params[[20]]
    aerial             <- in_params[[21]]
    elevation          <- in_params[[22]]
    xs_label_freq      <- in_params[[23]]
    exaggeration       <- in_params[[24]]
    extent_factor      <- in_params[[25]]
    output_dir         <- in_params[[26]]
    output_format      <- in_params[[27]]
    
    # Code for testing in RStudio
    # library(fluvgeo)
    # library(sp)
    # library(sf)
    # library(tibble)
    # library(dplyr)
    # library(arcgisbinding)
    # arc.check_product()
    # 
    # stream        <- "Cole Creek R3"
    # flowline_fc   <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Data/y2016_R3.gdb/flowline"
    # xs_fc         <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Data/y2016_R3.gdb/xs_50"
    # xs_dims_fc    <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Data/y2016_R3.gdb/xs_50_dims_L3"
    # xs_points_1   <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Data/y2016_R3.gdb/xs_50_points"
    # xs_points_2   <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Data/y2010_R3.gdb/xs_50_points"
    # xs_points_3   <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Data/y2004_R3.gdb/xs_50_points"
    # xs_points_4   <- NULL
    # survey_name_1 <- "2016"
    # survey_name_2 <- "2010"
    # survey_name_3 <- "2006"
    # survey_name_4 <- NULL
    # dem           <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Data/y2016_R3.gdb/dem_2016_hydro"
    # banklines_fc  <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Data/y2016_R3.gdb/banklines"
    # features_fc   <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Data/y2016_R3.gdb/features"
    # bf_estimate   <- 106
    # regions       <- c("USA")
    # label_xs      <- TRUE
    # show_xs_map   <- FALSE
    # profile_units <- "feet"
    # aerial        <- TRUE
    # elevation     <- TRUE
    # xs_label_freq <- 10
    # exaggeration  <- 10
    # extent_factor <- 1.3
    # output_dir    <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Reaches/02_Cole_Creek/Reports"
    # output_format <- "word_document"
    
    # Verify parameters
    ## Create list of parameters (named using the parameter names)
    param_list <- tibble::lst(stream, flowline_fc, xs_fc, xs_dims_fc,
                              xs_points_1, xs_points_2,
                              xs_points_3, xs_points_4,
                              survey_name_1, survey_name_2,
                              survey_name_3, survey_name_4,
                              dem, banklines_fc, features_fc, 
                              bf_estimate, regions, label_xs, 
                              show_xs_map, profile_units,
                              aerial, elevation, 
                              xs_label_freq, exaggeration, extent_factor,
                              output_dir, output_format)
    
    ## Get parameter verification table
    message("Compare input tool parameters")
    param_table <- compare_params(in_params, param_list)
    print(tibble::as_tibble(param_table), n = 27)
    
    # Render the report
    fluvgeo::level_3_report(stream, flowline_fc, xs_fc, xs_dims_fc,
                            xs_points_1, xs_points_2,
                            xs_points_3, xs_points_4,
                            survey_name_1, survey_name_2,
                            survey_name_3, survey_name_4,
                            dem, banklines_fc, features_fc, 
                            bf_estimate, regions, label_xs, 
                            show_xs_map, profile_units,
                            aerial, elevation, 
                            xs_label_freq, exaggeration, extent_factor,
                            output_dir, output_format)
    
    return(out_params)
}
