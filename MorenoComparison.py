#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 14:05:44 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates




'''
###############################################################################
SrgFile = '/home/tpham/Desktop/ProcessedFiles/SrgDiurnal_calibration.csv'
SrgData = pd.read_csv(SrgFile)

SrgMorenoFile = '/home/tpham/Desktop/ProcessedFiles/Srg_Moreno3.csv'
SrgMorenoData = pd.read_csv(SrgMorenoFile)


###############################################################################
SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrgData['Date']])
SrgData.set_index('Time', inplace = True, drop = True)
SrgData.replace(to_replace = -9999, value = np.nan, inplace = True) 

Start = np.where(SrgData["Date"] == str('01/01/2009 00:00'))[0][0]
End = np.where(SrgData["Date"] == str('11/30/2009 23:00'))[0][0]

#SrgData = SrgData[Start:End]

SrgData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in SrgData['Date']])
SrgData.drop(['Date'], axis = 1, inplace = True)
SrgData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrgData['month']])


SrgDF = SrgData.apply(pd.to_numeric).resample("D").mean()
SrgDF['P_sum'] = SrgData['Rain_Obs'].apply(pd.to_numeric).resample("D").sum()

SrgDF['ET_Total'] = SrgDF['Transpiration'] + SrgDF['EvaporationCanopy'] + SrgDF['EvaporationSoil']


#SrgData = SrgData.apply(pd.to_numeric).resample("M").mean()
#SrgData['month'] = SrgData['month'].astype(int)
#SrgData = SrgData.apply(pd.to_numeric).resample("M").mean()
#SrgData.index = ([datetime.datetime.strftime(x, '%b') 
#                        for x in SrgData.index])

SrgMorenoData['Date'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y') 
                        for x in SrgMorenoData['Time']])
SrgMorenoData.set_index('Date', inplace = True, drop = True)
SrgMorenoData.replace(to_replace = -9999, value = np.nan, inplace = True) 


SrgMorenoData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y') 
                        for x in SrgMorenoData['Time']])
SrgMorenoData.drop(['Time'], axis = 1, inplace = True)
SrgMorenoData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrgMorenoData['month']])

SrgMorenoData=SrgMorenoData.rename(columns = {'ET':'ET_M'})

#SrgMorenoData = SrgMorenoData.apply(pd.to_numeric).resample("D").mean()
#SrgMorenoData['month'] = SrgMorenoData['month'].astype(int)
#SrgMorenoData = SrgMorenoData.apply(pd.to_numeric).resample("M").mean()
#SrgMorenoData.index = ([datetime.datetime.strftime(x, '%b') 
#                        for x in SrgMorenoData.index])


SrgMerged = SrgDF.merge(SrgMorenoData, left_index=True, right_index=True, how='outer')


Start = SrgMerged.index.get_loc((SrgMerged[SrgMerged.index == '2009-01-01']).iloc[0].name)
End = SrgMerged.index.get_loc((SrgMerged[SrgMerged.index == '2009-11-30']).iloc[0].name)
SrgMerged = SrgMerged[Start:(End+1)]



###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
ax2 = ax1.twinx()
ax2.invert_yaxis()

lns1 = ax2.bar(SrgMerged.index, SrgMerged['P_sum'], 
        align = 'center', label = 'US-SRG Precipitation [mm]', width = 2)

lns2 = ax1.plot(SrgMerged.index, SrgMerged['ET_M'],
                label = 'ET (Moreno et al.)', color = 'C1', linewidth = 4)

lns4 = ax1.plot(SrgMerged.index, SrgMerged['ET'],
                label = 'ET (tRIBS)', linestyle = '--', color = 'C1', linewidth = 4)

lns3 = ax1.plot(SrgMerged.index, SrgMerged['T'],
                label = 'Transpiration (Moreno et al.)', color = 'C2', linewidth = 4)

lns5 = ax1.plot(SrgMerged.index, SrgMerged['Transpiration'],
                label = 'Transpiration (tRIBS)', linestyle = '--', color = 'C2', linewidth = 4)




ax1.set_ylim((0, 0.46))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.31, 0.05))
ax1.set_ylabel("ET Component [mm/hr]", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

ax2.margins(y=0)
ax2.set_ylim((40, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 21, 5))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.legend(prop={'size': 22})
ax2.legend().set_visible(False)


lns = lns5+lns4+lns3+lns2+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/Srg_Moreno_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)







'''

'''

###############################################################################
SrmFile = '/home/tpham/Desktop/ProcessedFiles/SrmDiurnal_calibration.csv'
SrmData = pd.read_csv(SrmFile)

SrmMorenoFile = '/home/tpham/Desktop/ProcessedFiles/Srm_Moreno.csv'
SrmMorenoData = pd.read_csv(SrmMorenoFile)


###############################################################################
SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrmData['Date']])
SrmData.set_index('Time', inplace = True, drop = True)
SrmData.replace(to_replace = -9999, value = np.nan, inplace = True) 

Start = np.where(SrmData["Date"] == str('01/01/2009 00:00'))[0][0]
End = np.where(SrmData["Date"] == str('11/30/2009 23:00'))[0][0]

#SrmData = SrmData[Start:End]

SrmData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in SrmData['Date']])
SrmData.drop(['Date'], axis = 1, inplace = True)
SrmData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrmData['month']])


SrmDF = SrmData.apply(pd.to_numeric).resample("D").mean()
SrmDF['P_sum'] = SrmData['Rain_Obs'].apply(pd.to_numeric).resample("D").sum()

#SrmData = SrmData.apply(pd.to_numeric).resample("M").mean()
#SrmData['month'] = SrmData['month'].astype(int)
#SrmData = SrmData.apply(pd.to_numeric).resample("M").mean()
#SrmData.index = ([datetime.datetime.strftime(x, '%b') 
#                        for x in SrmData.index])

SrmMorenoData['Date'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y') 
                        for x in SrmMorenoData['Time']])
SrmMorenoData.set_index('Date', inplace = True, drop = True)
SrmMorenoData.replace(to_replace = -9999, value = np.nan, inplace = True) 


SrmMorenoData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y') 
                        for x in SrmMorenoData['Time']])
SrmMorenoData.drop(['Time'], axis = 1, inplace = True)
SrmMorenoData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrmMorenoData['month']])

SrmMorenoData=SrmMorenoData.rename(columns = {'ET':'ET_M'})

#SrmMorenoData = SrmMorenoData.apply(pd.to_numeric).resample("D").mean()
#SrmMorenoData['month'] = SrmMorenoData['month'].astype(int)
#SrmMorenoData = SrmMorenoData.apply(pd.to_numeric).resample("M").mean()
#SrmMorenoData.index = ([datetime.datetime.strftime(x, '%b') 
#                        for x in SrmMorenoData.index])


SrmMerged = SrmDF.merge(SrmMorenoData, left_index=True, right_index=True, how='outer')


Start = SrmMerged.index.get_loc((SrmMerged[SrmMerged.index == '2009-01-01']).iloc[0].name)
End = SrmMerged.index.get_loc((SrmMerged[SrmMerged.index == '2009-11-30']).iloc[0].name)
SrmMerged = SrmMerged[Start:(End+1)]

###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
ax2 = ax1.twinx()
ax2.invert_yaxis()

lns1 = ax2.bar(SrmMerged.index, SrmMerged['P_sum'], 
        align = 'center', label = 'US-SRM Precipitation [mm]', width = 2)

lns2 = ax1.plot(SrmMerged.index, SrmMerged['ET_M'],
                label = 'ET (Moreno et al.)', color = 'C1', linewidth = 4)

lns4 = ax1.plot(SrmMerged.index, SrmMerged['ET'],
                label = 'ET (tRIBS)', linestyle = '--', color = 'C1', linewidth = 4)

lns3 = ax1.plot(SrmMerged.index, SrmMerged['T'],
                label = 'Transpiration (Moreno et al.)', color = 'C2', linewidth = 4)

lns5 = ax1.plot(SrmMerged.index, SrmMerged['Transpiration'],
                label = 'Transpiration (tRIBS)', linestyle = '--', color = 'C2', linewidth = 4)




ax1.set_ylim((0, 0.36))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.21, 0.05))
ax1.set_ylabel("ET Component [mm/hr]", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

ax2.margins(y=0)
ax2.set_ylim((36, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 16, 5))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.legend(prop={'size': 22})
ax2.legend().set_visible(False)


lns = lns5+lns4+lns3+lns2+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/Srm_Moreno_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)




'''


###############################################################################
SrcFile = '/home/tpham/Desktop/ProcessedFiles/SrcDiurnal_calibration.csv'
SrcData = pd.read_csv(SrcFile)

SrcMorenoFile = '/home/tpham/Desktop/ProcessedFiles/Src_Moreno.csv'
SrcMorenoData = pd.read_csv(SrcMorenoFile)


###############################################################################
SrcData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrcData['Date']])
SrcData.set_index('Time', inplace = True, drop = True)
SrcData.replace(to_replace = -9999, value = np.nan, inplace = True) 

Start = np.where(SrcData["Date"] == str('01/01/2009 00:00'))[0][0]
End = np.where(SrcData["Date"] == str('11/30/2009 23:00'))[0][0]

#SrcData = SrcData[Start:End]

SrcData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in SrcData['Date']])
SrcData.drop(['Date'], axis = 1, inplace = True)
SrcData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrcData['month']])


SrcDF = SrcData.apply(pd.to_numeric).resample("D").mean()
SrcDF['P_sum'] = SrcData['Rain_Obs'].apply(pd.to_numeric).resample("D").sum()

#SrcData = SrcData.apply(pd.to_numeric).resample("M").mean()
#SrcData['month'] = SrcData['month'].astype(int)
#SrcData = SrcData.apply(pd.to_numeric).resample("M").mean()
#SrcData.index = ([datetime.datetime.strftime(x, '%b') 
#                        for x in SrcData.index])

SrcMorenoData['Date'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y') 
                        for x in SrcMorenoData['Time']])
SrcMorenoData.set_index('Date', inplace = True, drop = True)
SrcMorenoData.replace(to_replace = -9999, value = np.nan, inplace = True) 


SrcMorenoData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y') 
                        for x in SrcMorenoData['Time']])
SrcMorenoData.drop(['Time'], axis = 1, inplace = True)
SrcMorenoData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrcMorenoData['month']])

SrcMorenoData=SrcMorenoData.rename(columns = {'ET':'ET_M'})

SrcMorenoData['ET_M'] = SrcMorenoData['ET_M'] / 24
SrcMorenoData['T'] = SrcMorenoData['T'] / 24
#SrcMorenoData = SrcMorenoData.apply(pd.to_numeric).resample("D").mean()
#SrcMorenoData['month'] = SrcMorenoData['month'].astype(int)
#SrcMorenoData = SrcMorenoData.apply(pd.to_numeric).resample("M").mean()
#SrcMorenoData.index = ([datetime.datetime.strftime(x, '%b') 
#                        for x in SrcMorenoData.index])


SrcMerged = SrcDF.merge(SrcMorenoData, left_index=True, right_index=True, how='outer')


Start = SrcMerged.index.get_loc((SrcMerged[SrcMerged.index == '2009-01-01']).iloc[0].name)
End = SrcMerged.index.get_loc((SrcMerged[SrcMerged.index == '2009-11-30']).iloc[0].name)
SrcMerged = SrcMerged[Start:(End+1)]

###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
ax2 = ax1.twinx()
ax2.invert_yaxis()

lns1 = ax2.bar(SrcMerged.index, SrcMerged['P_sum'], 
        align = 'center', label = 'US-SRC Precipitation [mm]', width = 2)

lns2 = ax1.plot(SrcMerged.index, SrcMerged['ET_M'],
                label = 'ET (Moreno et al.)', color = 'C1', linewidth = 4)

lns4 = ax1.plot(SrcMerged.index, SrcMerged['ET'],
                label = 'ET (tRIBS)', linestyle = '--', color = 'C1', linewidth = 4)

lns3 = ax1.plot(SrcMerged.index, SrcMerged['T'],
                label = 'Transpiration (Moreno et al.)', color = 'C2', linewidth = 4)

lns5 = ax1.plot(SrcMerged.index, SrcMerged['Transpiration'],
                label = 'Transpiration (tRIBS)', linestyle = '--', color = 'C2', linewidth = 4)




ax1.set_ylim((0, 0.6))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.31, 0.05))
ax1.set_ylabel("ET Component [mm/hr]", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

ax2.margins(y=0)
ax2.set_ylim((36, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 16, 5))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.legend(prop={'size': 22})
ax2.legend().set_visible(False)


lns = lns5+lns4+lns3+lns2+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)


plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/Src_Moreno_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)




'''
np.corrcoef(SrcMerged['ET_M'], SrcMerged['ET'])[1,0]

np.corrcoef(SrgMerged['ET_M'], SrgMerged['ET'])[1,0]

np.corrcoef(SrmMerged['ET_M'], SrmMerged['ET'])[1,0]



np.corrcoef(SrcMerged['T'], SrcMerged['Transpiration'])[1,0]

np.corrcoef(SrgMerged['T'], SrgMerged['Transpiration'])[1,0]

np.corrcoef(SrmMerged['T'], SrmMerged['Transpiration'])[1,0]


import hydroeval

hydroeval.nse(np.array(SrcMerged['T']), np.array(SrcMerged['Transpiration']))
hydroeval.nse(np.array(SrgMerged['T']), np.array(SrgMerged['Transpiration']))
hydroeval.nse(np.array(SrmMerged['T']), np.array(SrmMerged['Transpiration']))


hydroeval.nse(np.array(SrcMerged['ET_M']), np.array(SrcMerged['ET']))
hydroeval.nse(np.array(SrgMerged['ET_M']), np.array(SrgMerged['ET']))
hydroeval.nse(np.array(SrmMerged['ET_M']), np.array(SrmMerged['ET']))

'''










#SrmMorenoData['ET'] / SrmData['ET'] * 100
#SrmData['ET'] / SrmMorenoData['ET'] * 100





#SrmMorenoData['T'] / SrmData['Transpiration'] * 100
#SrmData['ET'] / SrmMorenoData['ET'] * 100


