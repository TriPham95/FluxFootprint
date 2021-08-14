################################################################################
################################################################################
# Remove previous object before running                                        
# rm(list=ls(all=TRUE))
################################################################################
library(raster)
library(sp)
library(gdalUtils)
library(rgdal)
library(GISTools)
library(sf)
library(maptools)
library(rasterVis)
inputpath <- "C:/Users/Tri/Desktop/EF5/GIS/"
RasterFile <- "CherryCreekDEM.tif"
shapefile <- "globalwatershed.shp"


# Reading the Raster
Raster1 <- paste(inputpath, RasterFile, sep = "")
CherryCreekRaster <- raster(Raster1)

# Reading the shapefile
CherryWatershed <- paste(inputpath, shapefile, sep = "")
CherryPolygons <- st_read(CherryWatershed)
CherryPolygons <- as(CherryPolygons, "Spatial")
CRSPolygons <- crs(CherryCreekRaster)

CherryCreekNew <- spTransform(CherryPolygons, CRSPolygons)
CherryCreekNew <- as(CherryCreekNew, "sf")



Raster2 <- crop(CherryCreekRaster, extent(CherryCreekNew))
FinalRaster <- mask(Raster2, CherryCreekNew)



plot(FinalRaster, main = "Cherry Creek Watershed")
scalebar(10, type = "bar", div = 4)
# plot(Dave2$geometry, add = T)
writeRaster(FinalRaster, file = paste(inputpath, "CherryCreekCropped.tif", 
                                      sep = ""),
            format = "GTiff")


# shape_inputpath2 <- "/home/tpham/Documents/Ecological/DaveBlueCreek/"
# shapefile2 <- "globalwatershed.shp"
# FullWatershed2 <- paste(shape_inputpath2, shapefile2, sep = "")
# Polygons2 <- st_read(FullWatershed2)
# Polygons2 <- as(Polygons2, "Spatial")
# CRSPolygons2 <- crs(Ras1)
# Dave2 <- spTransform(Polygons2, CRSPolygons2)
# Dave2 <- as(Dave2, "sf")


plot3D(FinalRaster, zfac = 1, col = topo.colors)





















