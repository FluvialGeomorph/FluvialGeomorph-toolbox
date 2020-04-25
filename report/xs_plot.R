tool_exec <- function(in_params, out_params) {
    # Produces a plot for the specified cross section at the specified
    # detrended elevation.
    # Args:
    #    xs_points_fc        character; an ESRI cross section points feature 
    #                        class
    #    xs_number           integer; The cross section identifier of the
    #                        requested cross section.
    #
    # Returns:
    #    a ggplot object
    #
    # Load required libraries
    if (!require("pacman")) install.packages("pacman")
    pacman::p_load(ggplot2, sp)

    # Source hydraulic geometry functions
    source("//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorphr/HydraulicGeometry2.R")
    
    # gp tool parameters
    xs_points_fc       <- in_params[[1]]
    xs_number          <- as.numeric(in_params[[2]])

    # Import fc to sp
    xs_points <- arc2sp(xs_points_fc)
    
    # Subset xs_points for the specified stream and cross section
    xs <- xs_points[xs_points$LineID == xs_number,]
    
    # Create the graph
    p <- ggplot(data = as.data.frame(xs),
                aes(POINT_M * 3.28084, POINT_Z, label = LineID)) +
        geom_line() +
        theme_bw() +
        theme(aspect.ratio = 2/5) +
        labs(title = paste("Cross Section ", as.character(xs_number)),
             x = "Station Distance (feet, from left descending bank)",
             y = "Elevation (NAVD88 feet)") +
        theme(plot.title = element_text(hjust = 0)
        )
    
    # Print the graph
    print(p)
    
    return(out_params)
}
