#' @title Check the validity of an `fluvgeo` `cross_section_dimension` data
#' structure
#'
#' @description Checks that the input data structure `cross_section_dimension`
#' meets the requirements for this data structure.
#'
#' @export
#' @param xs_dims_fc      character: A `cross_section_dimension` feature 
#'                        class data structure used by the fluvgeo package.
#' @param step            character; Last completed processing step. One of:
#'                        "level_1",
#'                        "cross_section_dimensions",
#'                        "rosgen_class", "shear_stress",
#'                        "stream_power", "planform", "metric_ratios"
#'
#' @details Cross section dimension feature classes evolve as different steps
#' are performed on them. The `step` parameter allows a `cross section_dimension`
#' data structure to be checked throughout its lifecycle. Each step defines a
#' changing set of requirements for the `cross section_dimension` data structure.
#'
#' @return Returns TRUE if the `cross_section_dimension` data structure matches
#' the requirements. The function throws an error for a data structure not
#' matching the data specification. Returns errors describing how the the data
#' structure doesn't match the requirement.
#'
tool_exec <- function(in_params, out_params) {
    # Declare location of script within the toolbox
    here::i_am("check/_check_cross_section_dimensions.R")
    # Load utility R functions
    fg_utils <- here::here("install", "FG_utils.R")
    source(fg_utils)
    message("Sourced utility functions: ", fg_utils)
    load_packages(c("dplyr", "raster", "fluvgeo"))
    # gp tool parameters
    xs_dims_fc  <- in_params[[1]]
    step        <- in_params[[2]]
    
    # Import fc to sf
    xs_dims_sf <- fc2sf(xs_dims_fc)
    
    fc_name <- basename(xs_dims_fc)
    
    # Check cross_section and print messages
    check <- try(check_cross_section_dimensions(xs_dims_sf, 
                                                step = step))
    if(inherits(check, "try-error")) {
        print(geterrmessage())
    } else { 
        message(paste(fc_name, 
                      "is a valid cross_section_dimensions data structure."))
    }
    
    return(out_params)
}