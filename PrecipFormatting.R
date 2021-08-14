# Remove previous object before running
rm(list=ls(all=TRUE))
library(tools)
library(rgdal)
library(gdalUtils)
library(raster)
options(scipen=999)


# User Input
inputpath <- "C:/Users/Tri/Desktop/EF5/RawData/Precip/"
outputpath <- "C:/Users/Tri/Desktop/EF5/RawData/P2/"
RasProjection <- "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs"
WRaster = FALSE

# setwd(inputpath)
PrecipFiles <- list.files(path = inputpath, pattern = "\\.tif$")

# Ras_i <- raster(paste(inputpath, PrecipFiles[1], sep = ""))
# proj4string(Rasi) <- CRS(RasProjection)


for (i in 1:length(PrecipFiles)) {
  cat("Processing File ", i, " of ", length(PrecipFiles), "\n")
  Ras_i <- raster(paste(inputpath, PrecipFiles[i], sep = ""))
  proj4string(Ras_i) <- CRS(RasProjection)

  Year <- substr(file_path_sans_ext(
    file_path_sans_ext(
      file_path_sans_ext(PrecipFiles[i]))), 
    start = 6, 
    stop = nchar(PrecipFiles[i]))
  
  if(nchar(Year) == 8) {
    Year = Year
    Hour <- substr(file_path_sans_ext(file_path_sans_ext(PrecipFiles[i])), 
                   start = 15, stop = nchar(PrecipFiles[i]))
  } else {
    Year = paste("20", Year, sep = "")
    Hour <- substr(file_path_sans_ext(file_path_sans_ext(PrecipFiles[i])), 
                   start = 13, stop = nchar(PrecipFiles[i]))
    
  }
  
  if (nchar(Hour) == 1) {
    Hour <- paste0(0, Hour)

  } else {
    Hour = Hour 
  }
  
  if (WRaster == FALSE) {
    Ras_i <- as(Ras_i, "SpatialGridDataFrame")
    write.asciigrid(Ras_i, 
                    fname = paste(outputpath, "3B42.", Year, ".", Hour,".ascii", 
                                  sep = ""), 
                    na.value = -9999)

  } else {
    writeRaster(Ras_i, 
                filename = paste(outputpath, "3B42.", Year, ".", Hour,".tif", 
                                 sep = ""), format = "GTiff",
                overwrite = TRUE)
  }
}

















