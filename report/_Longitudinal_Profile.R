#' @title Longitudinal Profile Plot
#' 
#' @description Produces a longitudinal profile plot for the cross sections
#' of the input stream reach.
#'     
#' @export
#' @param xs_dimensions_fc line feature class; a line feature class of cross 
#'                         section dimensions.
#' @param features_fc      point feature class; a point feature class of river 
#'                         features
#' @param label_xs         boolean; Draw the cross section locations?
#' 
#' @return A ggplot object
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("report/_Longitudinal_Profile.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("sp", "ggplot2", "ggrepel", "fluvgeo"))
    
    # Ensure pandoc can be found
    message("Setting pandoc directory...")
    set_pandoc()

    # gp tool parameters
    xs_dimensions_fc    <- in_params[[1]]
    features_fc         <- in_params[[2]]
    label_xs            <- as.logical(in_params[[3]])
    
    # Inputs for testing in RStudio
    #library(sp)
    #library(ggplot2)
    #library(ggrepel)
    #library(fluvgeo)
    #library(arcgisbinding)
    #arc.check_product()
    #xs_dimensions_fc    <- "Z:/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/riffle_dims"
    #features_fc         <- ""
    #label_xs            <- TRUE
    
    # Import fc to sp
    xs_dimensions <- fluvgeo::arc2sp(xs_dimensions_fc)
    features      <- fluvgeo::arc2sp(features_fc)

    # Call xs_plot function
    print(fluvgeo::xs_profile_plot(reach_xs_dims = xs_dimensions, 
                                   features = features, 
                                   label_xs = label_xs))
    
    return(out_params)
}
