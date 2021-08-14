inputpath <- "C:/Users/Tri/Desktop/EF5/"
flowrate <- "CherryCreekFull.csv"

Data <- read.csv(paste(inputpath, flowrate, sep = ""), skip = 0)

Q_cfs <- Data[,"Q"]
Q_m3s <- Q_cfs * 0.028316847
# Q_m3s <- as.numeric(Q_m3s)
Date <- Data[,"Date"]
Date_formatted <- format(strptime(Date, format = "%Y-%m-%d"), 
                         format = "%Y/%m/%d")

IndexStart <- which(Date_formatted == "2011/01/01")
IndexEnd <- which(Date_formatted == "2011/12/31")

CherryCreekDF <- data.frame(as.character(Date_formatted[IndexStart:IndexEnd]), 
                            Q_m3s[IndexStart:IndexEnd])
colnames(CherryCreekDF) <- c("Time (UTC)", "(cms)")


write.csv(CherryCreekDF, 
          file = paste(inputpath, "CherryCreek.csv", sep = ""),
          row.names = FALSE)













