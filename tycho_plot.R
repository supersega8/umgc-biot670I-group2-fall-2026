tycho_plot.R

@author: Natasha

# use created csv ('Project Tycho Filtered Dates.csv') to begin to plot vaccine data by year/region

install.packages("ggplot2")
library(ggplot2)

# use correct file name/path for device
data <- read.csv("C:/Users/nkiel/Documents/UMGC/F 2026/BIOT 670I/Project Files/Downloaded Files/Project Tycho Filtered Dates.csv")

# multi time plot

Tycho_plot <- ggplot (data, aes(x = Year, y = incidence_per_10000, color = disease)) +
 geom_line(linewidth = 1) +
 geom_point(size = 1.5, alpha = 0.6) +
 labs (title = "Project Tycho Measles, Mumps, Rubella, & Polio Since 1928", subtitle = "Comparative Analysis of Four Distinct Diseases", x = "Year", y = "Incidence (per 10000)", color = "Disease Type") +
 scale_x_continuous(breaks = seq(min(data$Year), max(data$Year), by = 10)) +
 theme_minimal(base_size = 14) +
 theme(legend.position = "bottom", plot.title = element_text(face = "bold"))

# save plot to PDF
ggsave("Tycho_Plot.pdf", plot = Tycho_plot, width = 8, height = 6)

# save plot to PNG
# save last plot used
ggplot2::ggsave("Tycho_Plot.png")