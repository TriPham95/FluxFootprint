################################################################################
################################################################################
# Remove previous object before running                                        
rm(list=ls(all=TRUE))
################################################################################
library(raster)
library(sp)
library(gdalUtils)
library(rgdal)
library(GISTools)
library(sf)
library(maptools)
raster_inputpath <- "/home/tpham/Documents/Ecological/USGS_NED_13_n36w098_ArcGrid/grdn36w098_13/"
shape_inputpath <- "/home/tpham/Documents/Ecological/DaveBlueCreek/"
RasterElevation <- "prj.adf"
shapefile <- "globalwatershed.shp"

# Reading Raster
FullRaster <- paste(raster_inputpath, RasterElevation, sep = "")
Ras1 <- raster(FullRaster)

# Reading the shapefile
FullWatershed <- paste(shape_inputpath, shapefile, sep = "")
Polygons <- st_read(FullWatershed)
Polygons <- as(Polygons, "Spatial")
CRSPolygons <- crs(Ras1)
Dave <- spTransform(Polygons, CRSPolygons)
Dave <- as(Dave, "sf")
Ras2 <- crop(Ras1, extent(Polygons))
newraster <- mask(Ras2, Dave)
plot(newraster, main = "Dave Blue Creek Watershed")
scalebar(2, type = "bar", div = 4)

