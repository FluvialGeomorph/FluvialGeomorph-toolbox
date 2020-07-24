#' @title Reach geometry graph
#' 
#' @description Produces a hydraulic geometry graph for all of the cross 
#'     sections in the current reach.
#' 
#' @export
#' @param xs_points_fc        character; an ESRI cross section points feature 
#'                            class
#' @param regions:            character vector; The regions that dimensions
#'                            will be calculated for. See the
#'                            fluvgeo::regional_curves$region field for a complete 
#'                            list.
#' @param bankfull_elevation  numeric; The detrended bankfull elevation (in 
#'                            feet) that is used to calculate hydraulic 
#'                            geometry.
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
  load_packages(c("sp", "dplyr", "tibble", "tidyr", "ggplot2", "ggrepel", 
                  "fluvgeo"))

  # gp tool parameters
  xs_points_fc        <- in_params[[1]]
  regions             <- c(in_params[[2]], recursive = TRUE)
  bankfull_elevation  <- in_params[[3]]
  
  # Import fc to sp
  xs_points <- arc2sp(xs_points_fc)

  # Determine the stream names
  streams <- unique(xs_points$ReachName)
  
  # Convert xs_points to a data frame
  xs_pts <- xs_points@data
  
  # Calculate cross section dimensions
  xs_dims <- xs_dimensions(xs_points = xs_pts, 
                           streams = streams, 
                           regions = regions, 
                           bankfull_elevation = bankfull_elevation)

  # Call the gof_graph plot function
  print(reach_rhg_graph(xs_dims = xs_dims, 
                        streams = streams, 
                        bf_elevation = bankfull_elevation))
  
  return(out_params)
}
