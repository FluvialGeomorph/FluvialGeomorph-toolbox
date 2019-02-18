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
#' @param lead_lag            numeric; The number of features to lead/lag on
#'                            either side of each feature that will be used to
#'                            calculate the slope and sinuosity.
#' @param use_smoothing       boolean; determines if smoothed elevation values
#'                            are used to calculate gradient. values are:
#'                            TRUE, FALSE (default)
#' @param loess_span          numeric; the loess regression span parameter,
#'                            defaults to 0.05
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
    lead_lag           <- as.numeric(in_params[[4]])
    use_smoothing      <- as.logical(in_params[[5]])
    loess_span         <- as.numeric(in_params[[6]])

    # Code for testing in RStudio
    library(sp)
    library(dplyr)
    library(fgm)
    library(arcgisbinding)
    arc.check_product()
    xs_fc              <- "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/riffle"
    xs_points_fc       <- "//mvrdfs/egis/Work/Office/Regional/ERDC/EMRRP_Sediment/Senachwine/Data/Watershed/01_LowerSenachwineCreek/LowerSenachwineCreek.gdb/riffle_points"
    bankfull_elevation <- 103
    lead_lag           <- 1
    use_smoothing      <- TRUE
    loess_span         <- 1

    # Convert ArcGIS fc to sp format
    xs        <- fgm::arc2sp(xs_fc)
    xs_points <- fgm::arc2sp(xs_points_fc)

    # Create a list to hold the xs dimensions
    xs_geoms_ss <- list()
    xs_geoms    <- list()

    # Iterate through xs ReachNames
    for (g in unique(xs_points$ReachName)) {
        # Subset xs for the current reach
        xs_reach <- xs@data[xs$ReachName == g, ]
        
        # Calculate slope and sinuosity for xs_reach
        xs_reach_ss <- fgm::slope_sinuosity(xs_reach,
                                            lead_lag = lead_lag,
                                            use_smoothing = use_smoothing,
                                            loess_span = loess_span)
        xs_geoms_ss[[g]] <- xs_reach_ss
        
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
    # Append the list of xs dimensions into a single data frame 
    # (slope_sinuosity)
    reach_geoms <- dplyr::bind_rows(xs_geoms_ss)

    # Append the list of xs_points dimensions into a singe data frame 
    # (xs_dimensions)
    xs_reach_geoms <- dplyr::bind_rows(xs_geoms)
    
    # Join reach_geoms and xs_reach_geoms
    dims_join <- merge(x = reach_geoms,
                       y = xs_reach_geoms,
                       by.x = "Seq", by.y = "cross_section")
    
    # Remove fields from dims_join already on xs
    # Get the list of names from xs
    xs_names <- names(xs@data)
    # Retain the field `Seq` for the join
    xs_names <- xs_names[xs_names != "Seq"]
    # Add other fields to be removed
    xs_names <- append(xs_names, c("reach_name", "xs_type"))
    # Remove the uneeded fields
    dims_join_reduced <- select(dims_join, -xs_names)
    
    # Join the reach_geoms to xs_fc
    xs_dims <- sp::merge(xs, dims_join_reduced, by.x = "Seq", by.y = "Seq")

    # Write the xs_fc with hydraulic dimensions
    xs_dims_path <- paste0(xs_fc, "_dims")
    fgm::sp2arc(sp_obj = xs_dims, fc_path = xs_dims_path)

    return(out_params)
}