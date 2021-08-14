library(dplyr)


inputpath = "/home/tpham/Desktop/"
options(scipen = 999)
Tower_File = "USMoisst.csv"
data = read.csv(paste(inputpath, Tower_File, sep = ""), skip = 0)  

data$TIMESTAMP <- as.POSIXct(data$TIMESTAMP, format = "%m/%d/%Y %H:%M")

data$TIMESTAMP <- format.POSIXct(data$TIMESTAMP, '%Y/%m/%d %H:%M')

TimeList <- seq.POSIXt(as.POSIXct("2013-01-01 0:00",'%Y/%m/%d %H:%M'),
                 as.POSIXct("2017-12-31 23:30",'%Y/%m/%d %H:%M'), by = "30 mins")

TimeList <- format.POSIXct(TimeList, '%Y/%m/%d %H:%M')

FullTime <- data.frame(TIMESTAMP = TimeList)


MOISST_Filled <- full_join(FullTime,data)

MOISST_Filled$TIMESTAMP <- format(strptime(MOISST_Filled$TIMESTAMP, 
                                          "%Y/%m/%d %H:%M"), 
                                  "%Y%m%d%H%M")

write.csv(MOISST_Filled, file = paste(inputpath, "MOISSTFilled.csv", sep = ""),
          row.names = F)


# data$TIMESTAMP[27623]
# data$TIMESTAMP[28097]








