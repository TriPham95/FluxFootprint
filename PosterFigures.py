#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:07:35 2019

@author: tpham
"""
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime


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


fig, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(6, 1)
plt.subplots_adjust(left=0.125)
ax1.invert_yaxis()
MesonetData['RAIN'].plot(ax = ax1)
ax1.set_ylim((81, 0))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0, 81, 20))
ax1.margins(y=0)
ax1.set_ylabel("Precipitation (mm)", fontsize = 8)
ax1.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

MesonetData['TAIR'].plot(ax = ax2, color = 'red')
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.margins(y=0)
ax2.set_ylabel("Air Temp (C)", fontsize = 8)
ax2.set_ylim((-20, 41))
ax2.yaxis.set_ticks(np.arange(-20, 41, 20))
ax2.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

MesonetData['SRAD'].plot(ax = ax3, color = "purple")
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.margins(y=0)
ax3.set_ylabel("Solar Radiation (W.m-2)", fontsize = 8)
ax3.set_ylim((0, 1000))
ax3.yaxis.set_ticks(np.arange(0, 1201, 200))
ax3.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

(MesonetData['RELH']*100).plot(ax = ax4, color = "green")
ax4.set_xticklabels([])
ax4.xaxis.label.set_visible(False)
ax4.margins(y=0)
ax4.set_ylabel("Rel Humidity (%)", fontsize = 8)
ax4.set_ylim((0, 101))
ax4.yaxis.set_ticks(np.arange(0, 101, 20))
ax4.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

MesonetData['WSPD'].plot(ax = ax5, color = 'orange')
ax5.set_xticklabels([])
ax5.xaxis.label.set_visible(False)
ax5.margins(y=0)
ax5.set_ylabel("Wind Speed (m.s-1)", fontsize = 8)
ax5.set_ylim((0, 15.1))
ax5.yaxis.set_ticks(np.arange(0, 15.1, 5))
ax5.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

MesonetData['PRES'].plot(ax = ax6)
#ax6.set_xticklabels([])
#ax6.xaxis.label.set_visible(False)
ax6.margins(y=0)
ax6.set_ylabel("Pressure (mbar)", fontsize = 8)
ax6.set_ylim((28, 30))
ax6.yaxis.set_ticks(np.arange(28, 31, 1))
ax6.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')











SWCFile = '/home/tpham/Windows Share/MOISST_SWC.csv'



SWCData = pd.read_csv(SWCFile)
SWCData.set_index('Time', inplace = True, drop = True)
SWCData = SWCData.astype('float32')
SWCData.dropna()


fig, ax = plt.subplots(1, 1)
plt.subplots_adjust(left = 0.125)
SWCData['SWC10cm'].plot()







ax1.set_ylim((81, 0))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0, 81, 20))
ax1.margins(y=0)
ax1.set_ylabel("Precipitation (mm)", fontsize = 8)
ax1.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')























