################################################################################
# Calculate Seasonal Footprint (Footprint Climatology) for US-Src Tower        #
# Simulation Period from 2008 - 2010                                           #
################################################################################
################################################################################
# Genral Setting
################################################################################
library("plot3D")
library(EBImage)
library(animation)
library(magick)
library(openair)
library(foreach)
library(parallel)
library(doParallel)
inputpath = "/home/tpham/Documents/Flux Footprint/FluxFootprint2019/"
setwd(inputpath)
options(scipen = 999)
################################################################################
# Reading files                                                                #      
################################################################################
Kljun_File = "calc_footprint_FFP_climatology.R"
Tower_File = "USSrm.csv"
source(Kljun_File)
data = read.csv(paste(inputpath, Tower_File, sep = ""), skip = 2)  
################################################################################
# Reading Data from File                                                       #
################################################################################
Time_Start <- data[,1] # Start recording time
Time_End <- data[,2] # End recording time
USTAR <- data[,"USTAR"] # Frictional Velocity in m/s
WINDDIRECTION <- data[,"WD_1_1_1"] # Wind Direction in Decimal Degree from 0 to 360
WINDSPEED <- data[,"WS_1_1_1"] # Wind Speed in m/s
SENSIBLEHEATFLUX <- data[,"H"] # Sensible Heat Flux in W/m^2
AIRTEMP <- data[,"TA_1_1_1"] # Air Temperature in C

ATMPRESSURE <- data[,"PA"] # Atmospheric Pressure in kPa
LATENTHEATFLUX <- data[,"LE"] # Latent Heat Flux in W/m^2
################################################################################
# Format Timestamp in .csv File to more easily Readable Format                 #
################################################################################
Timestamp_Start <- format(strptime(Time_Start, format = "%Y%m%d%H%M"), 
                          format = "%m/%d/%Y %H:%M")

Timestamp_End <- format(strptime(Time_End, format = "%Y%m%d%H%M"), 
                        format = "%m/%d/%Y %H:%M")
################################################################################
# Identify Index during Period 2008 - 2010                                     #
################################################################################
Index_Start <- which(Time_Start == "200401010000")
Index_End <- which(Time_Start == "201412312330")
################################################################################
# Get the data for period of 2008 to 2010                                      #
################################################################################
timestart <- Timestamp_Start[Index_Start:Index_End]
timeend <- Timestamp_End[Index_Start:Index_End]
ustar <- USTAR[Index_Start:Index_End]
winddir <- WINDDIRECTION[Index_Start:Index_End]
windspeed <- WINDSPEED[Index_Start:Index_End]
Hsenflux <- SENSIBLEHEATFLUX[Index_Start:Index_End]
Latentflux <- LATENTHEATFLUX[Index_Start:Index_End]
AirTemp <- AIRTEMP[Index_Start:Index_End]
AtmPressure <- ATMPRESSURE[Index_Start:Index_End]
################################################################################
# Create the Data Frame                                                        #
################################################################################
Flux20042014 <- data.frame(start <- timestart,
                           end <- timeend,
                           fric_vel <- ustar,
                           windir <- winddir,
                           windspd <- windspeed,
                           H <- Hsenflux,
                           LE <- Latentflux,
                           TA <- AirTemp,
                           AirPressure <- AtmPressure)
colnames(Flux20042014) <- c("Start", "End", "FricVel", "WindDir", "WindSpd", 
                            "SenFlux", "LatentFlux", "AirTemp", "AtmPressure")
################################################################################
# Remove All Rows with No Data (i.e -9999)                                     #
################################################################################
Flux20042014[Flux20042014 == -9999] <- NA
Flux20042014$FricVel[Flux20042014$FricVel == 0] <- NA
Flux20042014_Filtered <- na.omit(Flux20042014)
cat("Percent of Data Removed:", 
    (nrow(Flux20042014)-nrow(Flux20042014_Filtered)) / nrow(Flux20042014)*100, 
    "%")
################################################################################
# Need to Calculate the following Parameters                                   #
################################################################################
# zm       = Measurement height above displacement height                      #   
#            usually a scalar, but can also be a vector                        #
# z0       = Roughness length [m] - enter [NaN] if not known                   #
#            usually a scalar, but can also be a vector                        #
# h        = Vector of boundary layer height [m]                               #
# ol       = Vector of Obukhov length [m]                                      #
# sigmav   = Vector of standard deviation of lateral velocity                  #
#            fluctuations [ms-1]                                               #
################################################################################
# Measurement Height in meters
hmeas = 6.4
# Vegetation Height in m
zveg = 2.5
# von Karman Coefficient
k = 0.41
# Gravitational Acceleration
g = 9.81
# Specific Heat Capacity of Air at Constant Pressure in Jkg-1K-1
Cp = 1008 
# Air Density in kg/m^3
pa = 1.184 
# Reference Atmospheric Pressure in kPa
Po = 100
# Measurement Height Above the Displacement Height
zm = hmeas - 2/3*zveg
# Calculate the Coriolis Parameter
OMEGA <- 7.292115 * 10^-5 # Angular Velocity of the Earth in rad/s
PHI <- 31.8214 # Latitude of Santa Rita, AZ
# Coriolis Parameter in sec-1
f <- 2 * OMEGA * sin(PHI*3.14159265359/180)
################################################################################
# Roughness Length z0 in m                                                     #           
################################################################################
# Surface roughness length is calculated from the logarithmic relationship     #  
# V(z) = USTAR/k*ln((z-d)/z0)                                                  #
# Where:                                                                       #
# V(z) is wind speed function of height                                        #
# USTAR is frictional velocity                                                 #
# k is von Karman coefficient                                                  #
# d is zero plane displacement height                                          #
# z is height above ground surface                                             #
# z0 is surface roughness length                                               #
################################################################################
################################################################################
# Function to Calculate Virtual Temperature                                    #
################################################################################
# Calculate the Partial Pressure of Moist Air                                  #
################################################################################
MoistPressure <- function() {
  e <- NULL
  for (i in 1:nrow(Flux20042014_Filtered)) {
    # Moist Pressure in kPa
    moistpressure = (4.77 * (10^-3)) * (461.51) * (AirTemp[i] + 273.15) / 1000
    e <- c(e, moistpressure)
  }
  return(e)
}
# Moist Partial Pressure in kPa
e <- MoistPressure()
################################################################################
# Calculate the Partial Pressure of Dry Air                                    #
################################################################################
DryPressure <- function() {
  p <- NULL
  for (i in 1:nrow(Flux20042014_Filtered)) {
    # Dry Pressure in kPa
    drypressure <- AtmPressure[i] - e[i]
    p <- c(p, drypressure)
  }
  return(p)
}
# Dry Partial Pressure in kPa
p <- DryPressure()
################################################################################
# Calculate the Virtual Temperature                                            #
################################################################################
VirtualTemp <- function() {
  Tv <- NULL
  for (i in 1:nrow(Flux20042014_Filtered)) {
    # Virtual Temp in C
    virtualtemperature <- (AirTemp[i] + 273.15) / 
      (1 - e[i]/p[i] * (1- 0.622)) - 273.15
    Tv <- c(Tv, virtualtemperature)
  }
  return(Tv)
}
Tv <- VirtualTemp()
################################################################################
# Add Virtual Temperature Column to the Data Frame                             #
################################################################################
Flux20042014_Filtered[, "VirtualTemp"] <- Tv
# Zero Plane Displacement Height in mis estimated as 2/3 vegetation height
d = (2/3)*zveg
################################################################################
# Function to Calculate roughness length                                       #
# Assumed to be 1/10 of zveg                                                   #
################################################################################
roughness <- function() {
  roughness <- NULL
  for (i in 1: nrow((Flux20042014_Filtered))) {
    z0 = (1/10) * zveg
    roughness <- c(roughness, z0) 
  }
  return(roughness)
}
z0 <- roughness()

################################################################################
# Add Roughness Lengh to the Data Frame                                        #
################################################################################
Flux20042014_Filtered[, "RouHeight"] <- z0
################################################################################
# Obukhov Length is calculated from the relationship                           #
# L = -(ustar^3*cp*T*p)/(kgH)                                                  #
# Where                                                                        #
# L is Obukhov Length                                                          #
# ustar is frictional velocity                                                 #
# cp is specific heat of air at constant pressure                              #
# T is Virtual Temperature                                                     #
# p is density of air                                                          #
# k is von Karman coefficient                                                  #
# g is gravitational acceleration                                              #
# H is sensible heat flux                                                      #
################################################################################
ObukhovLength <- function() {
  Obukhov <- NULL
  for (i in 1: nrow((Flux20042014_Filtered))) {
    
    oL = -((Flux20042014_Filtered$FricVel[i]^3) * 
             (Flux20042014_Filtered$VirtualTemp[i] + 273.15)) / 
      (k*g*Flux20042014_Filtered$SenFlux[i]/(Cp*pa))
    
    Obukhov <- c(Obukhov, oL) 
  }
  return(Obukhov)
}
oL <- ObukhovLength()
################################################################################
# Add Obukhov Length Column to the Data Frame                                  #
################################################################################
Flux20042014_Filtered[, "Obukhov"] <- oL

################################################################################
# Calculate Potential Temperature                                              #
################################################################################
PotentialTemp <- function() {
  Tp <- NULL
  for (i in 1:nrow(Flux20042014_Filtered)) {
    # Potential Temperature in C
    potentialtemp = (Flux20042014_Filtered$AirTemp[i] + 273.15) * 
      (Po / Flux20042014_Filtered$AtmPressure[i])^0.286 - 273.15
    Tp <- c(Tp, potentialtemp)
  }
  return(Tp)
}
Tp <- PotentialTemp()
################################################################################
# Add Potential Temp Column to the Data Frame                                  #
################################################################################
Flux20042014_Filtered[, "PotentialTemp"] <- Tp
################################################################################
# Vector of boundary layer height                                              #
################################################################################
BoundaryLayerHeight <- function() {
  H <- NULL
  A = 0.2 # Coefficient
  B = 2.5 # Coefficient
  C = 8 # Coefficient
  cn = 0.3 # Coefficient
  gamma <- 0.01 # Potential Temperature Gradient in K/m
  # von Karman Coefficient
  k = 0.41
  # Gravitational Acceleration
  g = 9.81
  # Specific Heat Capacity of Air at Constant Pressure in Jkg-1K-1
  Cp = 1008 
  # Air Density in kg/m^3
  pa = 1.184 
  dhdt <- NULL
  for (i in 1:nrow(Flux20042014_Filtered)) {
    if (Flux20042014_Filtered$Obukhov[i] >= 0 & 
        Flux20042014_Filtered$Obukhov[i] <= 1000) { # For Neutral, 
      # Stable Condition
      boundaryheight = (Flux20042014_Filtered$Obukhov[i] / 
                          3.8) * 
        (-1 + (1 + 2.28*Flux20042014_Filtered$FricVel[i] / 
                 (f*Flux20042014_Filtered$Obukhov[i]))^(1/2))
      H <- c(H, boundaryheight)
    } else if (Flux20042014_Filtered$Obukhov[i] > 1000) {
      boundaryheight = cn * Flux20042014_Filtered$FricVel[i] / abs(f)
      H <- c(H, boundaryheight)
    }  else { # Convective Condition
      if (i > 1) {
        dhdt <- ((Flux20042014_Filtered$SenFlux[i-1]/(Cp*pa)) / gamma * 
                   ((H[i-1]^2) / ((1 + 2*A) * H[i-1] - 
                                    2*B*k*Flux20042014_Filtered$Obukhov[i-1]) + 
                      ((C*Flux20042014_Filtered$FricVel[i-1]^2*
                          (Flux20042014_Filtered$AirTemp[i-1] + 273.15)) /
                         (gamma*g*((1+A)*H[i-1] - 
                                     B*k*Flux20042014_Filtered$Obukhov[i-1]))))^-1)
        
        boundaryheight = H[i-1] + dhdt
        H <- c(H, boundaryheight)
      } else { 
        boundaryheight = (Flux20042014_Filtered$Obukhov[i] / 3.8) * 
          (-1 + (1 + 2.28 * Flux20042014_Filtered$FricVel[i] / 
                   (f * Flux20042014_Filtered$Obukhov[i]))^(1/2))
        H <- c(H, boundaryheight)
      }
    }
  }
  return(H) 
}
H <- BoundaryLayerHeight()
################################################################################
# Add Boundary Layer Height Column to the Data Frame                           #
################################################################################
Flux20042014_Filtered[, "BLH"] <- H
################################################################################
# Vector of standard deviation of lateral velocity fluctuations [ms-1]         #
################################################################################
StdLateralVelocity <- function() {
  StdV <- NULL
  FLUCTUATION <- NULL
  Vmean <- mean(Flux20042014_Filtered$WindSpd)
  for (i in 1:nrow(Flux20042014_Filtered)) {
    fluctuation = Vmean - Flux20042014_Filtered$WindSpd[i]
    FLUCTUATION <- c(FLUCTUATION, fluctuation)
    RMS_w = sqrt(sum(FLUCTUATION^2) / i)
    StdV <- c(StdV, RMS_w)
  }
  return(StdV)
}
sigmav <- StdLateralVelocity()
################################################################################
# Add Standard Deviation of Lateral Velocity Column to the Data Frame          #
################################################################################
Flux20042014_Filtered[, "SigmaV"] <- sigmav
################################################################################
# Fixing Wind Direction                                                        #
################################################################################
for (i in 1:nrow(Flux20042014_Filtered)) {
  if (Flux20042014_Filtered$WindDir[i] > 360) {
    Flux20042014_Filtered$WindDir[i] <- Flux20042014_Filtered$WindDir[i] - 360
  } 
}
################################################################################
# Remove Nan Row                                                               #
################################################################################
Flux20042014_Filtered <- na.omit(Flux20042014_Filtered)
Flux20042014_Filtered <- Flux20042014_Filtered[-which(
  zm/Flux20042014_Filtered$Obukhov < -15.5),]
Flux20042014_Filtered <- Flux20042014_Filtered[-which(
  Flux20042014_Filtered$BLH < 10),]
# Flux20042014_Filtered1 <- Flux20042014_Filtered[-which(
#   Flux20042014_Filtered$BLH < zm),]
# Flux20042014_Filtered = Flux20042014_Filtered1




z0_2008 <- Flux20042014_Filtered$RouHeight
umean_2008 <- Flux20042014_Filtered$WindSpd
h_2008 <- Flux20042014_Filtered$BLH
ol_2008 <- Flux20042014_Filtered$Obukhov
sigmav_2008 <- Flux20042014_Filtered$SigmaV
ustar_2008 <- Flux20042014_Filtered$FricVel
winddir_2008 <- Flux20042014_Filtered$WindDir
domain_2008 = c(-1000,1000,-1000,1000)
dx_2008 = 2 # 1 m resolution
nx_2008 = 1100


FFP_0414_Srm <- calc_footprint_FFP_climatology(zm = zm,
                                               z0 = z0_2008,
                                               umean = umean_2008,
                                               h = h_2008,
                                               ol = ol_2008,
                                               sigmav = sigmav_2008,
                                               ustar = ustar_2008,
                                               wind_dir = winddir_2008,
                                               r = seq(10,80,10),
                                               domain = domain_2008,
                                               nx = nx_2008,
                                               dx = dx_2008,
                                               smooth_data = 0,
                                               rslayer = 1)



options(scipen = 0)
image.plot(FFP_0414_Srm$x_2d[1,],
           FFP_0414_Srm$y_2d[,1],
           FFP_0414_Srm$fclim_2d,
           xlim = c(-150,150),
           ylim = c(-150,150),
           xlab = "x Distance (m)",
           ylab = "y Distance (m)",
           horizontal = FALSE,
           legend.args = list(text = expression("f" ~ (m^{-2})), side = 2))
for (i in 1:8) lines(FFP_0414_Srm$xr[[i]], 
                     FFP_0414_Srm$yr[[i]], 
                     type="l", 
                     col="red")
points(0,0, col = "black", pch = 19, cex = 2)





























################################################################################
# Spring from March 21 to June 21                                              #
# Summer from June 21 to September 21                                          #
# Fall from September 21 to December 21                                        #
# Winter from December 21 to March 21                                          #
################################################################################
# Calculate the Climatological Footprint                                       #
################################################################################
# Spring from March 21, 2009 to June 21, 2009                                  #
################################################################################
Start_Spring2009 <- which(Flux20042014_Filtered$Start == "03/23/2009 00:00")
End_Spring2009 <- which(Flux20042014_Filtered$Start == "06/20/2009 23:30")
z0_Sp2009 <- Flux20042014_Filtered$RouHeight[Start_Spring2009:End_Spring2009]
umean_Sp2009 <- Flux20042014_Filtered$WindSpd[Start_Spring2009:End_Spring2009]
h_Sp2009 <- Flux20042014_Filtered$BLH[Start_Spring2009:End_Spring2009]
ol_Sp2009 <- Flux20042014_Filtered$Obukhov[Start_Spring2009:End_Spring2009]
sigmav_Sp2009 <- Flux20042014_Filtered$SigmaV[Start_Spring2009:End_Spring2009]
ustar_Sp2009 <- Flux20042014_Filtered$FricVel[Start_Spring2009:End_Spring2009]
winddir_Sp2009 <- Flux20042014_Filtered$WindDir[Start_Spring2009:End_Spring2009]
domain_Sp2009 = c(-1000,1000,-1000,1000)
dx_Sp2009 = 2 # 1 m resolution
nx_Sp2009 = 1100
################################################################################
# Summer from June 21 to September 21                                          #
################################################################################
Start_Summer2009 <- which(Flux20042014_Filtered$Start == "06/21/2009 00:00")
End_Summer2009 <- which(Flux20042014_Filtered$Start == "09/20/2009 23:30")
z0_Su2009 <- Flux20042014_Filtered$RouHeight[Start_Summer2009:End_Summer2009]
umean_Su2009 <- Flux20042014_Filtered$WindSpd[Start_Summer2009:End_Summer2009]
h_Su2009 <- Flux20042014_Filtered$BLH[Start_Summer2009:End_Summer2009]
ol_Su2009 <- Flux20042014_Filtered$Obukhov[Start_Summer2009:End_Summer2009]
sigmav_Su2009 <- Flux20042014_Filtered$SigmaV[Start_Summer2009:End_Summer2009]
ustar_Su2009 <- Flux20042014_Filtered$FricVel[Start_Summer2009:End_Summer2009]
winddir_Su2009 <- Flux20042014_Filtered$WindDir[Start_Summer2009:End_Summer2009]
domain_Su2009 = c(-1000,1000,-1000,1000)
dx_Su2009 = 2 # 1 m resolution
nx_Su2009 = 1100
################################################################################
# Fall from September 21 to December 21                                        #
################################################################################
Start_Fall2009 <- which(Flux20042014_Filtered$Start == "09/21/2009 00:00")
End_Fall2009 <- which(Flux20042014_Filtered$Start == "12/20/2009 23:30")
z0_Fa2009 <- Flux20042014_Filtered$RouHeight[Start_Fall2009:End_Fall2009]
umean_Fa2009 <- Flux20042014_Filtered$WindSpd[Start_Fall2009:End_Fall2009]
h_Fa2009 <- Flux20042014_Filtered$BLH[Start_Fall2009:End_Fall2009]
ol_Fa2009 <- Flux20042014_Filtered$Obukhov[Start_Fall2009:End_Fall2009]
sigmav_Fa2009 <- Flux20042014_Filtered$SigmaV[Start_Fall2009:End_Fall2009]
ustar_Fa2009 <- Flux20042014_Filtered$FricVel[Start_Fall2009:End_Fall2009]
winddir_Fa2009 <- Flux20042014_Filtered$WindDir[Start_Fall2009:End_Fall2009]
domain_Fa2009 = c(-1000,1000,-1000,1000)
dx_Fa2009 = 2 # 1 m resolution
nx_Fa2009 = 1100
################################################################################
# Winter from December 21 to March 21                                          #
################################################################################
Start_Winter2009 <- which(Flux20042014_Filtered$Start == "12/21/2009 00:00")
End_Winter2009 <- which(Flux20042014_Filtered$Start == "03/19/2010 23:30")
z0_Win2009 <- Flux20042014_Filtered$RouHeight[Start_Winter2009:End_Winter2009]
umean_Win2009 <- Flux20042014_Filtered$WindSpd[Start_Winter2009:End_Winter2009]
h_Win2009 <- Flux20042014_Filtered$BLH[Start_Winter2009:End_Winter2009]
ol_Win2009 <- Flux20042014_Filtered$Obukhov[Start_Winter2009:End_Winter2009]
sigmav_Win2009 <- Flux20042014_Filtered$SigmaV[Start_Winter2009:End_Winter2009]
ustar_Win2009 <- Flux20042014_Filtered$FricVel[Start_Winter2009:End_Winter2009]
winddir_Win2009 <- Flux20042014_Filtered$WindDir[Start_Winter2009:End_Winter2009]
domain_Win2009 = c(-1000,1000,-1000,1000)
dx_Win2009 = 2 # 1 m resolution
nx_Win2009 = 1100

start_time_singlecore <- Sys.time()

################################################################################
# Calculate the Climatological Footprint for Spring 2009                       #
################################################################################
FFP_Sp2009 <- calc_footprint_FFP_climatology(zm = zm,
                                             z0 = z0_Sp2009,
                                             umean = umean_Sp2009,
                                             h = h_Sp2009,
                                             ol = ol_Sp2009,
                                             sigmav = sigmav_Sp2009,
                                             ustar = ustar_Sp2009,
                                             wind_dir = winddir_Sp2009,
                                             r = seq(10,80,10),
                                             domain = domain_Sp2009,
                                             nx = nx_Sp2009,
                                             dx = dx_Sp2009,
                                             smooth_data = 0,
                                             rslayer = 1)

windRose(Flux20042014_Filtered[Start_Spring2009:End_Spring2009,], 
         ws = "WindSpd",
         wd = "WindDir", 
         breaks = c(0,2,4,6,8,10,12,14,16), 
         width = 2, 
         paddle = FALSE, 
         annotate = FALSE,
         key.position = "right",
         cols = "jet",
         grid.line = 5, 
         max.freq = 22, 
         cex = 1.5)

options(scipen = 0)
image.plot(FFP_Sp2009$x_2d[1,],
           FFP_Sp2009$y_2d[,1],
           FFP_Sp2009$fclim_2d,
           xlim = c(-100,100),
           ylim = c(-100,100),
           xlab = "Along Wind Distance (m)",
           ylab = "Cross Wind Distance (m)",
           horizontal = FALSE,
           legend.args = list(text = expression("f" ~ (m^{-2})), side = 2))
for (i in 1:8) lines(FFP_Sp2009$xr[[i]], 
                     FFP_Sp2009$yr[[i]], 
                     type="l", 
                     col="red")
points(0,0, col = "black", pch = 19, cex = 2)

plot(FFP_Sp2009$x_2d,FFP_Sp2009$fclim_2d, type="l",
     xaxs = "i",
     yaxs = "i",
     xlim = c(-100, 100),
     ylim = c(0, 0.0012),
     xlab = "Upwind Distance from the Instrument (m)",
     ylab = expression("f" ~ (m^{-2})),
     col = "darkgreen")
title("Flux Footprint at US-SRc from March 21, 2009 to June 21, 2009")
################################################################################
# Calculate the Climatological Footprint for Summer 2009                       #
################################################################################
FFP_Su2009 <- calc_footprint_FFP_climatology(zm = zm,
                                             z0 = z0_Su2009,
                                             umean = umean_Su2009,
                                             h = h_Su2009,
                                             ol = ol_Su2009,
                                             sigmav = sigmav_Su2009,
                                             ustar = ustar_Su2009,
                                             wind_dir = winddir_Su2009,
                                             domain = domain_Su2009,
                                             nx = nx_Su2009,
                                             r = seq(10,80,10),
                                             smooth_data = 0,
                                             rslayer = 1)
windRose(Flux20042014_Filtered[Start_Summer2009:End_Summer2009,], 
         ws = "WindSpd",
         wd = "WindDir", 
         breaks = c(0,2,4,6,8,10,12,14,16), 
         width = 2, 
         paddle = FALSE, 
         annotate = FALSE,
         key.position = "right",
         cols = "jet",
         grid.line = 5, max.freq = 22, cex = 1.5)

options(scipen = 0)
image.plot(FFP_Su2009$x_2d[1,],
           FFP_Su2009$y_2d[,1],
           FFP_Su2009$fclim_2d,
           xlim = c(-100,100),
           ylim = c(-100,100),
           xlab = "Along Wind Distance (m)",
           ylab = "Cross Wind Distance (m)",
           horizontal = FALSE,
           legend.args = list(text = expression("f" ~ (m^{-2})), side = 2))
for (i in 1:8) lines(FFP_Su2009$xr[[i]], 
                     FFP_Su2009$yr[[i]], 
                     type="l", 
                     col="red")
points(0,0, col = "black", pch = 19, cex = 2)

plot(FFP_Su2009$x_2d,FFP_Su2009$fclim_2d, type="l",
     xaxs = "i",
     yaxs = "i",
     xlim = c(-100, 100),
     ylim = c(0, 0.001),
     xlab = "Upwind Distance from the Instrument (m)",
     ylab = expression("f" ~ (m^{-2})),
     col = "darkgreen")
title("Flux Footprint at US-SRc from June 21, 2009 to September 21, 2009")
################################################################################
# Calculate the Climatological Footprint for Fall 2009                         #
################################################################################
FFP_Fa2009 <- calc_footprint_FFP_climatology(zm = zm,
                                             z0 = z0_Fa2009,
                                             umean = umean_Fa2009,
                                             h = h_Fa2009,
                                             ol = ol_Fa2009,
                                             sigmav = sigmav_Fa2009,
                                             ustar = ustar_Fa2009,
                                             wind_dir = winddir_Fa2009,
                                             r = seq(10,80,10),
                                             smooth_data = 0,
                                             rslayer = 1)
windRose(Flux20042014_Filtered[Start_Fall2009:End_Fall2009,], 
         ws = "WindSpd",
         wd = "WindDir", 
         breaks = c(0,2,4,6,8,10,12,14,16), 
         width = 2, 
         paddle = FALSE, 
         annotate = FALSE,
         key.position = "right",
         cols = "jet",
         grid.line = 5, max.freq = 35, cex = 1.5)

options(scipen = -1)
image.plot(FFP_Fa2009$x_2d[1,],
           FFP_Fa2009$y_2d[,1],
           FFP_Fa2009$fclim_2d,
           xlim = c(-100,100),
           ylim = c(-100,100),
           xlab = "Along Wind Distance (m)",
           ylab = "Cross Wind Distance (m)",
           horizontal = FALSE,
           legend.args = list(text = expression("f" ~ (m^{-2})), side = 2))
for (i in 1:8) lines(FFP_Fa2009$xr[[i]], 
                     FFP_Fa2009$yr[[i]], 
                     type="l", 
                     col="red")
points(0,0, col = "black", pch = 19, cex = 2)

plot(FFP_Fa2009$x_2d,FFP_Fa2009$fclim_2d, type="l",
     xaxs = "i",
     yaxs = "i",
     xlim = c(-100, 100),
     ylim = c(0, 0.001),
     xlab = "Upwind Distance from the Instrument (m)",
     ylab = expression("f" ~ (m^{-2})),
     col = "darkgreen")
title("Flux Footprint at US-SRc from September 21, 2009 to December 21, 2009")
################################################################################
# Calculate the Climatological Footprint for Winter 2009                       #
################################################################################
FFP_Win2009 <- calc_footprint_FFP_climatology(zm = zm,
                                              z0 = z0_Win2009,
                                              umean = umean_Win2009,
                                              h = h_Win2009,
                                              ol = ol_Win2009,
                                              sigmav = sigmav_Win2009,
                                              ustar = ustar_Win2009,
                                              wind_dir = winddir_Win2009,
                                              r = seq(10,80,10),
                                              smooth_data = 0,
                                              rslayer = 1)
windRose(Flux20042014_Filtered[Start_Winter2009:End_Winter2009,], 
         ws = "WindSpd",
         wd = "WindDir", 
         breaks = c(0,2,4,6,8,10,12,14,16), 
         width = 2, 
         paddle = FALSE, 
         annotate = FALSE,
         key.position = "right",
         cols = "jet",
         grid.line = 5, max.freq = 30, cex = 1.5)

options(scipen = -1)
image.plot(FFP_Win2009$x_2d[1,],
           FFP_Win2009$y_2d[,1],
           FFP_Win2009$fclim_2d,
           xlim = c(-100,100),
           ylim = c(-100,100),
           xlab = "Along Wind Distance (m)",
           ylab = "Cross Wind Distance (m)",
           horizontal = FALSE,
           legend.args = list(text = expression("f" ~ (m^{-2})), side = 2))
for (i in 1:8) lines(FFP_Win2009$xr[[i]], 
                     FFP_Win2009$yr[[i]], 
                     type="l", 
                     col="red")
points(0,0, col = "black", pch = 19, cex = 2)


plot(FFP_Win2009$x_2d,FFP_Win2009$fclim_2d, type="l",
     xaxs = "i",
     yaxs = "i",
     xlim = c(-100, 100),
     ylim = c(0, 0.001),
     xlab = "Upwind Distance from the Instrument (m)",
     ylab = expression("f" ~ (m^{-2})),
     col = "darkgreen")
title("Flux Footprint at US-Fuf from December 21, 2009 to March 21, 2010")

end_time_singlecore <- Sys.time()

start_time_singlecore - end_time_singlecore

################################################################################
# Running the Flux Footprint Simulation in Parallel                            #
# The simulation will run simultaneously using 4 cores, recommend for computer #
# with more than 8 cores                                                       #
################################################################################
# start_time_parallel <- Sys.time()
# # Checking the number of core
# No_Cores <- detectCores() - 4
# # Create the cluster of 4 cores
# cluster <- makeCluster(No_Cores)
# # Import all global variables and external functions to be used or evaluated
# clusterExport(cluster, c("calc_footprint_FFP_climatology", "checkinput_climat", 
#                          "zm", "z0_Sp2009", "umean_Sp2009", "h_Sp2009", 
#                          "ol_Sp2009", "sigmav_Sp2009", "ustar_Sp2009", 
#                          "winddir_Sp2009", "domain_Sp2009", "nx_Sp2009",
#                          "dx_Sp2009", "z0_Su2009", "umean_Su2009", "h_Su2009", 
#                          "ol_Su2009", "sigmav_Su2009", "ustar_Su2009", 
#                          "winddir_Su2009", "domain_Su2009", "nx_Su2009",
#                          "dx_Su2009", "z0_Fa2009", "umean_Fa2009", "h_Fa2009", 
#                          "ol_Fa2009", "sigmav_Fa2009", "ustar_Fa2009", 
#                          "winddir_Fa2009", "domain_Fa2009", "nx_Fa2009",
#                          "dx_Fa2009", "z0_Win2009", "umean_Win2009", "h_Win2009", 
#                          "ol_Win2009", "sigmav_Win2009", "ustar_Win2009", 
#                          "winddir_Win2009", "domain_Win2009", "nx_Win2009",
#                          "dx_Win2009"))
# # Generate sequence of core, in this case 4 cores
# cores <- seq_along(cluster)
# 
# # Start Evaluating the function simulataneously
# r <- clusterApply(cluster[cores], cores, function(core) {
#   if (core == 1) { # Core ID
#     # For spring 2009
#     FFP_Sp2009Par <- calc_footprint_FFP_climatology(zm = zm,
#                                                     z0 = z0_Sp2009,
#                                                     umean = umean_Sp2009,
#                                                     h = h_Sp2009,
#                                                     ol = ol_Sp2009,
#                                                     sigmav = sigmav_Sp2009,
#                                                     ustar = ustar_Sp2009,
#                                                     wind_dir = winddir_Sp2009,
#                                                     r = seq(10,80,10),
#                                                     domain = domain_Sp2009,
#                                                     nx = nx_Sp2009,
#                                                     dx = dx_Sp2009,
#                                                     smooth_data = 1)
#   } else if (core == 2) { # Core ID
#     # FOr Summer 2009
#     FFP_Su2009Par <- calc_footprint_FFP_climatology(zm = zm,
#                                                     z0 = z0_Su2009,
#                                                     umean = umean_Su2009,
#                                                     h = h_Su2009,
#                                                     ol = ol_Su2009,
#                                                     sigmav = sigmav_Su2009,
#                                                     ustar = ustar_Su2009,
#                                                     wind_dir = winddir_Su2009,
#                                                     domain = domain_Su2009,
#                                                     nx = nx_Su2009,
#                                                     r = seq(10,80,10),
#                                                     smooth_data = 1)
#   } else if (core == 3) { # Core ID
#     # For Fall 2009
#     FFP_Fa2009Par <- calc_footprint_FFP_climatology(zm = zm,
#                                                     z0 = z0_Fa2009,
#                                                     umean = umean_Fa2009,
#                                                     h = h_Fa2009,
#                                                     ol = ol_Fa2009,
#                                                     sigmav = sigmav_Fa2009,
#                                                     ustar = ustar_Fa2009,
#                                                     wind_dir = winddir_Fa2009,
#                                                     r = seq(10,80,10),
#                                                     smooth_data = 1)
#   } else if (core == 4) { # Core ID
#     # For Winter 2009
#     FFP_Win2009Par <- calc_footprint_FFP_climatology(zm = zm,
#                                                      z0 = z0_Win2009,
#                                                      umean = umean_Win2009,
#                                                      h = h_Win2009,
#                                                      ol = ol_Win2009,
#                                                      sigmav = sigmav_Win2009,
#                                                      ustar = ustar_Win2009,
#                                                      wind_dir = winddir_Win2009,
#                                                      r = seq(10,80,10),
#                                                      smooth_data = 1)
#   }
# })