tool_exec <- function(in_params, out_params) {
  # Produces a hydraulic geometry graph for all of the cross sections in 
  # the current reach.
  # Args:
  #    xs_points_fc        character; an ESRI cross section points feature 
  #                        class
  #    regions:            character vector; The regions that dimensions
  #                        will be calculated for. See the
  #                        regional_curves$region field for a complete list.
  #    bankfull_elevation  numeric; The detrended bankfull elevation (in feet)
  #                        that is used to calculate hydraulic geometry.
  #
  # Returns:
  #    a ggplot object
  #
  # Load required libraries
  if (!require("pacman")) install.packages("pacman")
  pacman::p_load(dplyr, tibble, tidyr, ggplot2, ggrepel, sp)

  # Source hydraulic geometry functions
  source("//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorphr/HydraulicGeometry2.R")
  
  # gp tool parameters
  xs_points_fc        <- in_params[[1]]
  regions             <- c(in_params[[2]])
  bankfull_elevation  <- in_params[[3]]

  # Import fc to sp
  xs_points <- arc2sp(xs_points_fc)

  # Determine the stream name
  stream <- unique(xs_points$ReachName)
  
  # Calculate cross section dimensions
  xs_dims <- xs_Dimensions(xs_points, stream, regions, bankfull_elevation)

  # Call the gof_graph plot function
  print(reach_RHG_graph(xs_dims, stream, bankfull_elevation))
  
  return(out_params)
}
