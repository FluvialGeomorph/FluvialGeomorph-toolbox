#' @title Level 2 Report
#' 
#' @description  Creates a FluvialGeomorph level 2 report.
#'
#' @export
#' @param stream             character; The stream name. The stream name must
#'                           match a stream name in `ReachName` field in the
#'                           other parameters.
#' @param flowline_fc        character; The path to a `flowline` feature class.
#' @param xs_fc              character; The path to the cross section feature
#'                           class.
#' @param xs_points_fc       character; The path to a `xs_points` feature
#'                           class.
#' @param xs_dims_fc         character; The path to the "xs_dims" feature class.
#' @param dem                character; The path to the DEM raster.
#' @param banklines_fc       character: The path to the banklines feature class.
#' @param features_fc        character; The path to a `features` feature class.
#' @param bf_estimate        numeric; Detrended bankfull estimate (units:
#'                           detrended feet).
#' @param regions            character vector; Regions to calculate hydraulic
#'                           dimensions for. See the `RegionalCurve` package for
#'                           a list of regions.
#' @param extent_factor      numeric; The extent factor used to control the
#'                           extent of cross section site maps.
#' @param label_xs           logical; Label cross sections?
#' @param show_xs_map        logical; Add the cross section maps to the report?
#' @param profile_units      character; The units of the longitudinal profile.
#'                           One of "kilometers", "meters", "miles", or "feet".
#' @param output_dir         character; The path to the folder in which to
#'                           write the report.
#' @param output_format      character; The file format of the report. One of
#'                           "html_document", "word_document", "pdf_document".
#'
#' @return Produces a FluvialGeomorph Level 2 Report in the `output_dir` in the
#' requested file format.
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "sf", "tmap", "rmarkdown", "ggplot2", "fluvgeo"))
    
    # Ensure pandoc can be found
    message("Setting pandoc directory...")
    set_pandoc()
    
    # gp tool parameters
    stream             <- in_params[[1]]
    flowline_fc        <- in_params[[2]]
    xs_fc              <- in_params[[3]]
    xs_points_fc       <- in_params[[4]]
    xs_dims_fc         <- in_params[[5]]
    dem                <- in_params[[6]]
    banklines_fc       <- in_params[[7]]
    features_fc        <- in_params[[8]]
    bf_estimate        <- in_params[[9]]
    regions            <- c(in_params[[10]], recursive = TRUE)
    extent_factor      <- in_params[[11]]
    label_xs           <- in_params[[12]]
    show_xs_map        <- in_params[[13]]
    profile_units      <- in_params[[14]]
    output_dir         <- in_params[[15]]
    output_format      <- in_params[[16]]
    
    # Render the report
    fluvgeo::level_2_report(stream, flowline_fc, xs_fc, xs_points_fc,
                            xs_dims_fc, dem, banklines_fc, features_fc,
                            bf_estimate, regions, extent_factor, label_xs,
                            show_xs_map,
                            profile_units, output_dir, output_format)
    
    return(out_params)
}
