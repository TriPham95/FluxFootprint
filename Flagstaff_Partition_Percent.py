#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:06:06 2020

@author: tpham
"""



import pandas as pd
import numpy as np
import datetime


FufFile = '/home/tpham/Desktop/FufDiurnal_validation.csv'
FwfFile = '/home/tpham/Desktop/FwfDiurnal_calibration.csv'


FufData = pd.read_csv(FufFile)
FwfData = pd.read_csv(FwfFile)

###############################################################################
FufData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in FufData['Date']])
FufData.set_index('Time', inplace = True, drop = True)
FufData.replace(to_replace = -9999, value = np.nan, inplace = True) 
FufData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in FufData['Date']])
FufData.drop(['Date'], axis = 1, inplace = True)
FufData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FufData['month']])
FufData = FufData.apply(pd.to_numeric).resample("M").mean()
FufData['month'] = FufData['month'].astype(int)
FufData = FufData.apply(pd.to_numeric).resample("M").mean()
FufData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FufData.index])


FufData['EvaporationSoil'] / FufData['ET'] * 100
FufData['Transpiration'] / FufData['ET'] * 100 
FufData['EvaporationCanopy'] / FufData['ET']* 100






###############################################################################
FwfData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in FwfData['Date']])
FwfData.set_index('Time', inplace = True, drop = True)
FwfData.replace(to_replace = -9999, value = np.nan, inplace = True) 

FwfData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in FwfData['Date']])
FwfData.drop(['Date'], axis = 1, inplace = True)
FwfData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FwfData['month']])
FwfData = FwfData.apply(pd.to_numeric).resample("M").mean()
FwfData['month'] = FwfData['month'].astype(int)
FwfData = FwfData.apply(pd.to_numeric).resample("M").mean()
FwfData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FwfData.index])


FwfData['EvaporationSoil'] / FwfData['ET'] * 100
FwfData['Transpiration'] / FwfData['ET'] * 100 
FwfData['EvaporationCanopy'] / FwfData['ET']* 100





























