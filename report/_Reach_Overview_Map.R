#' @title Reach Overview Map
#'
#' @description Produces a reach overview map displaying cross section
#' locations over an aerial image or elevation multi-direction shaded relief.
#'
#' @export
#' @param flowline_fc         Path to a flowline feature class
#' @param cross_section_fc    Path to a cross section feature class
#' @param xs_label_freq       numeric; An integer indicating the frequency of
#'                            cross section labels.
#' @param background          character; The type of map background. One of
#'                            "aerial" or "elevation"
#' @param exaggeration        numeric; The degree of terrain exaggeration.
#' @param extent_factor       numeric; The amount the extent is expanded around
#'                            the cross section feature class. Values greater
#'                            than one zoom out, values less than one zoom in.
#'
#' @return A ggplot object
#'
tool_exec <- function(in_params, out_params) {
    # Load utility R functions
    dir_name <- getSrcDirectory(function(x) {x})
    fg <- dirname(dir_name)
    fg_install <- file.path(fg, "install")
    source(file.path(fg_install, "FG_utils.R"))
    # Load required libraries
    load_packages(c("tibble", "sf", "sp", "terra", "terrainr", "maptiles",
                    "raster", "tmap", "fluvgeo"))
    
    # Ensure pandoc can be found
    message("Setting pandoc directory...")
    set_pandoc()
    
    # gp tool parameters
    flowline_fc      <- in_params[[1]]
    cross_section_fc <- in_params[[2]]
    xs_label_freq    <- in_params[[3]]
    background       <- in_params[[4]]
    exaggeration     <- in_params[[5]]
    extent_factor    <- in_params[[6]]
    
    # Inputs for testing in RStudio
    # library(sf)
    # library(sp)
    # library(ceramic)
    # library(raster)
    # library(tmap)
    # library(arcgisbinding)
    # arc.check_product()
    # library(fluvgeo)
    # 
    # flowline_fc      <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Sites/02_Cole_Creek/Data/y2016_R1.gdb/flowline"
    # cross_section_fc <- "D:/Workspace/EMRRP_Sediment/PapillionCreek_NE/Sites/02_Cole_Creek/Data/y2016_R1.gdb/xs_50_dims_L1"
    # xs_label_freq    <- 10
    # background       <- "aerial"
    # exaggeration     <- 1
    # extent_factor    <- 2
    
    # Verify parameters
    ## Create list of parameters (named using the parameter names)
    param_list <- tibble::lst(flowline_fc, cross_section_fc, xs_label_freq, 
                              background, exaggeration, extent_factor)
    
    ## Get parameter verification table
    message("Compare input tool parameters")
    print(compare_params(in_params, param_list))
    
    # Convert fc to sf object
    flowline_sf      <- fluvgeo::fc2sf(flowline_fc)
    cross_section_sf <- fluvgeo::fc2sf(cross_section_fc)
    
    # Call the map_reach_overview function
    print("calling map...")
    print(fluvgeo::map_reach_overview(flowline_sf = flowline_sf,
                                      cross_section_sf = cross_section_sf,
                                      xs_label_freq = xs_label_freq,
                                      background = background,
                                      exaggeration = exaggeration,
                                      extent_factor = extent_factor))
    
    return(out_params)
}