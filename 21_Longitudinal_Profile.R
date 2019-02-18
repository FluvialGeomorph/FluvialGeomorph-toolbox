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
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "ggplot2", "ggrepel"))
    # Load FluvialGeomorph R packages
    load_fgm_packages()
    
    # gp tool parameters
    xs_dimensions_fc    <- in_params[[1]]
    features_fc         <- in_params[[2]]
    label_xs            <- as.logical(in_params[[3]])
    
    # temp variables for development within R
    #library(sp)
    #library(ggplot2)
    #library(ggrepel)
    #library(fgm)
    #library(arcgisbinding)
    #arc.check_product()
    #xs_dimensions_fc    <- "Z:/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/riffle_dims"
    #features_fc         <- ""
    #label_xs            <- TRUE
    
    # Import fc to sp
    xs_dimensions <- arc2sp(xs_dimensions_fc)
    features      <- arc2sp(features_fc)

    # Convert to a data frame
    xs_dims <- xs_dimensions@data
    feats   <- features@data
    
    # Call xs_plot function
    print(xs_profile_plot(reach_xs_dims = xs_dims, 
                          features = feats, 
                          label_xs = label_xs))
    
    return(out_params)
}
