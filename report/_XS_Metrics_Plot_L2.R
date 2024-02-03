#' @title Plot Level 2 Cross Section Metrics
#'
#' @description Produces a longitudinal plot of Level 2 cross section metrics 
#' for the input stream reach.
#'
#' @export
#' @param xs_dims_fc      character; A Level 2 cross section dimensions feature
#'                        class. 
#' @param features_fc     character; An infrastructure features feature class.
#' @param label_xs        logical; Draw the cross section locations?
#' @param xs_label_freq   numeric; An integer indicating the frequency of
#'                        cross section labels.
#' @param profile_units   character; the units of the longitudinal profile.
#'                        One of "kilometers", "meters", "miles", or "feet"
#'
#' @return A ggplot2 object.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("report/_XS_Metrics_Plot_L1.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("ggplot2", "ggrepel", "fluvgeo"))

    # gp tool parameters
    xs_dims_fc    <- in_params[[1]]
    features_fc   <- in_params[[2]]
    label_xs      <- as.logical(in_params[[3]])
    xs_label_freq <- as.numeric(in_params[[4]])
    profile_units <- in_params[[5]]
    
    # Import fc to sf
    xs_dims_sf  <- fluvgeo::fc2sf(xs_dims_fc)
    features_sf <- fluvgeo::fc2sf(features_fc)

    # Call xs metrics plot function
    print(fluvgeo::xs_metrics_plot_L2(xs_dims_sf = xs_dims_sf, 
                                      features_sf = features_sf,
                                      label_xs = label_xs,
                                      xs_label_freq = xs_label_freq,
                                      profile_units = profile_units))
    
    return(out_params)
}