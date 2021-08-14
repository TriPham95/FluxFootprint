library(raster)
library(shapefiles)

# Set working directory to your location
setwd("C:/Users/Tri/Desktop/EF5/GIS")

z=raster("CherryCreekDEM.tif")
plot(z)

# Pitremove
system("-n 8 pitremove -z CherryCreekDEM.tif -fel CherryCreekDEMfel.tif")
# fel = raster("CherryCreekDEMfel.tif")
# plot(fel)
