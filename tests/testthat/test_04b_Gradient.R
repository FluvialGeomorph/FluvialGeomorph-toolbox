here::i_am("tests/testthat/test_04b_Gradient.R")
source(here::here("tools", "_04b_Gradient.R"))


test_that("_04b_Gradient output exists", {
    # Set the tool parameters
    library(raster)
    flowline_points_fc <- "C:\\Workspace\\FluvialGeomorph\\fluvgeo\\inst\\extdata\\y2016_R1.gdb\\feature_dataset\\flowline_points"
    gradient_distance  <- 1000
    use_smoothing      <- TRUE
    loess_span         <- 0.05
    in_params <- list(flowline_points_fc, gradient_distance, use_smoothing, 
                      loess_span)
    # Call the tool
    tool_exec(in_params, out_params = list())
    
    # Expected output
    csv_name <- paste0(basename(flowline_points_fc), "_gradient.csv")
    gdb_folder_path <- dirname(dirname(dirname(flowline_points_fc)))
    csv_path <- file.path(gdb_folder_path, csv_name)
    
    # Check the outputs
    expect_true(file.exists(csv_path))

    # Cleanup
    file.remove(csv_path)
})
