# mumps_plot.R

# @author: Natasha

# use source excel ('Mumps 1980 - 2025.xlsx') to begin to plot vaccine data by year/region

install.packages("readxl")

library (ggplot2)
library (tidyr)
library (tidyverse)
library (readxl)

# use correct file name/path for device
mumps_data <- read_excel("C:/Users/nkiel/Documents/UMGC/F 2026/BIOT 670I/Project Files/Downloaded Files/Mumps 1980 - 2025.xlsx")

# multi time plot
# first have to tidy data
# CRITICAL CLEANUP: Remove text commas from numbers so R can graph them

mumps_tidy <- mumps_data %>%
     filter(`Country / Region` %in% c(
         "African Region", "Eastern Mediterranean Region", "European Region", "Region of the Americas", "South-East Asia Region", "Western Pacific Region"
     )) %>%
 pivot_longer(
     cols = `2025`:`1999`,
     names_to = "year",
     values_to = "cases"
 ) %>%
 mutate(year = as.numeric(year),
        cases = str_remove_all(cases, "[\\s,]"),
        cases = as.numeric(cases))

# plot

mumps_plot <- ggplot(mumps_tidy, aes(x = year, y = cases, color = `Country / Region`, group = `Country / Region`)) +
 geom_line(na.rm = TRUE, linewidth = 1) +
 geom_point(na.rm = TRUE) +
 facet_wrap(~ `Country / Region`, scales = "free_y") +
 labs (title = "Mumps Cases By Region Since 1980", x = "Year", y = "Number of Cases", color = "WHO Region") +
 theme_minimal() +
 theme(legend.position = "bottom")

print(mumps_plot)

# save plot to PDF
ggsave("Mumps_Plott.pdf", plot = mumps_plot, width = 8.5, height = 11)

# save plot to PNG
# save last plot used
ggplot2::ggsave("Mumps_Plot.png")
