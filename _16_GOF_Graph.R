tool_exec <- function(in_params, out_params) {
  # Produces a goodness of fit graph for the current reach by analysis
  # regions.
  # Args:
  #    xs_points_fc        character; an ESRI cross section points feature 
  #                        class
  #    regions:            character vector; The regions that dimensions
  #                        will be calculated for. See the
  #                        regional_curves$region field for a complete list.
  #    bankfull_elevation  numeric; The detrended bankfull elevation (in feet)
  #                        that is used to calculate hydraulic geometry.
  #    from_elevation      numeric; The detrended elevation (in feet) to begin
  #                        calculating Goodness of Fit (GOF) measures. 
  #    to_elevation        numeric; The detrended elevation (in feet) to end
  #                        calculating Goodness of Fit (GOF) measures.
  #    by_elevation        numeric; The detrended elevation (in feet) to step 
  #                        by for calculating Goodness of Fit (GOF) measures
  #
  # Returns:
  #    a ggplot object
  #
  # Load required libraries
  if (!require("pacman")) install.packages("pacman")
  pacman::p_load(dplyr, tibble, tidyr, Metrics, ggplot2, sp)

  # Source hydraulic geometry functions
  source("//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Methods/FluvialGeomorphr/HydraulicGeometry2.R")

  # gp tool parameters
  xs_points_fc        <- in_params[[1]]
  regions             <- c(in_params[[2]])
  bankfull_elevation  <- in_params[[3]]
  from_elevation      <- in_params[[4]]
  to_elevation        <- in_params[[5]]
  by_elevation        <- in_params[[6]]

  # Import fc to sp
  xs_points <- arc2sp(xs_points_fc)
  
  # Determine the stream name
  stream <- unique(xs_points$ReachName)

  # Bankfull elevations to examine for sensitivity analysis
  bankfull_elevations <- seq(from = from_elevation,
                             to = to_elevation,
                             by = by_elevation)

  # Calculate cross section dimensions
  xs_dims <- xs_Dimensions(xs_points, stream, regions, bankfull_elevations)
  # Calculate GOF statistics for all `streams`, `regions` and `bankfull_elevations`
  gof_stats <- Build_GOF_Stats(xs_dims, stream, regions, bankfull_elevations)
  # Gather the goodness of fit statistics into key-value fields (convert wide to long format) for graphing
  gof_stats_gather <- gather(data = gof_stats,
                             key = stats, value = measure,
                             XS_Area_rmse, XS_Width_rmse, XS_Depth_rmse,XS_Area_mae,XS_Width_mae,XS_Depth_mae)

  # Call the gof_graph plot function
  print(gof_graph(gof_stats_gather, stream, bankfull_elevation, "MAE"))

  return(out_params)
}
