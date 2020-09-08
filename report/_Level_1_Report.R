#' @title Level 1 Report
#' 
#' @description  Creates a FluvialGeomorph level 1 report.
#'
#' @export
#'
#' @param stream             character; The stream name. The stream name must
#'                           match a stream name in `ReachName` field in the
#'                           other parameters.
#' @param flowline_fc        character; The path to a `flowline` feature class.
#' @param cross_section_fc   character; The path to a cross section feature
#'                           class.
#' @param flowline_points_1  character; The path to a `flowline_points` feature
#'                           class for the first time period.
#' @param flowline_points_2  character; The path to a `flowline_points` feature
#'                           class for the second time period.
#' @param flowline_points_3  character; The path to a `flowline_points` feature
#'                           class for the third time period.
#' @param flowline_points_4  character; The path to a `flowline_points` feature
#'                           class for the fourth time period.
#' @param xs_points_1        character; The path to a `xs_points` feature
#'                           class for the first time period.
#' @param xs_points_2        character; The path to a `xs_points` feature
#'                           class for the second time period.
#' @param xs_points_3        character; The path to a `xs_points` feature
#'                           class for the third time period.
#' @param xs_points_4        character; The path to a `xs_points` feature
#'                           class for the fourth time period.
#' @param survey_name_1      character: The name or date of the first survey.
#' @param survey_name_2      character: The name or date of the second survey.
#' @param survey_name_3      character: The name or date of the third survey.
#' @param survey_name_4      character: The name or date of the fourth survey.
#' @param features_fc        character; The path to a `features` feature class.
#' @param profile_units      character; The units to be used for the x-axis of
#'                           the longitudinal profile graphs. One of "feet",
#'                           "miles", "meters", "kilometers".
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
#' @param output_dir         character; The path to the folder in which to write
#'                           the report.
#' @param output_format      character; The file format of the report. One of
#'                           "html_document", "word_document", "pdf_document".
#'
#' @return Produces a FluvialGeomorph Level 1 Report in the `output_dir` in the
#' requested file format.
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("purrr", "rmarkdown", "ggplot2", "tibble", "ceramic",
                    "fluvgeo"))
    
    # Ensure pandoc can be found
    message("Setting pandoc directory...")
    set_pandoc()

    # gp tool parameters
    stream             <- in_params[[1]]
    flowline_fc        <- in_params[[2]]
    cross_section_fc   <- in_params[[3]]
    flowline_points_1  <- in_params[[4]]
    flowline_points_2  <- in_params[[5]]
    flowline_points_3  <- in_params[[6]]
    flowline_points_4  <- in_params[[7]]
    xs_points_1        <- in_params[[8]]
    xs_points_2        <- in_params[[9]]
    xs_points_3        <- in_params[[10]]
    xs_points_4        <- in_params[[11]]
    survey_name_1      <- in_params[[12]]
    survey_name_2      <- in_params[[13]]
    survey_name_3      <- in_params[[14]]
    survey_name_4      <- in_params[[15]]
    features_fc        <- in_params[[16]]
    profile_units      <- in_params[[17]]
    aerial             <- in_params[[18]]
    elevation          <- in_params[[19]]
    xs_label_freq      <- in_params[[20]]
    exaggeration       <- in_params[[21]]
    extent_factor      <- in_params[[22]]
    output_dir         <- in_params[[23]]
    output_format      <- in_params[[24]]
    
    # Verify parameters
    ## Create list of parameters (named using the parameter names)
    param_list <- tibble::lst(stream, flowline_fc, cross_section_fc,
                              flowline_points_1, flowline_points_2,
                              flowline_points_3, flowline_points_4,
                              xs_points_1, xs_points_2, 
                              xs_points_3, xs_points_4,
                              survey_name_1, survey_name_2,
                              survey_name_3, survey_name_4,
                              features_fc, profile_units,
                              aerial, elevation,
                              xs_label_freq, exaggeration,
                              extent_factor,
                              output_dir, output_format)
    
    ## Get parameter verification table
    message("Compare input tool parameters")
    param_table <- compare_params(in_params, param_list)
    print(tibble::as_tibble(param_table), n = 24)
    
    # Render the report
    fluvgeo::level_1_report(stream, flowline_fc, cross_section_fc,
                            flowline_points_1, flowline_points_2,
                            flowline_points_3, flowline_points_4,
                            xs_points_1, xs_points_2, xs_points_3, xs_points_4,
                            survey_name_1, survey_name_2,
                            survey_name_3, survey_name_4,
                            features_fc, profile_units,
                            aerial, elevation,
                            xs_label_freq, exaggeration,
                            extent_factor,
                            output_dir, output_format)
    
    return(out_params)
}
