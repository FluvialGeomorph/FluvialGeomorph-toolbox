#' @title Plot cross section metrics
#' 
#' @description Produces a longitudinal plot of cross section metrics for the
#' input stream reach.
#'     
#' @export
#' @param xs_dimensions_fc line feature class; a line feature class of cross 
#'                         section dimensions.
#' @param features_fc      point feature class; a point feature class of 
#'                         infrastructure locations.
#' @param label_xs         boolean; Draw the cross section labels?
#'
#' @return A ggplot2 object.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("report/_XS_Metrics_Plot.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("sp", "ggplot2", "ggrepel", "fluvgeo"))

    # gp tool parameters
    xs_dimensions_fc    <- in_params[[1]]
    features_fc         <- in_params[[2]]
    label_xs            <- as.logical(in_params[[3]])
    
    # Import fc to sp
    xs_dimensions <- fluvgeo::arc2sp(xs_dimensions_fc)
    features_sp   <- fluvgeo::arc2sp(features_fc)

    # Convert to a data frame
    xs_dims <- xs_dimensions@data

    # Call xs_plot function
    print(fluvgeo::xs_metrics_plot(reach_xs_dims = xs_dims, 
                                   features_sp = features_sp,
                                   label_xs = label_xs))
    
    return(out_params)
}