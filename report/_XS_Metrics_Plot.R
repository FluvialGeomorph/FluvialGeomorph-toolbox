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
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "ggplot2", "ggrepel"))
    # Load FluvialGeomorph R packages
    load_fluvgeo_packages()
    
    # gp tool parameters
    xs_dimensions_fc    <- in_params[[1]]
    features_fc         <- in_params[[2]]
    label_xs            <- as.logical(in_params[[3]])
    
    # Import fc to sp
    xs_dimensions <- arc2sp(xs_dimensions_fc)
    features_sp <- arc2sp(features_fc)

    # Convert to a data frame
    xs_dims <- xs_dimensions@data

    # Call xs_plot function
    print(xs_metrics_plot(reach_xs_dims = xs_dims, 
                          features_sp = features_sp,
                          label_xs = label_xs))
    
    return(out_params)
}