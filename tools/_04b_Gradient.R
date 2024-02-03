#' @title Calculate Slope and Sinuosity
#' 
#' @description Calculates stream gradient (or slope) ans sinuosity for a 
#' `flowline_points` or `stream_network` feature class.
#'
#' @export
#' @param flowline_points_fc  character; the full path to a `flowline_points` 
#'                            feature class
#' @param gradient_distance   numeric; the number of features to lead (upstream)
#'                            and lag (downstream) to calculate the slope and 
#'                            sinuosity. Must be an integer.
#' @param use_smoothing       logical; determines if smoothed elevation values
#'                            are used to calculate gradient and sinuosity 
#'                            (default is FALSE). 
#' @param loess_span          numeric; the loess regression span parameter, 
#'                            defaults to 0.05
#'
#' @details Positive slope values represent elevations decreasing as one moves 
#'    downstream. Negative slope values represent elevations increasing as 
#'    one moves downstream (caused by error in the terrain data). 
#'
#' @return A new feature class called `gradient_<gradient_distance>` with new
#'    fields added describing slope and sinuosity. 
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("tools/_04b_Gradient.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("dplyr", "raster", "fluvgeo"))

    # gp tool parameters
    flowline_points_fc  <- in_params[[1]]
    gradient_distance   <- as.numeric(in_params[[2]])
    use_smoothing       <- as.logical(in_params[[3]])
    loess_span          <- as.numeric(in_params[[4]])
    
    # Code for testing in RStudio
    # library(raster)
    # flowline_points_fc <- "C:\\Workspace\\FluvialGeomorph\\fluvgeo\\inst\\extdata\\y2016_R1.gdb\\feature_dataset\\flowline_points"
    # gradient_distance  <- 1000
    # use_smoothing      <- TRUE
    # loess_span         <- 0.05

    # Set default values
    if(length(use_smoothing) < 1) {
        use_smoothing <- TRUE
    }
    if(length(loess_span) < 1) {
        loess_span <- 0.05
    }

    # Import fc to sf
    flowline_points_sf <- fluvgeo::fc2sf(flowline_points_fc)
    message("Conversion to sf complete")
    
    # Calculate slope and sinuosity
    fl_pts <- fluvgeo::slope_sinuosity(channel_features = flowline_points_sf, 
                                       lead_n = gradient_distance,
                                       lag_n = gradient_distance,
                                       use_smoothing = use_smoothing,
                                       loess_span = loess_span,
                                       vert_units = "ft")
    message("Calculated slope and sinuosity")
    
    # Write the hydraulic dimensions to a csv file
    # arcgisbinding::arc.write unable to reliably export sf to gdb
    table_name <- paste0(basename(flowline_points_fc), "_gradient.csv")
    gdb_folder_path <- dirname(dirname(dirname(flowline_points_fc)))
    csv_path <- file.path(gdb_folder_path, table_name)
    fluvgeo::sf2csv(sf_object = fl_pts, 
                    csv_path = csv_path)
    message("saving csv complete: ", csv_path)
    
    # Write the hydraulic dimensions to a file geodatabase table
    table_name <- paste0("gradient_", 
                         as.character(gradient_distance))
    gdb_path   <- dirname(dirname(xs_fc))
    table_path <- file.path(gdb_path, table_name)
    fluvgeo::sx2arc_table(sx_obj = gradient, table_path = table_path)
    message("saving table complete")
    
    return(out_params)
}
