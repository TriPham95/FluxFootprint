require(Metrics)
# setwd("D:\\EF5_training_short\\examples\\wangchu\\")
# dir.create("D:\\EF5_training_short\\examples\\wangchu\\LOL")
# shell.exec("D:\\EF5_training_short\\examples\\wangchu\\ef5_64.exe")
################################################################################
# Can be changed by the users                                                  #
################################################################################
# Output folder: Same as the EF5.exe file
outputpath = "C:/Users/Tri/Desktop/EF5/CherryCreekSimulation/"
# Name of the EF5.exe file
# EF5_name <- "ef5_64.exe"
# Name of the control file with extension 
controlfile_name = "control.txt"
# Moisture Plots. Either TRUE or FALSE, if FALSE, no moisture plot
Moisture_Plot = FALSE 
# Calibration Option. Either TRUE or FALSE, if FALSE, no auto-calibration
Calibration_Option = TRUE
calibration_task_name <- "CalibrateCherryCreek"
################################################################################
# Basic block                                                                  #
################################################################################
# In order c(DEM, DDM, FAM, PROJ, ESRIDDM, SelfFAM) separated by a comma
Basic_Param = c("basic/CCfilled6.tif", "basic/CCDir6.tif", "basic/CCAcc6.tif", 
                "geographic",
                "false", "true")
################################################################################
# PrecipForcing block                                                          #
################################################################################
# Name of PrecipForcing
PrecipForcing_name = "TRMM"
# In order of c(TYPE, UNIT, FREQ, LOC, NAME) separated by a comma
PrecipForcing_params = c("ASC", "mm/h", "3h", "precip/", "3B42.YYYYMMDD.HH.ascii")
################################################################################
# PETForcing block                                                             #
################################################################################
# Name of PETForcing
PETForcing_name = "FEWSNET"
# In order of c(TYPE, UNIT, FREQ, LOC, NAME) separated by a comma
PETForcing_params = c("ASC", "mm/d", "d", "pet/", "PET.YYYYMMDD.ascii")
################################################################################
# Gauge block                                                                  #
################################################################################
# Name of Gauge
Gauge_name = "CherryCreek"
# In order of c(LON, LAT, OBS, BASINAREA, OUTPUTTS)
Gauge_Params = c("-104.7627778", "39.3558333", "obs/CherryCreek.csv", "435.118", "TRUE")
################################################################################
# Basin block                                                                  #
################################################################################
# Name of Basin
Basin_name <- "CherryCreek"
GAUGE = "CherryCreek"
################################################################################
# CrestParamSet block                                                          #
################################################################################
CrestParamSet_name = "CherryCreek" 
# In order of c(gauge, wm, b, im, ke, fc, iwu)
CrestParamSet_params = c("CherryCreek", "75.403", "13.204", "0.154", "0.362", 
                         "53.558", "24.999")
################################################################################
# kwparamset block                                                             #
################################################################################
# Name of kwparamset
kwparamset_name <- "CherryCreek"
# In order of c(gauge, under, leaki, th, isu, alpha, beta, alpha0)
kwparamset_params = c("CherryCreek", "2.976", "0.042", "4.031", "0.000000", "2.847",
                      "0.884", "1.174")
################################################################################
# CrestCaliParams block                                                        #
################################################################################
CrestCaliParams_name <- "CherryCreek"
# In order of c(gauge, objective, dream_ndraw, wm, b, im, ke, fc, iwu)
CrestCaliParams_params <- c("CherryCreek", "nsce", "100", "5.0,250.0", "0.1,20.0", 
                            "0.00999999,0.5", "0.001,1.0", "0.0,150.0",
                            "24.9999,25.0")

################################################################################
# kwcaliparams block                                                           #
################################################################################
kwcaliparams_name <- "CherryCreek"
# In order of c(gauge, alpha, alpha0, beta, under, leaki, th, isu)
kwcaliparams_params <- c("CherryCreek", "0.01,3.0", "0.01,5.0", "0.01,1.0", 
                        "0.0001,3.0", "0.01,1.0", "1.0,10.0", "0.0,0.0000001")
################################################################################
# Task block                                                                   #
################################################################################
# Name of task
task_name <- "RunCherryCreek"
# In order of c(STYLE, MODEL, ROUTING, BASIN, PRECIP, PET, OUTPUT,
# PARAM_SET, ROUTING_PARAM_SET, TIMESTEP, TIME_BEGIN, TIME_WARMEND, TIME_END)
task_param = c("SIMU", "CREST", "KW", "CherryCreek", "TRMM", "FEWSNET", "output/",
               "CherryCreek", "CherryCreek", "1d", "201001010000", "201006010000",
               "201112310000")
################################################################################
# Do not change from this point                                                #
################################################################################
setwd(outputpath)
fullcontrol = paste(outputpath, controlfile_name, sep = "")
cat(paste0("Start writing control file at ", Sys.time(), "\n"))
# Write the basic block
cat("[Basic]", "\n", file = fullcontrol, sep = "")
cat("DEM=", Basic_Param[1], "\n", file = fullcontrol, sep = "", append = TRUE)
cat("DDM=", Basic_Param[2], "\n", file = fullcontrol, sep = "", append = TRUE)
cat("FAM=", Basic_Param[3], "\n", file = fullcontrol, sep = "", append = TRUE)
cat("PROJ=", Basic_Param[4], "\n", file = fullcontrol, sep = "", append = TRUE)
cat("ESRIDDM=", Basic_Param[5], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("SelfFAM=", Basic_Param[6], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("\n", file = fullcontrol, sep = "", append = TRUE)

# Precipitation forcing block
cat("[PrecipForcing", " ", PrecipForcing_name, "]\n", file = fullcontrol, 
    sep = "", append = TRUE)
cat("TYPE=", PrecipForcing_params[1], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("UNIT=", PrecipForcing_params[2], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("FREQ=", PrecipForcing_params[3], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("LOC=", PrecipForcing_params[4], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("NAME=", PrecipForcing_params[5], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("\n", file = fullcontrol, sep = "", append = TRUE)

# PET forcing block
cat("[PETForcing", " ", PETForcing_name, "]\n", file = fullcontrol, 
    sep = "", append = TRUE)
cat("TYPE=", PETForcing_params[1], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("UNIT=", PETForcing_params[2], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("FREQ=", PETForcing_params[3], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("LOC=", PETForcing_params[4], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("NAME=", PETForcing_params[5], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("\n", file = fullcontrol, sep = "", append = TRUE)

# Gauge forcing block
cat("[Gauge", " ", Gauge_name, "]\n", file = fullcontrol, 
    sep = "", append = TRUE)
cat("LON=", Gauge_Params[1], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("LAT=", Gauge_Params[2], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("OBS=", Gauge_Params[3], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("BASINAREA=", Gauge_Params[4], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("OUTPUTTS=", Gauge_Params[5], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("\n", file = fullcontrol, sep = "", append = TRUE)
cat("[Basin", " ", Basin_name, "]\n", file = fullcontrol, 
    sep = "", append = TRUE)
cat("GAUGE=", GAUGE, "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("\n", file = fullcontrol, sep = "", append = TRUE)

# CrestparamSet block
cat("[CrestParamSet", " ", CrestParamSet_name, "]\n", file = fullcontrol, 
    sep = "", append = TRUE)
cat("gauge=", CrestParamSet_params[1], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("wm=", CrestParamSet_params[2], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("b=", CrestParamSet_params[3], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("im=", CrestParamSet_params[4], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("ke=", CrestParamSet_params[5], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("fc=", CrestParamSet_params[6], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("iwu=", CrestParamSet_params[7], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("\n", file = fullcontrol, sep = "", append = TRUE)

# kwparamset block
cat("[kwparamset", " ", kwparamset_name, "]\n", file = fullcontrol, 
    sep = "", append = TRUE)
cat("gauge=", kwparamset_params[1], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("under=", kwparamset_params[2], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("leaki=", kwparamset_params[3], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("th=", kwparamset_params[4], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("isu=", kwparamset_params[5], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("alpha=", kwparamset_params[6], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("beta=", kwparamset_params[7], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("alpha0=", kwparamset_params[8], "\n", file = fullcontrol, sep = "", 
    append = TRUE)
cat("\n", file = fullcontrol, sep = "", append = TRUE)

# Calibration block
if (Calibration_Option == TRUE) {
  # CrestCaliParams block
  cat("[CrestCaliParams", " ", CrestCaliParams_name, "]\n", file = fullcontrol, 
      sep = "", append = TRUE)
  cat("gauge=", CrestCaliParams_params[1], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("objective=", CrestCaliParams_params[2], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("dream_ndraw=", CrestCaliParams_params[3], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("wm=", CrestCaliParams_params[4], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("b=", CrestCaliParams_params[5], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("im=", CrestCaliParams_params[6], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("ke=", CrestCaliParams_params[7], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("fc=", CrestCaliParams_params[8], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("iwu=", CrestCaliParams_params[9], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("\n", file = fullcontrol, sep = "", append = TRUE)
  
  # kwcaliparams block
  cat("[kwcaliparams", " ", kwcaliparams_name, "]\n", file = fullcontrol, 
      sep = "", append = TRUE)
  cat("gauge=", kwcaliparams_params[1], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("alpha=", kwcaliparams_params[2], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("alpha0=", kwcaliparams_params[3], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("beta=", kwcaliparams_params[4], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("under=", kwcaliparams_params[5], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("leaki=", kwcaliparams_params[6], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("th=", kwcaliparams_params[7], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("isu=", kwcaliparams_params[8], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("\n", file = fullcontrol, sep = "", append = TRUE)
}

# Task block
if (Calibration_Option == TRUE) {
  # To calibrate
  cat("[Task", " ", calibration_task_name, "]\n", file = fullcontrol, 
      sep = "", append = TRUE)
  cat("STYLE=", "cali_dream", "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("MODEL=", task_param[2], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("ROUTING=", task_param[3], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("BASIN=", task_param[4], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("PRECIP=", task_param[5], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("PET=", task_param[6], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("OUTPUT=", task_param[7], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("PARAM_SET=", task_param[8], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("ROUTING_PARAM_Set=", task_param[9], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("cali_param=", task_param[9], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("routing_cali_param=", task_param[9], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("TIMESTEP=", task_param[10], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("TIME_BEGIN=", task_param[11], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("TIME_WARMEND=", task_param[12], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("TIME_END=", task_param[13], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("\n", file = fullcontrol, sep = "", append = TRUE)
  
  cat("[Execute]", "\n", file = fullcontrol, 
      sep = "", append = TRUE)
  cat("TASK=", calibration_task_name, "\n", file = fullcontrol, sep = "", 
      append = TRUE)
} else {
  # Task block
  cat("[Task", " ", task_name, "]\n", file = fullcontrol, 
      sep = "", append = TRUE)
  cat("STYLE=", task_param[1], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("MODEL=", task_param[2], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("ROUTING=", task_param[3], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("BASIN=", task_param[4], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("PRECIP=", task_param[5], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("PET=", task_param[6], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("OUTPUT=", task_param[7], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("PARAM_SET=", task_param[8], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("ROUTING_PARAM_Set=", task_param[9], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("TIMESTEP=", task_param[10], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("TIME_BEGIN=", task_param[11], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("TIME_WARMEND=", task_param[12], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("TIME_END=", task_param[13], "\n", file = fullcontrol, sep = "", 
      append = TRUE)
  cat("\n", file = fullcontrol, sep = "", append = TRUE)
  cat("[Execute]", "\n", file = fullcontrol, 
      sep = "", append = TRUE)
  cat("TASK=", task_name, "\n", file = fullcontrol, sep = "", 
      append = TRUE)
}




cat(paste0("Finished writing control file at ", Sys.time()))
################################################################################
# Run the simulation                                                           #
################################################################################
# shell.exec(paste(outputpath, EF5_name, sep = ""))

################################################################################
# Reading the output                                                           #
################################################################################
# OutputData <- read.csv("/home/tpham/Documents/EF5/EF5_training_short/examples/wangchu/output/ts.chhukha.crest.csv",
#                        skip = 0, sep = ",")
# 
# Time <- OutputData[,1]
# Date <- seq(as.Date(Time[1]),
#             to = as.Date(Time[length(Time)]), by = '1 month')
# Sim_Discharge <- OutputData[,2]
# Obs_Discharge <- OutputData[,3]
# Precip <- OutputData[,4]
# PET <- OutputData[,5]
# SM <- OutputData[,6]
# Fast_Flow <- OutputData[,7]
# Slow_Flow <- OutputData[,8]
# 
# ################################################################################
# # Nash-Sutcliffe Efficiency                                                    #
# ################################################################################
# NSEC <- function(Sim, Obs) {
#   if (length(Sim) != length(Obs)) {
#     stop("Number of Obs must be equal to number of Sim")
#   }
#   DF <- data.frame(Sim, Obs)
#   colnames(DF) <- c("Sim", "Obs")
#   DF <- DF[complete.cases(DF),]
#   # Numerator is the sum of (simulation - observation)^2
#   numerator <- sum((DF[, "Sim"] - DF[,"Obs"])^2)
#   # Denominator is the sum of (observation - mean_observation)^2
#   denominator <- sum((DF[, "Obs"] - mean(DF[, "Obs"]))^2)
#   
#   # Calculate the Nash-Sutcliffe Efficiency Coefficient
#   NSEC <- 1 - numerator / denominator
#   
#   return(NSEC)
#   
# }
# 
# Discharge_CC <- format(cor(Sim_Discharge, Obs_Discharge, use = "complete.obs"),
#                        nsmall = 2)
# 
# Discharge_Bias <- bias(Obs_Discharge, Sim_Discharge)
# 
# Discharge_NSEC <- NSEC(Sim_Discharge, Obs_Discharge)
# ################################################################################
# # Plotting the Discharge                                                       #
# ################################################################################
# par(pty = "m")
# plot.new()
# par(mar = c(5,5,2,5))
# zx = c(0,1)
# zy = c(-1,-1)
# par(new = TRUE, mar=c(5,5,2,5))
# plot(zx,zy,ylim=range(0,5),xaxt='n',yaxt='n',ann=FALSE)
# par(new = TRUE,mar=c(5,5,18,5))
# plot(as.Date(Time, format = "%Y-%m-%d %H:%M"), 
#      Sim_Discharge,
#      xlab = "Time",
#      ylab = expression("Discharge" ~ ("m"^3/s)),
#      type = "l", 
#      col = "red", 
#      lwd = 2.5,
#      bty = "n", 
#      axes = F)
# points(as.Date(Time, format = "%Y-%m-%d %H:%M"), 
#        Obs_Discharge,
#        xlab = "",
#        ylab = "",
#        type = "l", 
#        col = "black", 
#        lwd = 2.5,
#        bty = "n", 
#        axes = F)
# legend("center", 
#        title = paste0("Cor = ", format(Discharge_CC, nsmall = 1), "\n",
#                       "Bias = ", format(Discharge_Bias, nsmall = 1), "\n",
#                       "NSEC = ", format(Discharge_NSEC, nsmall = 1)),
#        c("Precipitation", "Q_Sim ", "Q_Obs"),
#        lty = c(1,1,1),
#        col = c("darkgreen", "red", "black"), 
#        bty = "n")
# axis(1, at = Date, labels = Date)
# axis(2)
# par(new = TRUE,mar = c(26,5,2,5))
# barplot(Precip, 
#         xaxt = 'n', 
#         ylim = c(max(Precip),0), 
#         bty='n', 
#         yaxs = "i", 
#         xlab = "", 
#         ylab = "", 
#         border = "darkgreen", axes = F)
# axis(4)
# mtext(expression("Precipitation" ~ ("mm"/h)), side = 4, line = 3)
# ################################################################################
# # Plot the Soil Moisture
# ################################################################################
# if (Moisture_Plot == TRUE) {
#   par(pty = "m")
#   plot.new()
#   par(mar = c(5,5,2,5))
#   zx = c(0,1)
#   zy = c(-1,-1)
#   par(new = TRUE, mar=c(5,5,2,5))
#   plot(zx,zy,ylim=range(0,5),xaxt='n',yaxt='n',ann=FALSE)
#   par(new = TRUE,mar=c(5,5,18,5))
#   plot(as.Date(Time, format = "%Y-%m-%d %H:%M"), 
#        SM,
#        xlab = "Time",
#        ylab = expression("Soil Moisture" ~ "(%)"),
#        type = "l", 
#        col = "red", 
#        lwd = 2.5,
#        bty = "n", 
#        axes = F)
#   axis(1, at = Date, labels = Date)
#   axis(2, xlim = c(0, 100))
#   par(new = TRUE,mar = c(26,5,2,5))
#   barplot(Precip, 
#           xaxt = 'n', 
#           ylim = c(max(Precip),0), 
#           bty='n', 
#           yaxs = "i", 
#           xlab = "", 
#           ylab = "", 
#           border = "darkgreen", 
#           axes = F)
#   axis(4)
#   mtext(expression("Precipitation" ~ ("mm"/h)), side = 4, line = 3)
# 
# }
# 
# 
















