#' @title Calculate cross section dimensions
#' 
#' @description  Calculates cross section hydraulic geometry dimensions for 
#'     the input cross section feature class. 
#' 
#' @export
#' @param xs_fc               character; the full path to an ESRI cross section 
#'                            line feature class
#' @param xs_points_fc        character; the full path to an ESRI cross section 
#'                            points feature class
#' @param bankfull_elevation  numeric; The bankfull elevation (in feet) that is
#'                            used to calculate hydraulic geometry.
#' @param lead_n              numeric; The number of features to lead/lag on
#'                            either side of each feature that will be used to
#'                            calculate the slope and sinuosity.
#' @param use_smoothing       boolean; determines if smoothed elevation values
#'                            are used to calculate gradient. values are:
#'                            TRUE, FALSE (default)
#' @param loess_span          numeric; the loess regression span parameter,
#'                            defaults to 0.05
#' @param vert_units          character; The vertical units. One of: "m"
#'                            (meter), "ft" (foot), "us-ft" (us survey foot)
#' @param discharge_method  character; The method for calculating discharge (Q).
#'                          Must be one of: "model_measure", "regional_curve",
#'                          "width_relationship".
#' @param discharge_value   numeric; The discharge value (single value or vector)
#'                          to use for the stream power calculation. Required
#'                          if discharge_method = "model_measure".
#' @param region            character; The regional curve name used to calculate
#'                          discharge. Required if discharge_method =
#'                          "regional_curve". This parameter is passed to the
#'                          RegionalCurve::RHG function. See the RegionalCurve
#'                          package for a list of regions with discharge
#'                          relationships.
#' @param drainage_area     numeric; The drainage area (single value or vector)
#'                          used by the RegionalCurve::RHG function to calculate
#'                          discharge. Required if discharge_method =
#'                          "regional_curve".
#' @param width_method      character; The name of the width relationship used
#'                          to calculate discharge (Q) from width. Required if
#'                          discharge_method = "width_relationship". Must be
#'                          one of: <list goes here when implemented>
#'
#' @return A new cross section feature class with the hydraulic geometry 
#'      dimensions is added to the attribute table.
#'      
#' #TODO Create an fluvgeo function to perform this operation
#' 
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("sp", "dplyr", "purrr", "tibble"))
    # Load FluvialGeomorph R packages
    load_fluvgeo_packages()
    
    # gp tool parameters
    xs_fc              <- in_params[[1]]
    xs_points_fc       <- in_params[[2]]
    bankfull_elevation <- in_params[[3]]
    lead_n             <- in_params[[4]]
    use_smoothing      <- in_params[[5]]
    loess_span         <- in_params[[6]]
    vert_units         <- in_params[[7]]
    discharge_method   <- unlist(in_params[[8]])
    discharge_value    <- in_params[[9]]
    region             <- in_params[[10]]
    drainage_area      <- in_params[[11]]
    width_method       <- in_params[[12]]
    
    # Code for testing in RStudio
    # library(sp)
    # library(dplyr)
    # library(fluvgeo)
    # library(arcgisbinding)
    # arc.check_product()
    # xs_fc              <- "D:\\Workspace\\EMRRP_Sediment\\Methods\\FluvialGeomorph\\tests\\data\\test.gdb\\xs_200"
    # xs_points_fc       <- "D:\\Workspace\\EMRRP_Sediment\\Methods\\FluvialGeomorph\\tests\\data\\test.gdb\\xs_200_points"
    # bankfull_elevation <- 104.5
    # lead_n             <- 1
    # use_smoothing      <- TRUE
    # loess_span         <- 1
    # vert_units         <- "ft"
    # discharge_method   <- "regional_curve"
    # discharge_value    <- NULL
    # region             <- "Lower Southern Driftless"
    # drainage_area      <- 41
    # width_method       <- NULL
    # in_params <- list(xs_fc, xs_points_fc, bankfull_elevation, lead_n,
    #                   use_smoothing, loess_span, vert_units,
    #                   discharge_method, discharge_value, region, 
    #                   drainage_area, width_method)
    
    # Verify parameters
    ## Create list of parameters (named using the parameter names)
    param_list <- tibble::lst(xs_fc, xs_points_fc, bankfull_elevation, lead_n,
                              use_smoothing, loess_span, vert_units,
                              discharge_method, discharge_value, region, 
                              drainage_area, width_method)
    
    ## Get parameter verification table
    message("Compare input tool parameters")
    print(compare_params(in_params, param_list))
    
    # Convert ArcGIS fc to sp format
    xs        <- fluvgeo::arc2sp(xs_fc)
    xs_points <- fluvgeo::arc2sp(xs_points_fc)
    message("Conversion to sp complete")
    
    # Calculate cross section dimensions
    xs_dims <- fluvgeo::cross_section_dimensions(xs = xs,
                                        xs_points = xs_points,
                                        bankfull_elevation = bankfull_elevation,
                                        lead_n = lead_n,
                                        use_smoothing = use_smoothing,
                                        loess_span = loess_span,
                                        vert_units = vert_units)
    message("Calculated cross section dimensions")
    
    # Calculate shear stress
    xs_dims_ss <- fluvgeo::shear_stress(xs_dims)
    message("Calculated shear stress")
    
    # Calculate stream power
    xs_dims_spow <- fluvgeo::stream_power(xs_dims_ss, 
                                      discharge_method = discharge_method,
                                      discharge_value = discharge_value,
                                      region = region,
                                      drainage_area = drainage_area,
                                      width_method = width_method)
    message("Calculated stream power")
    
    # Join the xs_dims to xs
    xs_dims_sp <- sp::merge(xs, xs_dims_spow, by.x = "Seq", by.y = "Seq")
    message("join table of metrics to fc complete")
    
    # Write the xs with hydraulic dimensions
    xs_dims_path <- paste0(xs_fc, "_dims")
    fluvgeo::sp2arc(sp_obj = xs_dims_sp, fc_path = xs_dims_path)
    
    return(out_params)
}