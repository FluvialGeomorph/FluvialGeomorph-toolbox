#' @title Check the validity of an `fluvgeo` `cross_section` data structure
#'
#' @description Checks that the input data structure `cross_section` meets
#' the requirements for this data structure.
#'
#' @export
#' @param cross_section_fc   character: a `cross_section` feature class
#'                           used by the fluvgeo package.
#' @param step               character; last completed processing step. One of
#'                           "assign_ids", "watershed_area", "river_position",
#'                           "station_points", "loop_bend"
#'
#' @details Cross section feature classes evolve as different steps are
#' performed on them. The `step` parameter allows a `cross section` data
#' structure to be checked throughout its lifecycle. Each step defines a
#' changing set of requirements for the `cross section` data structure.
#'
#' @return Returns TRUE if the `cross_section` data structure matches the
#' requirements. The function throws an error for a data structure not matching
#' the data specification. Returns errors describing how the the data structure
#' doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_cross_section.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    # gp tool parameters
    cross_section_fc  <- in_params[[1]]
    step              <- in_params[[2]]
    
    # Import fc to sp
    cross_section_sf <- fc2sf(cross_section_fc)
    
    fc_name <- basename(cross_section_fc)
    
    # Check cross_section and print messages
    check <- try(check_cross_section(cross_section_sf, 
                                     step = step))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, "is a valid cross_section data structure."))
    }
    
    return(out_params)
}