#' @title Plot cross section metrics
#' 
#' @description Produces a longitudinal plot of cross section metrics for the
#' input stream reach.
#'     
#' @export
#' @param xs_dimensions_fc line feature class; a line feature class of cross 
#'                         section dimensions.
#' @param label_xs         boolean; Draw the cross section locations?
#'
#' @return A ggplot2 object.
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "ggplot2", "ggrepel"))
    # Load FluvialGeomorph R packages
    load_fluvgeo_packages()
    
    # gp tool parameters
    xs_dimensions_fc    <- in_params[[1]]
    label_xs            <- as.logical(in_params[[2]])
    
    # Import fc to sp
    xs_dimensions <- arc2sp(xs_dimensions_fc)

    # Convert to a data frame
    xs_dims <- xs_dimensions@data

    # Call xs_plot function
    print(xs_metrics_plot(reach_xs_dims = xs_dims, 
                          label_xs = label_xs))
    
    return(out_params)
}