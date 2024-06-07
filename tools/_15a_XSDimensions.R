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
#'      dimensions added to the attribute table.
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
    load_packages(c("dplyr", "purrr", "tibble", "fluvgeo"))
    
    # gp tool parameters
    xs_fc              <- in_params[[1]]
    lead_n             <- in_params[[2]]
    use_smoothing      <- in_params[[3]]
    loess_span         <- in_params[[4]]
    vert_units         <- in_params[[5]]

    # Code for testing in RStudio
    # library(dplyr)
    # library(fluvgeo)
    # xs_fc              <- "C:\\Workspace\\FluvialGeomorph\\fluvgeo\\inst\\extdata\\y2016_R1.gdb\\feature_dataset\\xs_50"
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
    message("Calculated cross section dimensions table")
    
    # Join the xs_dims to xs_sf
    xs_dims_sf <- xs_sf %>%
        dplyr::select(Seq) %>%
        dplyr::left_join(as.data.frame(xs_dims), by = join_by(Seq))
    message("join table of cross section dimensions to sf complete")
    
    # Write the hydraulic dimensions to a csv file
    # arcgisbinding::arc.write unable to reliably export sf to gdb
    table_name <- paste0(basename(xs_fc), "_dims_L1_table.csv")
    gdb_folder_path <- dirname(dirname(dirname(xs_fc)))
    csv_path <- file.path(gdb_folder_path, table_name)
    fluvgeo::sf2csv(sf_object = xs_dims_sf, 
                    csv_path = csv_path)
    message("saving csv complete: ", csv_path)
    
    return(out_params)
}