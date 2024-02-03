#' @title Calculate Level 3 Cross Section Planform Dimensions
#' 
#' @description  Calculates Level 3 stream planform statistics for the input 
#' cross section feature class. 
#' 
#' @export
#' @param xs_dims_L2          character; The full path to a Level 2 cross 
#'                            section dimension line feature class. 
#' @param bankline_points     character; The full path to an bankline points 
#'                            feature class. 
#'
#' @return A new cross section feature class with the planform dimensions added 
#' to the attribute table.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("tools/_15c_XSPlanform.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    # Load required libraries
    load_packages(c("dplyr", "purrr", "tibble", "fluvgeo"))

    # gp tool parameters
    xs_dimensions      <- in_params[[1]]
    bankline_points    <- in_params[[2]]
    
    # Code for testing in RStudio
    # library(dplyr)
    # library(fluvgeo)
    # xs_dims_L2      <- "C:\\Workspace\\FluvialGeomorph\\fluvgeo\\inst\\extdata\\y2016_R1.gdb\\feature_dataset\\xs_50_dims_L2"
    # bankline_points <- "C:\\Workspace\\FluvialGeomorph\\fluvgeo\\inst\\extdata\\y2016_R1.gdb\\feature_dataset\\bankline_points"
    # in_params <- list(xs_dimensions, bankline_points)

    # Verify parameters
    ## Create list of parameters (named using the parameter names)
    param_list <- tibble::lst(xs_dims_L2, bankline_points)
    
    ## Get parameter verification table
    message("Compare input tool parameters")
    print(compare_params(in_params, param_list))

    # Convert ArcGIS fc to sp format
    xs_dims_L2_sf   <- fluvgeo::fc2sf(xs_dims_L2)
    bankline_points_sf <- fluvgeo::fc2sf(bankline_points)
    message("Conversion to sp complete")

    # Calculate planform dimensions
    xs_dims_plan <- fluvgeo::planform_dimensions(xs_dims_L2_sf, 
                                                 bankline_points_sf)
    message("planform dimensions complete")
    
    # Calculate metric ratios
    xs_dims_ratios <- fluvgeo::xs_metric_ratios(xs_dims_plan)
    message("metric ratios complete")
    
    # Write the hydraulic dimensions to a csv file
    # arcgisbinding::arc.write unable to reliably export sf to gdb
    xs_dims_L3_name <- paste0(basename(xs_dims_L2))
    csv_name <- gsub("_L2", "_L3_table.csv", xs_dims_L3_name, fixed = TRUE)
    gdb_folder_path <- dirname(dirname(dirname(xs_dims_L2)))
    csv_path <- file.path(gdb_folder_path, csv_name)
    fluvgeo::sf2csv(sf_object = xs_dims_ratios,
                    csv_path = csv_path)
    message("saving csv complete: ", csv_path)
    
    return(out_params)
}    