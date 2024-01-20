#' @title Calculate Level 1 Cross Section Dimensions
#' 
#' @description  Calculates Level 1 cross section dimensions for the input 
#' cross section feature class. 
#' 
#' @export
#' @param xs_fc               feature class; The full path to a cross section 
#'                            line feature class.
#' @param lead_n              numeric; The number of features to lead/lag on
#'                            either side of each feature that will be used to
#'                            calculate the slope and sinuosity.
#' @param use_smoothing       boolean; Determines if smoothed elevation values
#'                            are used to calculate gradient. values are:
#'                            TRUE, FALSE (default)
#' @param loess_span          numeric; The loess regression span parameter. 
#'                            Use values 0.05 - 1. Defaults to 0.05
#' @param vert_units	      character; The DEM vertical units. One of: "m"
#'                            (meter), "ft" (foot), "us-ft" (us survey foot)
#'
#'
#' @return A new cross section feature class with the hydraulic geometry 
#'      dimensions is added to the attribute table.
#'      
#' #TODO Create an fluvgeo function to perform this operation
#' 
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("tools/_15a_XSDimensions.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("sp", "dplyr", "purrr", "tibble", "fluvgeo"))
    
    # gp tool parameters
    xs_fc              <- in_params[[1]]
    lead_n             <- in_params[[2]]
    use_smoothing      <- in_params[[3]]
    loess_span         <- in_params[[4]]
    vert_units         <- in_params[[5]]

    # Code for testing in RStudio
    # library(sp)
    # library(dplyr)
    # library(fluvgeo)
    # library(arcgisbinding)
    # arc.check_product()
    # xs_fc              <- "D:\\Workspace\\EMRRP_Sediment\\Methods\\FluvialGeomorph-toolbox\\tests\\data\\test.gdb\\xs_200"
    # lead_n             <- 1
    # use_smoothing      <- TRUE
    # loess_span         <- 0.5
    # vert_units         <- "ft"
    
    # Verify parameters
    ## Create list of parameters (named using the parameter names)
    param_list <- tibble::lst(xs_fc, lead_n, use_smoothing, 
                              loess_span, vert_units)
    
    ## Get parameter verification table
    message("Compare input tool parameters")
    print(compare_params(in_params, param_list))
    
    # Convert ArcGIS fc to sf format
    xs_sf <- fluvgeo::fc2sf(xs_fc)
    message("Conversion to sf complete")
    
    # Calculate cross section dimensions
    xs_dims <- fluvgeo::cross_section_dimensions_L1(xs_sf = xs_sf,
                                                 lead_n = lead_n,
                                                 use_smoothing = use_smoothing,
                                                 loess_span = loess_span,
                                                 vert_units = vert_units)
    message("Calculated cross section dimensions")
    
    # Join the xs_dims to xs
    xs_dims_sf <- sp::merge(xs_sf[, c("Seq")], 
                            xs_dims, 
                            by = "Seq")
    message("join table of metrics to fc complete")
    
    # Convert sf to sp for writing
    xs_dims_sp <- sf::as_Spatial(xs_dims_sf)
    
    # Write the hydraulic dimensions to a file geodatabase table
    table_name <- paste0(basename(xs_fc), "_dims_L1_table")
    gdb_path   <- dirname(dirname(xs_fc))
    table_path <- file.path(gdb_path, table_name)
    fluvgeo::sx2arc_table(sx_obj = xs_dims_sp, table_path = table_path)
    message("saving table complete")
    
    return(out_params)
}