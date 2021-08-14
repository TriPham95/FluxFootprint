inputpath <- "C:/Users/Tri/Desktop/EF5/"
flowrate <- "CherryCreek.csv"

Data <- read.csv(paste(inputpath, flowrate, sep = ""), skip = 0)

Q_cfs <- Data[,"Q"]
Q_m3s <- Q_cfs * 0.028316847

Date <- Data[,"Date"]

Date_formatted <- format(strptime(Date, format = "%Y-%m-%d"), 
                         format = "%Y/%m/%d")


CherryCreekDF <- data.frame(Date_formatted, Q_m3s)
colnames(CherryCreekDF) <- c("Date", "Q(m3s)")


write.csv(CherryCreekDF, 
          file = paste(inputpath, "Cherry.csv", sep = ""),
          row.names = FALSE)













