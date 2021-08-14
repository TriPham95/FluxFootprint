#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 23:31:11 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from scipy.stats import gaussian_kde


PixelFile = '/home/tpham/Desktop/Tribs_USFuf_20062010/Output/Voronoi/USFufVoronoi0.pixel'
FluxFile = '/home/tpham/Desktop/ProcessedFiles/USFufFormatted.csv'


FluxData = pd.read_csv(FluxFile, header = 0)
FluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FluxData['Timestamp']])
FluxData.set_index('Time', inplace = True, drop = True)
Start = FluxData.index.get_loc((FluxData[FluxData['Timestamp'] == 200701010000]).iloc[0].name)
End = FluxData.index.get_loc((FluxData[FluxData['Timestamp'] == 200712312300]).iloc[0].name)
FluxDF = FluxData[Start:(End+1)]
FluxDF.replace(to_replace = str(-9999), value = np.nan, inplace = True) 

FluxDF = FluxDF.reset_index()


pixeldata = pd.read_csv(PixelFile, delim_whitespace=True, header = None)
pixeldata.columns = ["ID", "Time", "Nwt", "Nf", "Nt", "Mu", "Mi", "Qpout",
                         "Qpin", "Trnsm", "GWflx", "Srf", "Rain", "SoilMoist", 
                         "RootMoist", " AirT", "DewT", "SurfT", "SoilT", 
                         "Press", "RelHum", "SkyCov", "Wind", "NetRad", 
                         "ShrtRadIn", "ShrtRadIn_dir", "ShrtRadIn_dif", 
                         "ShortAbsbVeg", "ShortAbsbSoi", "LngRadIn", 
                         "LngRadOut", "PotEvp", "ActEvp", " EvpTtrs", 
                         "EvpWetCan", "EvpDryCan", "EvpSoil", "Gflux", "Hflux", 
                         "Lflux", "NetPrecip", "LiqWE", "IceWE", "SnWE", "U",
                         "RouteWE", "SnTemp", "SurfAge", "DU", "snLHF", "snSHF", 
                         "snGHF", "snPHF", "snRLout", "snRLin", "snRSin", 
                         "Uerror", "intSWEq", "intSub", "intSnUnload", 
                         "CanStorage", "CumIntercept", "Interception", 
                         "Recharge", "RunOn", "srf_Hour", "Qstrm", "Hlevel", 
                         "CanStorParam", "IntercepCoeff", "ThroughFall", 
                         "CanFieldCap", "DrainCoeff", "DrainExpPar", 
                         "LandUseAlb", "VegHeight", "OptTransmCoeff", "StomRes", 
                         "VegFraction", "LeafAI"]
pixeldata = pixeldata.iloc[1:]
pixeldata = pixeldata.reset_index()



PlotDF = FluxDF.merge(pixeldata, left_index=True, right_index=True, how='outer')


###############################################################################
LE_Obs = FluxData["LE"][0:8760]
LE_Sim = pixeldata["Lflux"][0:8760]
H_Obs = FluxData["H"][0:8760]
H_Sim = pixeldata["Hflux"][0:8760]
SoilMoisture_Sim = pixeldata["SoilMoist"][3500:8760]
# SoilMoisture_Sim = PixelData[, "SoilMoist"][0:8760]
SoilMoisture_Obs = FluxData["SWC_1_1_1"][3500:8760]/100
# SoilMoisture2_Obs = FluxData[Index_Start:Index_End, "SWC_2_1_1"][0:8760]/100
RootSoilMoisture_Sim = pixeldata["RootMoist"][3500:8760]
# SoilMoisture_Sim = PixelData["SoilMoist"][0:8760]
RootSoilMoisture_Obs = FluxData["SWC_1_2_1"][3500:8760]/100
G_Obs = FluxData["G_1_1_1"][0:8760]
G_Sim = pixeldata["Gflux"][0:8760]
P_Obs = FluxData["P"][0:8760]
P_Sim = pixeldata["Rain"][0:8760]
TS_Obs = FluxData["TS_1_1_1"][0:8760]
TS_Sim = pixeldata["SurfT"][0:8760]
RootTS_Obs = FluxData["TS_1_2_1"][0:8760]
RootTS_Sim = pixeldata["SoilT"][0:8760]
NetRad_Obs = FluxData["NETRAD"][0:8760]
NetRad_Sim = pixeldata["NetRad"][0:8760]
Rain_Obs = FluxData["P"]
###############################################################################
plt.rcParams.update({'font.size': 22})
fig = plt.figure(figsize=(20,34))
grid = gridspec.GridSpec(nrows = 3, ncols = 6)
fig.subplots_adjust(top=0.95)
# Add axes which can span multiple grid boxes
ax1 = fig.add_subplot(grid[0:1, 0:2], adjustable='box')
ax2 = fig.add_subplot(grid[0:1, 2:4], adjustable='box')
ax3 = fig.add_subplot(grid[0:1, 4:6], adjustable='box')
ax4 = fig.add_subplot(grid[1:2, 0:2], adjustable='box')
ax5 = fig.add_subplot(grid[1:2, 2:4], adjustable='box')
ax6 = fig.add_subplot(grid[1:2, 4:6], adjustable='box')
ax7 = fig.add_subplot(grid[2:3, 1:3], adjustable='box')
ax8 = fig.add_subplot(grid[2:3, 3:5], adjustable='box')


# Calculate the point density
xy = np.vstack([PlotDF["NETRAD"], PlotDF['NetRad']])
xy = xy[~np.isnan(xy)]

z = gaussian_kde(xy)(xy)

# Sort the points by density, so that the densest points are plotted last
idx = z.argsort()
x, y, z = PlotDF["NETRAD"][idx], PlotDF['NetRad'][idx], z[idx]


ax1.scatter(x, y, c=z, s=50, edgecolor='', cmap= 'hot')
ax1.set_xlim((-200, 800))
ax1.set_ylim((-200, 800))
ax1.yaxis.set_ticks(np.arange(-200,801, 200))
ax1.xaxis.set_ticks(np.arange(-200,801, 200))







































