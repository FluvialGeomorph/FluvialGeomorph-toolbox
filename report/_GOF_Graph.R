#' @title Reach bankfull goodness-of-fit graph
#' 
#' @description Produces a goodness of fit graph for the current reach for 
#'     each analysis region.
#'     
#' @export
#' @param xs_points_fc        character; an ESRI cross section points feature 
#'                            class
#' @param regions             character vector; The regions that dimensions
#'                            will be calculated for. See the
#'                            fluvgeo::regional_curves$region field for a complete 
#'                            list.
#' @param bankfull_elevation  numeric; The detrended bankfull elevation (in 
#'                            feet) that is used to calculate hydraulic 
#'                            geometry.
#' @param from_elevation      numeric; The detrended elevation (in feet) to 
#'                            begin calculating Goodness of Fit (GOF) measures.
#' @param to_elevation        numeric; The detrended elevation (in feet) to end
#'                            calculating Goodness of Fit (GOF) measures.
#' @param by_elevation        numeric; The detrended elevation (in feet) to 
#'                            step by for calculating Goodness of Fit (GOF) 
#'                            measures
#'
#' @return A ggplot object
#'
tool_exec <- function(in_params, out_params) {
  # Load utility R functions
  dir_name <- getSrcDirectory(function(x) {x})
  fg <- dirname(dir_name)
  fg_install <- file.path(fg, "install")
  source(file.path(fg_install, "FG_utils.R"))
  # Load required libraries
  load_packages(c("sp", "dplyr", "tibble", "tidyr", "Metrics", "ggplot2", 
                  "fluvgeo"))

  # gp tool parameters
  xs_points_fc        <- in_params[[1]]
  regions             <- c(in_params[[2]], recursive = TRUE)
  bankfull_elevation  <- in_params[[3]]
  from_elevation      <- in_params[[4]]
  to_elevation        <- in_params[[5]]
  by_elevation        <- in_params[[6]]

  # Import fc to sp
  xs_points <- arc2sp(xs_points_fc)
  
  # Determine the stream names
  streams <- unique(xs_points$ReachName)

  # Bankfull elevations to examine for sensitivity analysis
  bankfull_elevations <- seq(from = from_elevation,
                             to = to_elevation,
                             by = by_elevation)
  
  # Convert xs_points to a data frame
  xs_pts <- xs_points@data

  # Calculate cross section dimensions
  xs_dims <- xs_dimensions(xs_points = xs_pts, 
                           streams = streams, 
                           regions = regions, 
                           bankfull_elevation = bankfull_elevations)
  
  # Calculate GOF stats for all `streams`, `regions` and `bankfull_elevations`
  gof_stats <- build_gof_stats(xs_dims = xs_dims, 
                               streams = streams, 
                               regions = regions, 
                               bankfull_elevations = bankfull_elevations)
  
  # Call the gof_graph plot function
  print(gof_graph(gof_stats = gof_stats, 
                  stream = streams, 
                  bankfull_elevation = bankfull_elevation, 
                  stat = "MAE"))

  return(out_params)
}
