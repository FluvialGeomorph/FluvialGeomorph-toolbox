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
#' to the attribute table
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    source(file.path(dir_name, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr"))
    # Load FluvialGeomorph R packages
    load_fgm_packages()

    # gp tool parameters
    xs_dimensions      <- in_params[[1]]
    bankline_points    <- in_params[[2]]
    
    # # Code for testing in RStudio
    # library(sp)
    # library(dplyr)
    # library(fgm)
    # library(arcgisbinding)
    # arc.check_product()
    # xs_dimensions   <- "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/riffle_channel_dims"
    # bankline_points <- "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/bankline_points"

    # Convert ArcGIS fc to sp format
    xs_dimensions_sp   <- fgm::arc2sp(xs_dimensions)
    bankline_points_sp <- fgm::arc2sp(bankline_points)
    message("Conversion to sp complete")
    
    # Convert sp format to data frame
    bankline_pts <- bankline_points_sp@data
    
    # Calculate planform dimensions
    bends_planform <- fgm::planform(bankline_pts)
    message("planform calculated")
    
    # Join planform dimensions to xs_dimension
    xs_dims <- sp::merge(xs_dimensions_sp, bends_planform, 
                         by.x = c("loop", "bend"), by.y = c("loop", "bend"))
    message("join planform metrics to xs_dimensions complete")
    
    # Calculate metric ratios
    xs_dims_ratios <- fgm::xs_metric_ratios(xs_dims)
    
    # Remove unneeded fields from xs_dims
    drop_fields <- c("OBJECTID", "OBJECTID_1")
    xs_dims_ratios <- xs_dims_ratios[, !names(xs_dims_ratios) %in% drop_fields]
    
    # Write the xs_dims with planform dimensions
    xs_dims_path <- paste0(xs_dimensions, "_planform")
    fgm::sp2arc(sp_obj = xs_dims_ratios, fc_path = xs_dims_path)
    
    return(out_params)
}    