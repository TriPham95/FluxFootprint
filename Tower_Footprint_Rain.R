################################################################################
# Genral Setting
################################################################################
library("plot3D")
library(EBImage)
library(animation)
library(magick)
library(png)
library(stringr)
inputpath = "C:/Users/pham2974/Desktop/PNG_Plots/"
setwd(inputpath)

################################################################################
# Reading files
################################################################################
Kljun_File = "calc_footprint_FFP_climatology.R"
Tower_File = "FootprintTrial.csv"
data = read.csv(paste(inputpath, Tower_File, sep = ""))  

################################################################################
# Wet Flux Footprint
################################################################################
rain_date <- data[1:21,1]
rain_winddir <- data[1:21,4]
rain_windspeed <- data[1:21,5]
rain_fricvelo <- data[1:21,6]
rain_obukhov <- data[1:21,7]
rain_boundaryheight <- data[1:21,8]
rain_std <- data[1:21,9]
# rain_date <- data[1:5,1]
# rain_winddir <- data[1:5,4]
# rain_windspeed <- data[1:5,5]
# rain_fricvelo <- data[1:5,6]
# rain_obukhov <- data[1:5,7]
# rain_boundaryheight <- data[1:5,8]
# rain_std <- data[1:5,9]

################################################################################
# Dry Flux Footprint
################################################################################

dry_winddir <- data[,16]
dry_windspeed <- data[,17]
dry_fricvelo <- data[,15]
dry_obukhov <- data[,18]
dry_boundaryheight <- data[,19]
dry_std <- data[,20]

################################################################################
# Running the Footprint function script
################################################################################

source(file.path(inputpath,"calc_footprint_FFP_climatology.R"))

################################################################################
# For Wet Period
################################################################################

for (x in 1:length(rain_winddir)) {
  Rain_Fetch <- calc_footprint_FFP_climatology(zm = 60, z0 = 0.01, umean = NA,
                                               h = rain_boundaryheight[x],
                                               ol = rain_obukhov[x], 
                                               sigmav = rain_std[x],
                                               ustar = rain_fricvelo[x],
                                               wind_dir = rain_winddir[x],
                                               domain = c(-2000,2000,
                                                          -2000,2000),
                                               nx = 1100,
                                               smooth_data = 1)
  png(paste0(inputpath,str_pad(x, 3, pad = "0"),".png"))
  image.plot(Rain_Fetch$x_2d[1,], Rain_Fetch$y_2d[,1], Rain_Fetch$fclim_2d,
             xlab = "X-Distance (m)", ylab = "Y-Distance (m)",
             main = paste(rain_date[x]))
  for (i in 1:8) lines(Rain_Fetch$xr[[i]], Rain_Fetch$yr[[i]], 
                       type="l", col="red")
}

################################################################################
# Turn off all dev devices
################################################################################
while (!is.null(dev.list()))  dev.off()

################################################################################
# Read the plotted .png
################################################################################

png_name <- list.files(inputpath, "*.png", full.names = TRUE)
Combined_Footprint_PNG <- c()
for (i in png_name) {
  png_dat <- image_read(i)
  Combined_Footprint_PNG <- append(Combined_Footprint_PNG, png_dat)
}

################################################################################
# Animate the list
################################################################################

Combined_Footprint_PNG_Scale <- image_scale(Combined_Footprint_PNG)
Footprint_Animate <- image_animate(Combined_Footprint_PNG_Scale, fps = 2, 
                                   dispose = "previous")
image_write(Footprint_Animate, paste0("Rain_Footprint.gif"))

################################################################################
################################################################################
################################################################################















# Rain_Fetch <- calc_footprint_FFP_climatology(zm = 60, z0 = 0.01, umean = NA,
#                                              h = rain_boundaryheight,
#                                              ol = rain_obukhov, sigmav = rain_std,
#                                              ustar = rain_fricvelo,
#                                              wind_dir = rain_winddir,
#                                              domain = c(-1500,1500,-1500,1500),
#                                              nx = 1100,
#                                              smooth_data = 1)

# 
# image.plot(Rain_Fetch$x_2d[1,], Rain_Fetch$y_2d[,1], Rain_Fetch$fclim_2d,
#            xlab = "Distance (m)", ylab = "Distance (m)")
# for (i in 1:8) lines(Rain_Fetch$xr[[i]], Rain_Fetch$yr[[i]], type="l", col="red")









































































# For Dry Period
# Dry_Fetch <- calc_footprint_FFP_climatology(zm = 60, z0 = 0.01, umean = NA,
#                                              h = dry_boundaryheight,
#                                              ol = dry_obukhov, sigmav = dry_std,
#                                              ustar = dry_fricvelo,
#                                              wind_dir = dry_winddir,
#                                              domain = c(-1500,1500,-1500,1500),
#                                              nx = 1100,
#                                              smooth_data = 1)
# 
# 
# 
# 
# image.plot(Dry_Fetch$x_2d[1,], Dry_Fetch$y_2d[,1], Dry_Fetch$fclim_2d,
#            xlab = "Distance (m)", ylab = "Distance (m)")
# for (i in 1:8) lines(Dry_Fetch$xr[[i]], Dry_Fetch$yr[[i]], type="l", col="red")















