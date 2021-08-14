################################################################################
# Calculate Seasonal Footprint (Footprint Climatology) for US-FuF Tower        #
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
Tower_File = "MOISSTFilled.csv"
source(Kljun_File)
data = read.csv(paste(inputpath, Tower_File, sep = ""), skip = 0)  
################################################################################
# Reading Data from File                                                       #
################################################################################
Time_Start <- data[,"TIMESTAMP"] # Start recording time
Time_End <- data[,"TIMESTAMP"] # End recording time
USTAR <- data[, "u_star"] # Frictional Velocity in m/s
WINDDIRECTION <- data[, "wnd_dir_compass"] # Wind Direction in Decimal Degree from 0 to 360
WINDSPEED <- data[, "wnd_spd"] # Wind Speed in m/s
SENSIBLEHEATFLUX <- data[,"Hs"] # Sensible Heat Flux in W/m^2
AIRTEMP <- data[, "Temp_C1_Avg"] # Air Temperature in C

ATMPRESSURE <- data[,"press_Avg"] # Atmospheric Pressure in kPa
LATENTHEATFLUX <- data[,"LE_wpl"] # Latent Heat Flux in W/m^2
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
Index_Start <- which(Time_Start == "201401010000")
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
Flux2014 <- data.frame(start <- timestart,
                           end <- timeend,
                           fric_vel <- ustar,
                           windir <- winddir,
                           windspd <- windspeed,
                           H <- Hsenflux,
                           LE <- Latentflux,
                           TA <- AirTemp,
                           AirPressure <- AtmPressure)
colnames(Flux2014) <- c("Start", "End", "FricVel", "WindDir", "WindSpd", 
                            "SenFlux", "LatentFlux", "AirTemp", "AtmPressure")
################################################################################
# Remove All Rows with No Data (i.e -9999)                                     #
################################################################################
Flux2014[Flux2014 == -9999] <- NA
Flux2014$FricVel[Flux2014$FricVel == 0] <- NA
Flux2014_Filtered <- na.omit(Flux2014)
cat("Percent of Data Removed:", 
    (nrow(Flux2014)-nrow(Flux2014_Filtered)) / nrow(Flux2014)*100, 
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
hmeas = 3
# Vegetation Height in m
zveg = 1.5
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
PHI <-  36.069  # Latitude of Marena, OK
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
  for (i in 1:nrow(Flux2014_Filtered)) {
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
  for (i in 1:nrow(Flux2014_Filtered)) {
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
  for (i in 1:nrow(Flux2014_Filtered)) {
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
Flux2014_Filtered[, "VirtualTemp"] <- Tv
# Zero Plane Displacement Height in mis estimated as 2/3 vegetation height
d = (2/3)*zveg
################################################################################
# Function to Calculate roughness length                                       #
# Assumed to be 1/10 of zveg                                                   #
################################################################################
roughness <- function() {
  roughness <- NULL
  for (i in 1: nrow((Flux2014_Filtered))) {
    z0 = (1/10) * zveg
    roughness <- c(roughness, z0) 
  }
  return(roughness)
}
z0 <- roughness()

################################################################################
# Add Roughness Lengh to the Data Frame                                        #
################################################################################
Flux2014_Filtered[, "RouHeight"] <- z0
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
  for (i in 1: nrow((Flux2014_Filtered))) {
    
    oL = -((Flux2014_Filtered$FricVel[i]^3) * 
             (Flux2014_Filtered$VirtualTemp[i] + 273.15)) / 
      (k*g*Flux2014_Filtered$SenFlux[i]/(Cp*pa))
    
    Obukhov <- c(Obukhov, oL) 
  }
  return(Obukhov)
}
oL <- ObukhovLength()
################################################################################
# Add Obukhov Length Column to the Data Frame                                  #
################################################################################
Flux2014_Filtered[, "Obukhov"] <- oL

################################################################################
# Calculate Potential Temperature                                              #
################################################################################
PotentialTemp <- function() {
  Tp <- NULL
  for (i in 1:nrow(Flux2014_Filtered)) {
    # Potential Temperature in C
    potentialtemp = (Flux2014_Filtered$AirTemp[i] + 273.15) * 
      (Po / Flux2014_Filtered$AtmPressure[i])^0.286 - 273.15
    Tp <- c(Tp, potentialtemp)
  }
  return(Tp)
}
Tp <- PotentialTemp()
################################################################################
# Add Potential Temp Column to the Data Frame                                  #
################################################################################
Flux2014_Filtered[, "PotentialTemp"] <- Tp
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
  for (i in 1:nrow(Flux2014_Filtered)) {
    if (!is.na(Flux2014_Filtered$Obukhov[i]) >= 0 & 
        !is.na(Flux2014_Filtered$Obukhov[i] <= 1000)) { # For Neutral, 
      # Stable Condition
      boundaryheight = (Flux2014_Filtered$Obukhov[i] / 
                          3.8) * 
        (-1 + (1 + 2.28*Flux2014_Filtered$FricVel[i] / 
                 (f*Flux2014_Filtered$Obukhov[i]))^(1/2))
      H <- c(H, boundaryheight)
    } else if (!is.na(Flux2014_Filtered$Obukhov[i]) > 1000) {
      boundaryheight = cn * Flux2014_Filtered$FricVel[i] / abs(f)
      H <- c(H, boundaryheight)
    }  else { # Convective Condition
      if (i > 1) {
        dhdt <- ((Flux2014_Filtered$SenFlux[i-1]/(Cp*pa)) / gamma * 
                   ((H[i-1]^2) / ((1 + 2*A) * H[i-1] - 
                                    2*B*k*Flux2014_Filtered$Obukhov[i-1]) + 
                      ((C*Flux2014_Filtered$FricVel[i-1]^2*
                          (Flux2014_Filtered$AirTemp[i-1] + 273.15)) /
                         (gamma*g*((1+A)*H[i-1] - 
                                     B*k*Flux2014_Filtered$Obukhov[i-1]))))^-1)
        
        boundaryheight = H[i-1] + dhdt
        H <- c(H, boundaryheight)
      } else { 
        boundaryheight = (Flux2014_Filtered$Obukhov[i] / 3.8) * 
          (-1 + (1 + 2.28 * Flux2014_Filtered$FricVel[i] / 
                   (f * Flux2014_Filtered$Obukhov[i]))^(1/2))
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
Flux2014_Filtered[, "BLH"] <- H
################################################################################
# Vector of standard deviation of lateral velocity fluctuations [ms-1]         #
################################################################################
StdLateralVelocity <- function() {
  StdV <- NULL
  FLUCTUATION <- NULL
  Vmean <- mean(Flux2014_Filtered$WindSpd)
  for (i in 1:nrow(Flux2014_Filtered)) {
    fluctuation = Vmean - Flux2014_Filtered$WindSpd[i]
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
Flux2014_Filtered[, "SigmaV"] <- sigmav
################################################################################
# Fixing Wind Direction                                                        #
################################################################################
for (i in 1:nrow(Flux2014_Filtered)) {
  if (Flux2014_Filtered$WindDir[i] > 360) {
    Flux2014_Filtered$WindDir[i] <- Flux2014_Filtered$WindDir[i] - 360
  } 
}
################################################################################
# Remove Nan Row                                                               #
################################################################################
Flux2014_Filtered <- na.omit(Flux2014_Filtered)
# Flux2014_Filtered <- Flux2014_Filtered[-which(
#   zm/Flux2014_Filtered$Obukhov < -15.5),]
# Flux2014_Filtered <- Flux2014_Filtered[-which(
#   Flux2014_Filtered$BLH < 10),]


z0_2014 <- Flux2014_Filtered$RouHeight
umean_2014 <- Flux2014_Filtered$WindSpd
h_2014 <- Flux2014_Filtered$BLH
ol_2014 <- Flux2014_Filtered$Obukhov
sigmav_2014 <- Flux2014_Filtered$SigmaV
ustar_2014 <- Flux2014_Filtered$FricVel
winddir_2014 <- Flux2014_Filtered$WindDir
domain_2014 = c(-1000,1000,-1000,1000)
dx_2014 = 2 # 1 m resolution
nx_2014 = 1100


FFP_2014_MOISST <- calc_footprint_FFP_climatology(zm = zm,
                                               z0 = z0_2014,
                                               umean = umean_2014,
                                               h = h_2014,
                                               ol = ol_2014,
                                               sigmav = sigmav_2014,
                                               ustar = ustar_2014,
                                               wind_dir = winddir_2014,
                                               r = seq(10,80,10),
                                               domain = domain_2014,
                                               nx = nx_2014,
                                               dx = dx_2014,
                                               smooth_data = 0,
                                               rslayer = 1)





























