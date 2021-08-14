################################################################################
# Genral Setting
################################################################################
library("plot3D")
library(EBImage)
library(animation)
library(magick)
library(png)
library(stringr)
inputpath = "C:/Users/pham2974/Desktop/PNG_Plots_Dry/"
setwd(inputpath)

################################################################################
# Reading files
################################################################################
Kljun_File = "calc_footprint_FFP_climatology.R"
Tower_File = "dry.csv"
data = read.csv(paste(inputpath, Tower_File, sep = ""))  


################################################################################
# Dry Flux Footprint
################################################################################
# dry_date <- data[,12]
# dry_winddir <- data[,16]
# dry_windspeed <- data[,17]
# dry_fricvelo <- data[,15]
# dry_obukhov <- data[,18]
# dry_boundaryheight <- data[,19]
# dry_std <- data[,20]

dry_date <- data[,1]
dry_winddir <- data[,5]
dry_windspeed <- data[,6]
dry_fricvelo <- data[,4]
dry_obukhov <- data[,7]
dry_boundaryheight <- data[,8]
dry_std <- data[,9]







################################################################################
# Running the Footprint function script
################################################################################

source(file.path(inputpath,"calc_footprint_FFP_climatology.R"))

################################################################################
# For Wet Period
################################################################################

for (x in 1:length(dry_winddir)) {
  dry_Fetch <- calc_footprint_FFP_climatology(zm = 60, z0 = 0.01, umean = NA,
                                               h = dry_boundaryheight[x],
                                               ol = dry_obukhov[x], 
                                               sigmav = dry_std[x],
                                               ustar = dry_fricvelo[x],
                                               wind_dir = dry_winddir[x],
                                               domain = c(-2000,2000,
                                                          -2000,2000),
                                               nx = 1100,
                                               smooth_data = 1)
  png(paste0(inputpath,str_pad(x, 3, pad = "0"),".png"))
  image.plot(dry_Fetch$x_2d[1,], dry_Fetch$y_2d[,1], dry_Fetch$fclim_2d,
             xlab = "X-Distance (m)", ylab = "Y-Distance (m)",
             main = paste(dry_date[x]))
  for (i in 1:8) lines(dry_Fetch$xr[[i]], dry_Fetch$yr[[i]], 
                       type="l", col="red")
  dev.off()
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
image_write(Footprint_Animate, paste0("dry_Footprint.gif"))

################################################################################
################################################################################
################################################################################


























