tool_exec <- function(in_params, out_params) {
    # Calculates cross section hydraulic geometry dimensions for the input 
    # cross section feature class. 
    # Args:
    #    xs_fc               character; the full path to an ESRI cross section 
    #                        line feature class
    #    xs_points_fc        character; the full path to an ESRI cross section 
    #                        points feature class
    #    bankfull_elevation  numeric; The bankfull elevation (in feet) that is
    #                        used to calculate hydraulic geometry.
    #
    # Returns:
    #    a new cross section feature class with the hydraulic geometry 
    #    dimensions added to the attribute table
    #
    # Load required libraries
    if (!require("pacman")) install.packages("pacman")
    pacman::p_load(sp, dplyr)
    
    # Source hydraulic geometry functions
    source("//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorphr/HydraulicGeometry2.R")
    
    # gp tool parameters
    xs_fc              <- in_params[[1]]
    xs_points_fc       <- in_params[[2]]
    bankfull_elevation <- as.numeric(in_params[[3]])
    
    # Code for testing
    #library(arcgisbinding)
    #arc.check_product()
    #xs_fc              <- "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/XS_50_test"
    #xs_points_fc       <- "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/XS_50_test_points"
    #bankfull_elevation <- 103
    
    # Import fc to sp
    xs        <- arc2sp(xs_fc)
    xs_points <- arc2sp(xs_points_fc)
    
    # Create a list to hold the xs dimensions
    xs_geoms <- list()
    
    # Iterate through xs's and calculate dimensions
    for (i in xs$Seq) {
        stream <- unique(xs_points$ReachName)
        dims <- xs_GeometryTable(xs_points = xs_points, 
                                 stream = stream, 
                                 xs_number = i, 
                                 bankfull_elevation = bankfull_elevation)
        xs_geoms[[i]] <- dims
    }
    
    # Append the list of xs dimensions into a singe data frame
    reach_geoms <- dplyr::bind_rows(xs_geoms)
    
    # Join the reach_geoms to xs_fc
    xs_dims <- sp::merge(xs, reach_geoms, by.x = "Seq", by.y = "Cross_Section")
    
    # Write the xs_fc with hydraulic dimensions
    xs_dims_path <- paste0(xs_fc, "_dims") 
    sp2arc(sp_obj = xs_dims, fc_path = xs_dims_path)
    
    return(out_params)
}
