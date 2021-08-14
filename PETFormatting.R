# Remove previous object before running
rm(list=ls(all=TRUE))
library(tools)
library(ncdf4)
library(h5)
library(rgdal)
library(gdalUtils)
library(raster)
options(scipen=999)

# User Input
inputpath <- "C:/Users/Tri/Desktop/EF5/RawData/"
outputpath <- "C:/Users/Tri/Desktop/EF5/RawData/PET2/"
RasProjection <- "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs"
WRaster = FALSE




# No Change from Here
setwd(inputpath)
ZippedFolder <- list.files(path = inputpath, pattern = "\\.tar.gz$")



for (i in 1:length(ZippedFolder)) {
  untar(ZippedFolder[i])
  ZippedSubFolder <- list.files(path = paste(inputpath, 
                                             file_path_sans_ext(
                                               file_path_sans_ext(ZippedFolder[i])),
                                             sep = ""), 
                                pattern = "\\.tar.gz$")
  setwd(paste(inputpath, 
              file_path_sans_ext(file_path_sans_ext(ZippedFolder[i])),
              sep = ""))
  
  for (i in 1:length(ZippedSubFolder)) {
    cat("Processing File ", i , " of ",length(ZippedSubFolder), "\n")
    untar(ZippedSubFolder[i])
    Ras_i <- raster(paste(
      file_path_sans_ext(
        file_path_sans_ext(ZippedSubFolder[i])), ".bil", sep = ""))
    Ras_i = Ras_i /100
    if (WRaster == FALSE) {
      proj4string(Ras_i) <- CRS(RasProjection)
      Ras_i <- as(Ras_i, "SpatialGridDataFrame")
      write.asciigrid(Ras_i, 
                      fname = paste(outputpath, "PET.20", substr(file_path_sans_ext(
                        file_path_sans_ext(ZippedSubFolder[i])), 
                        start = 3, 
                        stop = 8), ".ascii", sep = ""), 
                      na.value = -9999)
    } else {
      proj4string(Ras_i) <- CRS(RasProjection)
      writeRaster(Ras_i, 
                  filename = paste(outputpath, "PET.20", substr(file_path_sans_ext(
                    file_path_sans_ext(ZippedSubFolder[i])), 
                    start = 3, 
                    stop = 8), ".tif", sep = ""), 
                  format="GTiff",
                  overwrite=TRUE)
    }
  }
  setwd(inputpath)
}






# for (i in 1:length(ZippedSubFolder)) {
#   untar(ZippedSubFolder[i])
#   Ras_i <- raster(paste(
#     file_path_sans_ext(
#       file_path_sans_ext(ZippedSubFolder[i])), ".bil", sep = ""))
#   if (WRaster == FALSE) {
#     Ras_i <- as(Ras_i, "SpatialGridDataFrame")
#     write.asciigrid(Ras_i, 
#                     fname = paste(outputpath, "pet.", substr(file_path_sans_ext(
#                       file_path_sans_ext(ZippedSubFolder[i])), 
#                       start = 3, 
#                       stop = 8), ".ascii", sep = ""), na.value = -9999)
#   } else {
#     proj4string(Ras_i) <- CRS(RasProjection)
#     writeRaster(Ras_i, 
#                 filename = paste(outputpath, "PET.", substr(file_path_sans_ext(
#                   file_path_sans_ext(ZippedSubFolder[i])), 
#                   start = 3, 
#                   stop = 8), ".tif", sep = ""))
#   }
# }






