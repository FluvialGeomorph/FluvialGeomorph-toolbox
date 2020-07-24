#' @title Cross Section Metrics Report
#' 
#' @description Produces the cross section metrics report.
#' 
#' @export
#' @param xs_points_fc        point feature class; A cross section points 
#'                            feature class. 
#' @param xs_dims_planform_fc point feature class; A cross section planform 
#'                            dimensions feature class. 
#' @param dem                 character; path to a dem raster
#' @param banklines           SpatialLinesDataFrame; a banklines feature class
#' @param extent_factor       numeric; A numeric value used to expand the map
#'                            extent around each cross section
#' @param regions             character; The regions that a dimension will be
#'                            calculated for. See the regional_curves$region
#'                            field for a complete list.
#' @param features_fc         point feature class; A point feature class of 
#'                            river features
#' @param label_xs            boolean; Draw the cross section labels?
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
    source(file.path(dir_name, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr", "tibble", "tidyr", "Metrics", "ggplot2",
                    "ggrepel", "knitr", "rmarkdown", "kableExtra", "reshape2",
                    "assertthat", "fluvgeo"))
    # Set pandoc
    set_pandoc()
    
    # gp tool parameters
    xs_points_fc        <- in_params[[1]]
    xs_dims_planform_fc <- in_params[[2]]
    dem                 <- in_params[[3]]
    banklines_fc        <- in_params[[4]]
    extent_factor       <- in_params[[5]]
    regions             <- c(in_params[[6]], recursive = TRUE)
    features_fc         <- in_params[[7]]
    label_xs            <- as.logical(in_params[[8]])
    output_dir          <- in_params[[9]]
    output_format       <- in_params[[10]]
    
    # Import fc to sp
    xs_points_sp        <- arc2sp(xs_points_fc)
    xs_dims_planform_sp <- arc2sp(xs_dims_planform_fc)
    bankline_sp         <- arc2sp(banklines_fc)
    features_sp         <- arc2sp(features_fc)
    
    # Determine the stream names
    streams <- unique(xs_points$ReachName)
    
    # Convert sp objects to a data frame
    xs_points        <- xs_points_sp@data
    xs_dims_planform <- xs_dims_planform_sp@data
    features         <- features_sp@data
    
    # Call the estimate_bankfull function to create the report
    xs_metrics_report(xs_points = xs_points,
                      xs_dims_planform = xs_dims_planform,
                      dem = dem,
                      banklines = bankline_sp,
                      extent_factor = extent_factor,
                      streams = streams,
                      regions = regions,
                      features = features,
                      label_xs = label_xs,
                      output_dir = output_dir,
                      output_format = output_format)
    
    return(out_params)
}