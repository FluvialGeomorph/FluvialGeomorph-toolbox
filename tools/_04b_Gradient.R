#' Calculates stream gradient (or slope) for a flowline_points feature
#' class.
#'
#' Args:
#'    flowline_points_fc: character; the full path to an ESRI flowline 
#'                        points feature class
#'    gradient_distance:  numeric; the window size (in feet) around each 
#'                        point that will be used to calculate the stream 
#'                        gradient
#'    use_smoothing:      boolean; determines if smoothed elevation values
#'                        are used to calculate gradient. values are: 
#'                        TRUE, FALSE (default)
#'    loess_span:         numeric; the loess regression span parameter, 
#'                        defaults to 0.05
#'
#' Usage:
#'    Positive slope values represent elevations decreasing as one moves 
#'    downstream. Negative slope values represent elevations increasing as 
#'    one moves downstream (caused by error in the terrain data). 
#'
#' Returns:
#'    A new flowline_points feature class called 'gradient' with the new
#'    fields 'slope', `sinuosity`. 
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr", "raster", "fluvgeo"))

    # gp tool parameters
    flowline_points_fc  <- in_params[[1]]
    gradient_distance   <- as.numeric(in_params[[2]])
    use_smoothing       <- as.logical(in_params[[3]])
    loess_span          <- as.numeric(in_params[[4]])
    
    # temp variables for development within R
    #library(arcgisbinding)
    #arc.check_product()
    #library(raster)
    #flowline_points_fc <- "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/flowline_points"
    #gradient_distance  <- 1000
    #use_smoothing      <- TRUE
    #loess_span         <- 0.05
    
    # Set default values
    if(length(use_smoothing) < 1) {
        use_smoothing <- TRUE
    }
    if(length(loess_span) < 1) {
        loess_span <- 0.05
    }

    # Import fc to sp
    flowline_points <- arc2sp(flowline_points_fc)
    
    # Convert to data frame
    flowline_pts <- data.frame(flowline_points@data)
    
    # Call the fluvgeo::slope_sinuosity function
    fl_pts <- slope_sinuosity(channel_features = flowline_pts, 
                              lead_lag = gradient_distance,
                              use_smoothing = use_smoothing,
                              loess_span = loess_span)
    
    # Join slope attributes back to sp object
    gradient <- sp::merge(x = flowline_points, 
                          y = fl_pts[,c("OBJECTID","Z_smooth", 
                                        "upstream_x","upstream_y", 
                                        "downstream_x","downstream_y",
                                        "upstream_z","downstream_z",
                                        "upstream_m","downstream_m","rise","run",
                                        "stream_length","valley_length",
                                        "sinuosity","slope")], 
                          by.x = "OBJECTID", by.y = "OBJECTID")
    
    # Convert sp object back to new feature class
    gradient_path <- paste0(dirname(flowline_points_fc), "/", "gradient_", 
                            as.character(gradient_distance))
    sp2arc(sp_obj = gradient, fc_path = gradient_path)
    
    return(out_params)
}
