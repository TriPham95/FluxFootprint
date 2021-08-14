# Remove previous object before running
rm(list=ls(all=TRUE))
library(ncdf4) 
library(raster) 
library(rgdal)
library(tools)
options(scipen=999)


inputpath <- "C:/Users/Tri/Desktop/EF5/TRMMNetCDF/"
outputpath <- "C:/Users/Tri/Desktop/EF5/NetCDFFormatted/"
setwd("C:/Users/Tri/Desktop/EF5/RawData/")
WRaster = TRUE

NetCDFFiles <- list.files(inputpath, pattern = "\\.nc4$")


for (i in 1:length(NetCDFFiles)) {
  cat("Processing File ", i, " of ", length(NetCDFFiles), "\n")
  nc_data <- nc_open(paste(inputpath, NetCDFFiles[i], sep = ""))
  lon <- ncvar_get(nc_data, "lon")
  lat <- ncvar_get(nc_data, "lat", verbose = F)
  
  PrecipData <- ncvar_get(nc_data, "precipitation")
  
  fillvalue <- ncatt_get(nc_data, "precipitation", "_FillValue")
  
  nc_close(nc_data) 
  
  PrecipData[PrecipData == fillvalue$value] <- NA
  
  Ras <- raster(t(PrecipData), 
              xmn=min(lon), 
              xmx=max(lon), 
              ymn=min(lat), 
              ymx=max(lat), 
              crs=CRS("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0"))
  Ras <- flip(Ras, direction='y')
  if (WRaster == FALSE) {
    # Ras <- as(Ras, "SpatialGridDataFrame")
    writeRaster(Ras, 
                filename = paste(outputpath, 
                                  file_path_sans_ext(file_path_sans_ext(NetCDFFiles[i])),
                                  ".ascii", 
                                  sep = ""), format = "ascii",
                overwrite = TRUE)
    
  } else {
    writeRaster(Ras, 
                filename = paste(outputpath, 
                                 file_path_sans_ext(file_path_sans_ext(NetCDFFiles[i])),
                                 ".tif", 
                                 sep = ""), format = "GTiff",
                overwrite = TRUE)
    
  }
  
  
  
}






