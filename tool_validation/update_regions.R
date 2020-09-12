# Update region dropdown list

library(RegionalCurve)

# Get the list of regions
regional_curve <- RegionalCurve::regional_curve

# Extract the region names 
region_names <- levels(regional_curve$region_name)

# Convert the vector of region names into a comma seperated list with each 
# region listed on a new line.
cat(paste(shQuote(region_names, type="cmd"), collapse=", \n"))

# Copy the console output to the `validate_Estimate_Bankfull.py` 
# initializeParameters value.list 