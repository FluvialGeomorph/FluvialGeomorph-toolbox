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
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr", "raster", "fluvgeo"))

    # gp tool parameters
    flowline_points_fc  <- in_params[[1]]
    gradient_distance   <- as.numeric(in_params[[2]])
    use_smoothing       <- as.logical(in_params[[3]])
    loess_span          <- as.numeric(in_params[[4]])
    
    # temp variables for development within R
    # library(arcgisbinding)
    # arc.check_product()
    # library(raster)
    # flowline_points_fc <- "D:/Workspace/EMRRP_Sediment/09_LittleSenachwineCreek/LittleSenachwineCreek.gdb/flowline_points"
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

    # Import fc to sp
    flowline_points <- fluvgeo::arc2sp(flowline_points_fc)
    
    # Calculate slope and sinuosity
    message("Calculating slope and sinuosity...")
    fl_pts <- fluvgeo::slope_sinuosity(channel_features = flowline_points, 
                                       lead_n = gradient_distance,
                                       lag_n = gradient_distance,
                                       use_smoothing = use_smoothing,
                                       loess_span = loess_span,
                                       vert_units = "ft")
    
    # Join slope attributes back to sp object
    message("Joining slope-sinuosity attributes...")
    gradient <- sp::merge(x = flowline_points, 
                          y = fl_pts[,c("OBJECTID","z_smooth", 
                                        "upstream_x","upstream_y", 
                                        "downstream_x","downstream_y",
                                        "upstream_z","downstream_z",
                                        "upstream_m","downstream_m", 
                                        "rise","run",
                                        "stream_length","valley_length",
                                        "sinuosity", "sinuosity_gte_one",
                                        "slope", "slope_gte_zero")], 
                          by.x = "OBJECTID", by.y = "OBJECTID")
    
    # Write the hydraulic dimensions to a file geodatabase table
    table_name <- paste0("gradient_", 
                         as.character(gradient_distance))
    gdb_path   <- dirname(dirname(xs_fc))
    table_path <- file.path(gdb_path, table_name)
    fluvgeo::sx2arc_table(sx_obj = gradient, table_path = table_path)
    message("saving table complete")
    
    return(out_params)
}
