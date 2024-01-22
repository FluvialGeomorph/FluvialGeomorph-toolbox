#' @title Cross Section Plot
#' 
#' @description Produces a plot for the specified cross section at the 
#'     specified detrended elevation.
#'     
#' @export
#' @param xs_points_fc        character; an ESRI cross section points feature 
#'                            class
#' @param xs_number           integer; The cross section identifier of the
#'                            requested cross section.
#' @param bankfull_elevation  numeric; The bankfull elevation (in feet) that is
#'                            used to calculate hydraulic geometry.
#' 
#' @return A ggplot object
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("report/_XSPlot.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("sp", "ggplot2", "fluvgeo"))
    
    # gp tool parameters
    xs_points_fc       <- in_params[[1]]
    xs_number          <- as.numeric(in_params[[2]])
    bankfull_elevation <- as.numeric(in_params[[3]])
    
    # Import fc to sp
    xs_points <- fluvgeo::arc2sp(xs_points_fc)
    
    # Determine the stream names
    stream <- unique(xs_points$ReachName)
    
    # Convert to a data frame
    xs_pts <- xs_points@data
    
    # Call xs_plot function
    print(fluvgeo::xs_plot(xs_points = xs_pts, 
                           stream = stream, 
                           xs_number = xs_number, 
                           bankfull_elevation = bankfull_elevation))
    
    return(out_params)
}
