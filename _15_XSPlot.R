tool_exec <- function(in_params, out_params) {
  # Produces a plot for the specified cross section at the specified
  # detrended elevation.
  # Args:
  #    xs_points_fc        character; an ESRI cross section points feature 
  #                        class
  #    xs_number           integer; The cross section identifier of the
  #                        requested cross section.
  #    bankfull_elevation  numeric; The bankfull elevation (in feet) that is
  #                        used to calculate hydraulic geometry.
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
  bankfull_elevation <- as.numeric(in_params[[3]])

  # Import fc to sp
  xs_points <- arc2sp(xs_points_fc)
  
  # Determine the stream name
  stream <- unique(xs_points$ReachName)

  # Call xs_plot function
  print(xs_plot(xs_points, stream, xs_number, bankfull_elevation))

  return(out_params)
}
