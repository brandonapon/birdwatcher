# Get streamlined Google map of dc in black and white
g <- ggmap(get_googlemap(
	center = c(-77.04136, 38.90573), 
	zoom = 13, 
	maptype = "roadmap", 
	color = "bw", 
	style = c(feature = "all", element = "labels", visibility = "off")
	)
)

# Creates a map plot for a given set of bird locations
# Input: dataframe of location data, subtitle for the map
# Returns: altered ggmap with heatmap
createPlot <- function(data, title) {
  time <- paste("Time: ", substring(title, 1, 2), ":", substring(title, 4, 5), sep = "")
  g + 
    stat_bin2d(
    aes(x = longitude, y = latitude),
    size = 1,
    bins = 40,
    alpha = 0.5,
    data = data
  ) +
    scale_fill_continuous(low="yellow", high="red") +
    labs(
      title = "Tracking the flow of Bird scooters across DC",
      subtitle = time,
      x = "",
      y = "",
      caption = "conormclaughlin.net"
    ) +
    theme_minimal() +
    theme(
      legend.position = "none",
      axis.title.x = element_blank(),
      axis.title.y = element_blank(),
      axis.ticks = element_blank(),
      axis.text.y = element_blank(),
      axis.text.x = element_blank(),
      plot.title = element_text(size = 16, face = "bold"),
      plot.subtitle = element_text(size = 12)
    )
}
