#' @title Check the validity of a `fluvgeo` `cross_section_points` data structure
#'
#' @description Checks that the input data structure `cross_section_points`
#' meets the requirements for this data structure.
#'
#' @export
#' @param xs_points_fc    character; a `cross_section_points` feature class
#'                        used by the fluvgeo package.
#' @param step            character; last completed processing step. One of
#'                        "station_points", "loop_bend"
#'
#' @details This is a wrapper to the `fluvgeo::check_cross_section_points` 
#' function.
#' 
#' @return Returns TRUE if the `cross_section_points` data structure matches the
#' requirements. The function throws an error for a data structure not matching
#' the data specification. Returns errors describing how the the data structure
#' doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_cross_section_points.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    
    # gp tool parameters
    xs_points_fc  <- in_params[[1]]
    step          <- in_params[[1]]
    
    # Import fc to sf
    cross_section_points_sf <- fc2sf(xs_points_fc)
    
    fc_name <- basename(xs_points_fc)
    
    # Check cross_section_points and print messages
    check <- try(check_cross_section_points(xs_points_sf,
                                            step = step))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, 
                      "is a valid cross_section_points data structure."))
    }
    
    return(out_params)
}