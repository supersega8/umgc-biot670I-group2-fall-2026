# BIOT 670i Capstone: R dependencies
# Run this script in R or RStudio after installing R (used version: 4.5.1).
# RStudio is an IDE; it is not a pip package.

required_packages <- c(
  "tidyverse", # Includes ggplot2, dplyr, tidyr, readr, etc.
  "Hmisc"      # Used in historical NIS data processing
)

missing_packages <- setdiff(required_packages, rownames(installed.packages()))
if (length(missing_packages) > 0) {
  install.packages(missing_packages, repos = "https://cloud.r-project.org")
}

message("R package setup complete.")
