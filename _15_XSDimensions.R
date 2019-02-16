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
#'
#' @return A new cross section feature class with the hydraulic geometry 
#'      dimensions added to the attribute table
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
    xs_fc              <- in_params[[1]]
    xs_points_fc       <- in_params[[2]]
    bankfull_elevation <- as.numeric(in_params[[3]])

    # Code for testing in RStudio
    #library(arcgisbinding)
    #arc.check_product()
    #xs_fc              <- "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/XS_50_test"
    #xs_points_fc       <- "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/XS_50_test_points"
    #bankfull_elevation <- 103

    # Convert ArcGIS fc to sp format
    xs        <- fgm::arc2sp(xs_fc)
    xs_points <- fgm::arc2sp(xs_points_fc)

    # Create a list to hold the xs dimensions
    xs_geoms <- list()

    # Iterate through ReachNames
    for (g in unique(xs_points$ReachName)) {
        # Iterate through xs's and calculate dimensions
        for (i in xs[xs$ReachName == g, ]$Seq) {
            # Subset for the current stream and convert to data frame
            xs_pts <- xs_points@data[xs_points$ReachName == g, ]
            # Calculate xs dimensions
            dims <- fgm::xs_metrics(xs_points = xs_pts,
                                    stream = g,
                                    xs_number = i,
                                    bankfull_elevation = bankfull_elevation)
            xs_geoms[[i]] <- dims
        }
    }

    # Append the list of xs dimensions into a singe data frame
    reach_geoms <- dplyr::bind_rows(xs_geoms)

    # Join the reach_geoms to xs_fc
    xs_dims <- sp::merge(xs, reach_geoms, by.x = "Seq", by.y = "cross_section")

    # Write the xs_fc with hydraulic dimensions
    xs_dims_path <- paste0(xs_fc, "_dims")
    fgm::sp2arc(sp_obj = xs_dims, fc_path = xs_dims_path)

    return(out_params)
}