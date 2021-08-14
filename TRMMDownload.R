library(curl)

# Folder to save the downloaded files
# Example "C:/Users/pham2974/Desktop/P/"
outputpath <- "C:/Users/pham2974/Desktop/P/"

# Define the period of data to get, ex. c(2009, 2010, 2011) for 3 year
Data_to_Get <- c(2009)

# in the format "ftp://youremail%40ou.edu:youremail%40ou.edu@arthurhou.pps.eosdis.nasa.gov/trmmdata/GIS/"
# %40 is equal to @



URLMain <- "ftp://tri.g.pham%40ou.edu:tri.g.pham%40ou.edu@arthurhou.pps.eosdis.nasa.gov/trmmdata/GIS/"

h = new_handle(ftp_use_epsv = FALSE, dirlistonly = TRUE, crlf = TRUE,
               ssl_verifypeer = FALSE, ftp_response_timeout = 30)

MainConnection <- curl(URLMain, "r", h)
FolderList <- readLines(MainConnection)
close.connection(MainConnection)

# Access Year Folder
for (i in 1:length(Data_to_Get)) {
  SubURL <- paste(URLMain, Data_to_Get[i], "/", sep = "")
  SubConnection <- curl(SubURL, "r", 
                        handle = new_handle(ftp_use_epsv = FALSE, 
                                            dirlistonly = TRUE, 
                                            ssl_verifypeer = FALSE, 
                                            ftp_response_timeout = 30))
  SubFolderList <- readLines(SubConnection)
  print(SubFolderList)
  close.connection(SubConnection)
  # Access Month Folder
  for (i in 1:length(SubFolderList)) {
    MonthFolderURL <- paste(SubURL, SubFolderList[i], "/", sep = "")
    MonthFolderConnection <- curl(MonthFolderURL, "r", 
                                  handle = new_handle(ftp_use_epsv = FALSE, 
                                                      dirlistonly = TRUE, 
                                                      crlf = TRUE,
                                                      ssl_verifypeer = FALSE, 
                                                      ftp_response_timeout = 30))
    DayFolderList <- readLines(MonthFolderConnection)
    print(DayFolderList)
    close.connection(MonthFolderConnection)
    # Access Day Folder
    for (i in 1:length(DayFolderList)) {
      HourlyDataURL <- paste(MonthFolderURL, DayFolderList[i], "/", sep = "")
      HourlyDataConnection <- curl(HourlyDataURL, 
                                   "r", 
                                   handle = new_handle(ftp_use_epsv = FALSE, 
                                                       dirlistonly = TRUE, 
                                                       crlf = TRUE,
                                                       ssl_verifypeer = FALSE, 
                                                       ftp_response_timeout = 30))
      HourlyFileList <- readLines(HourlyDataConnection)
      print(HourlyFileList)
      close.connection(HourlyDataConnection)
      # Access Hourly Data and Download
      for (i in 1:length(HourlyFileList)) {
        File_Path <- paste(HourlyDataURL, HourlyFileList[i], sep = "")
        # print(File_Path)
        curl_download(File_Path,
                      destfile = paste(outputpath, HourlyFileList[i], sep = ""),
                      quiet = FALSE)
      }
    }
  }
}









