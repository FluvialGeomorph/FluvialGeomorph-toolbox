#' @title Estimate Bankfull Report
#' 
#' @description Produces the FluvialGeomorph Bankfull Estimate report.
#' 
#' @export
#' @param stream              character; The stream name. The stream name must
#'                            match a stream name in `ReachName` field in the
#'                            other parameters.
#' @param flowline_fc         character; The path to the `flowline` feature
#'                            class.
#' @param xs_dims_fc          character; The path to the "xs_dims" feature
#'                            class. This is for the "base year" survey.
#' @param xs_points_1         character; The path to a `xs_points` feature
#'                            class for the "base year".
#' @param xs_points_2         character; The path to a `xs_points` feature
#'                            class for the second time period.
#' @param xs_points_3         character; The path to a `xs_points` feature
#'                            class for the third time period.
#' @param xs_points_4         character; The path to a `xs_points` feature
#'                            class for the fourth time period.
#' @param survey_name_1       character: The name or date of the "base year"
#'                            survey.
#' @param survey_name_2       character: The name or date of the second survey.
#' @param survey_name_3       character: The name or date of the third survey.
#' @param survey_name_4       character: The name or date of the fourth survey.
#' @param features_fc         character; The path to a `features` feature class.
#' @param dem                 character; The path to the DEM raster.
#' @param show_xs_map         logical; Add the cross section maps to the report?
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
#' @param label_xs            logical; Label cross sections?
#' @param profile_units       character; The units of the longitudinal profile.
#'                            One of "kilometers", "meters", "miles", or "feet"
#' @param aerial              logical; Display an overview map with an aerial
#'                            photo background?
#' @param elevation           logical; Display an overview map with an elevation
#'                            background?
#' @param xs_label_freq       numeric; An integer indicating the frequency of
#'                            cross section labels.
#' @param exaggeration        numeric; The degree of terrain exaggeration.
#' @param extent_factor       numeric; The amount the extent is expanded around
#'                            the cross section feature class. Values greater
#'                            than one zoom out, values less than one zoom in.
#' @param output_dir          character; The output directory for the report.
#' @param output_format       character; The output format of the report. One
#'                            of "html_document", "word_document",
#'                            "pdf_document".
#'
#' @return A report written to the file system in the output format requested.
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("tibble", "purrr", "rmarkdown", 
                    "sf", "sp", "raster", "rgdal", "tmap", 
                    "ggplot2", "ceramic", "fluvgeo"))
    
    # Ensure pandoc can be found
    message("Setting pandoc directory...")
    set_pandoc()
    
    # gp tool parameters
    stream              <- in_params[[1]]
    flowline_fc         <- in_params[[2]]
    xs_dims_fc          <- in_params[[3]]
    xs_points_1         <- in_params[[4]]
    xs_points_2         <- in_params[[5]]
    xs_points_3         <- in_params[[6]]
    xs_points_4         <- in_params[[7]]
    survey_name_1       <- in_params[[8]]
    survey_name_2       <- in_params[[9]]
    survey_name_3       <- in_params[[10]]
    survey_name_4       <- in_params[[11]]
    features_fc         <- in_params[[12]]
    dem                 <- in_params[[13]]
    show_xs_map         <- in_params[[14]]
    regions             <- c(in_params[[15]], recursive = TRUE)
    from_elevation      <- in_params[[16]]
    to_elevation        <- in_params[[17]]
    by_elevation        <- in_params[[18]]
    bf_estimate         <- in_params[[19]]
    stat                <- in_params[[20]]
    label_xs            <- in_params[[21]]
    profile_units       <- in_params[[22]]
    aerial              <- in_params[[23]]
    elevation           <- in_params[[24]]
    xs_label_freq       <- in_params[[25]]
    exaggeration        <- in_params[[26]]
    extent_factor       <- in_params[[27]]
    output_dir          <- in_params[[28]]
    output_format       <- in_params[[29]]
    
    # Verify parameters
    ## Create list of parameters (named using the parameter names)
    param_list <- tibble::lst(stream, flowline_fc, xs_dims_fc,
                              xs_points_1, xs_points_2,
                              xs_points_3, xs_points_4,
                              survey_name_1, survey_name_2,
                              survey_name_3, survey_name_4,
                              features_fc, dem, show_xs_map, regions, 
                              from_elevation, to_elevation, by_elevation, 
                              bf_estimate, stat, label_xs, profile_units,
                              aerial, elevation, xs_label_freq,
                              exaggeration, extent_factor,
                              output_dir, output_format)
    
    ## Get parameter verification table
    message("Compare input tool parameters")
    param_table <- compare_params(in_params, param_list)
    print(tibble::as_tibble(param_table), n = 29)
    
    # Bankfull elevations to examine for sensitivity analysis
    bankfull_elevations <- seq(from = from_elevation,
                               to = to_elevation,
                               by = by_elevation)
    
    # Call the estimate_bankfull function to create the report
    fluvgeo::estimate_bankfull(stream, flowline_fc, xs_dims_fc,
                               xs_points_1, xs_points_2,
                               xs_points_3, xs_points_4,
                               survey_name_1, survey_name_2,
                               survey_name_3, survey_name_4,
                               features_fc, dem, show_xs_map, 
                               regions, bankfull_elevations, bf_estimate,
                               stat, label_xs, profile_units,
                               aerial, elevation, xs_label_freq,
                               exaggeration, extent_factor,
                               output_dir, output_format)
    
    return(out_params)
}