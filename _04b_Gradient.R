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
    source("FG_utils.R")
    # Load required libraries
    load_packages(c("sp", "dplyr", "raster"))
    # Load FluvialGeomorph R packages
    load_fgm_packages()
    
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
    
    # Add new columns to hold calculated values
    flowline_pts$Z_smooth      <- 0
    flowline_pts$upstream_x    <- 0
    flowline_pts$upstream_y    <- 0
    flowline_pts$downstream_x  <- 0
    flowline_pts$downstream_y  <- 0
    flowline_pts$upstream_z    <- 0
    flowline_pts$downstream_z  <- 0
    flowline_pts$upstream_m    <- 0
    flowline_pts$downstream_m  <- 0
    flowline_pts$rise          <- 0
    flowline_pts$run           <- 0
    flowline_pts$stream_length <- 0
    flowline_pts$valley_length <- 0
    flowline_pts$sinuosity     <- 0
    flowline_pts$slope         <- 0
    
    # Sort by ReachName and POINT_M
    fl_pts <- flowline_pts[order(flowline_pts$ReachName, 
                                 flowline_pts$POINT_M),]
    
    # Iterate through reaches and calculate gradient and sinuosity
    reaches <- levels(as.factor(fl_pts$ReachName))
    for (r in reaches) {
        print(r)
        ## Calculate gradient-slope
        # Calculate a loess smoothed z
        l_z_5 <- loess(Z ~ POINT_M, 
                       data = fl_pts[fl_pts$ReachName == r,], 
                       span = loess_span)
        fl_pts[fl_pts$ReachName == r,]$Z_smooth <- predict(l_z_5)
    
        # Calculate average point spacing: mean(lead m - current m)
        point_spacing <- mean((lead(fl_pts[fl_pts$ReachName == r,]$POINT_M, 1) - 
                               fl_pts[fl_pts$ReachName == r,]$POINT_M) * 3280.84, 
                              na.rm = TRUE)
        # Convert gradient_distance to lead_lag vector position (because 
        # lead,lag use vector position)
        lead_lag <- as.integer((gradient_distance / point_spacing) / 2)
        
        # Calculate variable mins and maxs. Use as default to lead/lag to 
        # prevent NAs being introduced at ends of series.
        upstream_m_lead         <- max(fl_pts[fl_pts$ReachName == r,]$POINT_M)
        downstream_m_lag        <- min(fl_pts[fl_pts$ReachName == r,]$POINT_M)
        upstream_z_smooth_lead  <- max(fl_pts[fl_pts$ReachName == r,]$Z_smooth)
        downstream_z_smooth_lag <- min(fl_pts[fl_pts$ReachName == r,]$Z_smooth)
        upstream_z_lead         <- max(fl_pts[fl_pts$ReachName == r,]$Z)
        downstream_z_lag        <- min(fl_pts[fl_pts$ReachName == r,]$Z)
        
        # Calculate z values (already in feet)
        if (use_smoothing == TRUE) {
            fl_pts[fl_pts$ReachName == r,]$upstream_z   <- 
                          lead(x = fl_pts[fl_pts$ReachName == r,]$Z_smooth, 
                               n = lead_lag,
                               default = upstream_z_smooth_lead)
            fl_pts[fl_pts$ReachName == r,]$downstream_z <- 
                           lag(x = fl_pts[fl_pts$ReachName == r,]$Z_smooth, 
                               n = lead_lag,
                               default = downstream_z_smooth_lag)
        } 
        if (use_smoothing == FALSE) {
            fl_pts[fl_pts$ReachName == r,]$upstream_z   <- 
                          lead(x = fl_pts[fl_pts$ReachName == r,]$Z, 
                               n = lead_lag,
                               default = upstream_z_lead)
            fl_pts[fl_pts$ReachName == r,]$downstream_z <- 
                           lag(x = fl_pts[fl_pts$ReachName == r,]$Z, 
                               n = lead_lag,
                               default = downstream_z_lag)
        }

        # Calculate m values (and convert from kilometers to feet: 1 km = 
        # 3280.84 ft)
        fl_pts[fl_pts$ReachName == r,]$upstream_m   <- 
                          lead(x = fl_pts[fl_pts$ReachName == r,]$POINT_M, 
                               n = lead_lag, 
                               default = upstream_m_lead) * 3280.48
        fl_pts[fl_pts$ReachName == r,]$downstream_m <- 
                           lag(x = fl_pts[fl_pts$ReachName == r,]$POINT_M, 
                               n = lead_lag, 
                               default = downstream_m_lag) * 3280.48
        
        # Calculate rise and run (in feet)
        fl_pts[fl_pts$ReachName == r,]$rise <- 
                          fl_pts[fl_pts$ReachName == r,]$upstream_z - 
                          fl_pts[fl_pts$ReachName == r,]$downstream_z
        fl_pts[fl_pts$ReachName == r,]$run  <- 
                          fl_pts[fl_pts$ReachName == r,]$upstream_m - 
                          fl_pts[fl_pts$ReachName == r,]$downstream_m
    
        # Calculate slope: (rise / run)
        fl_pts[fl_pts$ReachName == r,]$slope <- 
                          fl_pts[fl_pts$ReachName == r,]$rise / 
                          fl_pts[fl_pts$ReachName == r,]$run
        
        ## Calculate sinuosity
        # Calculate coords of first and last record. Use as default to lead/lag 
        # to prevent NAs being introduced at ends of series.
        upstream_x_lead  <- last(fl_pts[fl_pts$ReachName == r,]$POINT_X)
        downstream_x_lag <- first(fl_pts[fl_pts$ReachName == r,]$POINT_X)
        upstream_y_lead  <- last(fl_pts[fl_pts$ReachName == r,]$POINT_Y)
        downstream_y_lag <- first(fl_pts[fl_pts$ReachName == r,]$POINT_Y)
        
        # Calculate x values
        fl_pts[fl_pts$ReachName == r,]$upstream_x   <- 
                          lead(x = fl_pts[fl_pts$ReachName == r,]$POINT_X,
                               n = lead_lag,
                               default = upstream_x_lead)
        fl_pts[fl_pts$ReachName == r,]$downstream_x   <- 
                           lag(x = fl_pts[fl_pts$ReachName == r,]$POINT_X,
                               n = lead_lag,
                               default = downstream_x_lag)
        
        # Calculate y values
        fl_pts[fl_pts$ReachName == r,]$upstream_y   <- 
                          lead(x = fl_pts[fl_pts$ReachName == r,]$POINT_Y,
                               n = lead_lag,
                               default = upstream_y_lead)
        fl_pts[fl_pts$ReachName == r,]$downstream_y <- 
                           lag(x = fl_pts[fl_pts$ReachName == r,]$POINT_Y,
                               n = lead_lag,
                               default = downstream_y_lag)
        
        # Calculate stream_length (in feet)
        fl_pts[fl_pts$ReachName == r,]$stream_length <- 
                          fl_pts[fl_pts$ReachName == r,]$upstream_m - 
                          fl_pts[fl_pts$ReachName == r,]$downstream_m
        
        # Calculate valley_length (convert from meters to feet)
        fl_pts[fl_pts$ReachName == r,]$valley_length <- 
          pointDistance(p1 = cbind(fl_pts[fl_pts$ReachName == r,]$upstream_x,
                                   fl_pts[fl_pts$ReachName == r,]$upstream_y),
                        p2 = cbind(fl_pts[fl_pts$ReachName == r,]$downstream_x, 
                                   fl_pts[fl_pts$ReachName == r,]$downstream_y),
                        lonlat = FALSE) * 3.28084
        
        # Calculate sinuosity stream_length / valley_length
        fl_pts[fl_pts$ReachName == r,]$sinuosity <- 
                        fl_pts[fl_pts$ReachName == r,]$stream_length / 
                        fl_pts[fl_pts$ReachName == r,]$valley_length
    }
    
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
