#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:47:04 2020

@author: tpham
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 13:09:33 2019

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
from matplotlib.dates import DateFormatter


MoisstFile = '/home/tpham/Desktop/MoisstFormatted.csv'

MoisstData = pd.read_csv(MoisstFile)
MoisstData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in MoisstData['Timestamp']])
MoisstData.set_index('Time', inplace = True, drop = True)

MoisstIndexStart = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201504010000]).iloc[0].name)
MoisstIndexEnd = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201504200000]).iloc[0].name)
MoisstDF = MoisstData[MoisstIndexStart:MoisstIndexEnd]
MoisstDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

MoisstDF['Rn_total_Avg'].mean()
MoisstDF['LE_wpl'].mean()
MoisstDF['Hs'].mean()
MoisstDF['SHF1_Avg'].mean()
MoisstDF['SWC10'].mean()
MoisstDF['SWC90'].mean()
MoisstDF['SoilTC1_Avg'].mean()
MoisstDF['SoilTC5_Avg'].mean()


MoisstIndexStart = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201504200000]).iloc[0].name)
MoisstIndexEnd = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201505010000]).iloc[0].name)
MoisstDF = MoisstData[MoisstIndexStart:MoisstIndexEnd]
MoisstDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

MoisstDF['Rn_total_Avg'].mean()
MoisstDF['LE_wpl'].mean()
MoisstDF['Hs'].mean()
MoisstDF['SHF1_Avg'].mean()
MoisstDF['SWC10'].mean()
MoisstDF['SWC90'].mean()
MoisstDF['SoilTC1_Avg'].mean()
MoisstDF['SoilTC5_Avg'].mean()


MoisstIndexStart = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201504200000]).iloc[0].name)
MoisstIndexEnd = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201505100000]).iloc[0].name)
MoisstDF = MoisstData[MoisstIndexStart:MoisstIndexEnd]
MoisstDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

MoisstDF['Rn_total_Avg'].mean()
MoisstDF['LE_wpl'].mean()
MoisstDF['Hs'].mean()
MoisstDF['SHF1_Avg'].mean()
MoisstDF['SWC10'].mean()
MoisstDF['SWC90'].mean()
MoisstDF['SoilTC1_Avg'].mean()
MoisstDF['SoilTC5_Avg'].mean()



###############################################################################
MesonetFile = '/home/tpham/Desktop/MoisstPrecipitation.csv'

MesonetData = pd.read_csv(MesonetFile)
MesonetData.replace(-999, float('nan'), inplace=True)

MesonetData['Time'] = ([datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M') 
                        for x in MesonetData['TIME']])
MesonetData['TAIR'] = (["{0:.2f}".format((x - 32) * (5/9)) \
                       for x in MesonetData['TAIR']])
MesonetData['TDEW'] = (["{0:.2f}".format((x - 32) * (5/9)) \
                       for x in MesonetData['TDEW']])
MesonetData['RELH'] = (["{0:.2f}".format(float(x) / 100) 
                        for x in MesonetData['RELH']])
MesonetData['RAIN'] = (["{0:.4f}".format(float(x) * 25.4) 
                        for x in MesonetData['RAIN']])
MesonetData['PRES'] = (["{0:.4f}".format(float(x) * 1) 
                        for x in MesonetData['PRES']])
MesonetData['SRAD'] = (["{0:.2f}".format(float(x)) 
                        for x in MesonetData['SRAD']])
MesonetData['WSPD'] = (["{0:.2f}".format(float(x) * 0.44704) 
                        for x in MesonetData['WSPD']])
MesonetData['WDIR'] = (["{0:.2f}".format(float(x)) 
                        for x in MesonetData['WDIR']])
MesonetData.drop(['STID', 'TIME', 'TMIN', 'TMAX', 'WMAX'], axis = 1, inplace = True)
MesonetData.set_index('Time', inplace = True, drop = True)
MesonetData = MesonetData.astype('float32')
Start = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2015-04-01 00:00:00']).iloc[0].name)
End = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2015-05-10 00:00:00']).iloc[0].name)
MesonetDataNew = MesonetData[Start:End]


MesonetDataNew['RAIN'].mean()
MesonetDataNew['SRAD'].mean()

MesonetDataNew['TAIR'].mean()

MesonetDataNew['RELH'].mean()

(MesonetDataNew['PRES']*33.8639).mean()


Start = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2015-04-20 00:00:00']).iloc[0].name)
End = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2015-05-10 00:00:00']).iloc[0].name)
MesonetDataNew = MesonetData[Start:End]

MesonetDataNew['RAIN'].mean()
MesonetDataNew['SRAD'].mean()

MesonetDataNew['TAIR'].mean()

MesonetDataNew['RELH'].mean()

(MesonetDataNew['PRES']*33.8639).mean()




































































