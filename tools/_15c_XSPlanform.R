#' @title Calculate cross section planform dimensions
#' 
#' @description  Calculates stream planform statistics for the input cross 
#' section feature class. 
#' 
#' @export
#' @param xs_dimensions       character; the full path to an ESRI cross section 
#'                            dimension line feature class
#' @param bankline_points     character; the full path to an ESRI cross section 
#'                            points feature class
#'
#' @return A new cross section feature class with the planform dimensions added 
#' to the attribute table.
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr", "purrr", "tibble", "fluvgeo"))

    # gp tool parameters
    xs_dimensions      <- in_params[[1]]
    bankline_points    <- in_params[[2]]
    
    # Code for testing in RStudio
    # library(sp)
    # library(dplyr)
    # library(fluvgeo)
    # library(arcgisbinding)
    # arc.check_product()
    # xs_dimensions   <- "D:\\Workspace\\EMRRP_Sediment\\Methods\\FluvialGeomorph\\tests\\data\\test.gdb\\xs_200_dims"
    # bankline_points <- "D:\\Workspace\\EMRRP_Sediment\\Methods\\FluvialGeomorph\\tests\\data\\test.gdb\\bankline_points"
    # in_params <- list(xs_dimensions, bankline_points)
    
    # Verify parameters
    ## Create list of parameters (named using the parameter names)
    param_list <- tibble::lst(xs_dimensions, bankline_points)
    
    ## Get parameter verification table
    message("Compare input tool parameters")
    print(compare_params(in_params, param_list))

    # Convert ArcGIS fc to sp format
    xs_dimensions_sp   <- fluvgeo::arc2sp(xs_dimensions)
    bankline_points_sp <- fluvgeo::arc2sp(bankline_points)
    message("Conversion to sp complete")

    # Calculate planform dimensions
    xs_dims_plan <- fluvgeo::planform_dimensions(xs_dimensions_sp, 
                                             bankline_points_sp)
    message("planform dimensions complete")
    
    # Calculate metric ratios
    xs_dims_ratios <- fluvgeo::xs_metric_ratios(xs_dims_plan)
    message("metric ratios complete")
    
    # Convert SpatialLinesDataFrame to a SpatialPointsDataFrame
    xs_dims_pts <- xs2pts(xs_dims_ratios)
    message("conversion to points complete")
    
    # Write the xs lines with the planform dimensions
    xs_dims_path <- paste0(xs_dimensions, "_planform")
    fluvgeo::sp2arc(sp_obj = xs_dims_ratios, fc_path = xs_dims_path)
    
    # Write the xs points with the planform dimensions
    xs_dims_path <- paste0(xs_dimensions, "_planform_pts")
    fluvgeo::sp2arc(sp_obj = xs_dims_pts, fc_path = xs_dims_path)
    
    return(out_params)
}    