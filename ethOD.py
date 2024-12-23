#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 05:17:10 2020

@ygoats
"""

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceRequestException

import apiHighs

import telegram_send

from time import sleep

from datetime import datetime, timedelta

from requests import exceptions

symbol_list = ['ETHUSDT']

def getVars():
    highList = []
    lowList = []
    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    
    try:
        client = Client(apiHighs.APIKey, apiHighs.SecretKey)
        klines = client.get_klines(symbol=symbol_list[0],interval=KLINE_INTERVAL_1DAY, limit=1)
        dailyHigh = float(klines[0][2])  
        dailyLow = float(klines[0][3]) 
        highList.append(dailyHigh)
        lowList.append(dailyLow)
        conNode = False
    except Exception as e:
        pd = open('logs/ethOD.log', 'a')
        pd.write("\n" + str(t) + str(e))
        pd.close()
        print(str(e))
        sleep(60)
        conNode = True
            
        while conNode == True:
            try:
                client = Client(apiHighs.APIKey, apiHighs.SecretKey)
                klines = client.get_klines(symbol=symbol_list[0],interval=KLINE_INTERVAL_1DAY, limit=1)
                dailyHigh = float(klines[0][2])  
                dailyLow = float(klines[0][3]) 
                highList.append(dailyHigh)
                lowList.append(dailyLow)
                conNode = False
            except Exception as e:
                print(str(e))
                sleep(60)
                conNode == True
                
    return highList, lowList
            
def getHighs():
    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    try:
        client = Client(apiHighs.APIKey, apiHighs.SecretKey)
        klines = client.get_klines(symbol=symbol_list[0],interval=KLINE_INTERVAL_1DAY, limit=1)
        currentHigh = klines[0][2]
        conNode = False
    except Exception as e:
        pd = open('logs/ethOD.log', 'a')
        pd.write("\n" + str(t) + str(e))
        pd.close()
        print(str(e))
        sleep(60)
        conNode = True
            
        while conNode == True:
            try:
                client = Client(apiHighs.APIKey, apiHighs.SecretKey)
                klines = client.get_klines(symbol=symbol_list[0],interval=KLINE_INTERVAL_1DAY, limit=1)
                currentHigh = klines[0][2]
                conNode = False
            except Exception as e:
                print(str(e))
                sleep(60)
                conNode == True
                
    return currentHigh

def getLows():
    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    try:
        client = Client(apiHighs.APIKey, apiHighs.SecretKey)
        klines = client.get_klines(symbol=symbol_list[0],interval=KLINE_INTERVAL_1DAY, limit=1)
        currentLow = klines[0][3]
        conNode = False
    except Exception as e:
        pd = open('logs/ethOD.log', 'a')
        pd.write("\n" + str(t) + str(e))
        pd.close()
        print(str(e))
        sleep(60)
        conNode = True
            
        while conNode == True:
            try:
                client = Client(apiHighs.APIKey, apiHighs.SecretKey)
                klines = client.get_klines(symbol=symbol_list[0],interval=KLINE_INTERVAL_1DAY, limit=1)
                currentLow = klines[0][3]
                conNode = False
            except Exception as e:
                print(str(e))
                sleep(60)
                conNode == True
                
    return currentLow
    
def Main():        
    now = datetime.now()
    t = now.strftime("%m/%d/%Y, %H:%M:%S")
    
    print("Connection Established ")
    print(str(t))
    
    highList = getVars()[0]
    highL = float(highList[0]) 
    lowList = getVars()[1]
    lowL = float(lowList[0])
    

    conNode = False
    
    y = 0
    
    while conNode == False:
        sleep(4)
        high = float(getHighs())
        low = float(getLows())
        
        if high > highL:
            print('breaking high')
            telegram_send.send(conf='user1.conf',messages=["New high of day " + str(symbol_list[0]) + " " + str(highList)])
            sleep(60)
            highList = getVars()[0]
            highL = float(highList[0])
            y = y + 1
            continue
        
        if low < lowL:
            print('break lows')
            telegram_send.send(conf='user1.conf',messages=["New low of day " + str(symbol_list[0]) + " " + str(lowList)])
            sleep(60)
            lowList = getVars()[1]
            lowL = float(lowList[0])
            y = y + 1
            continue 
        
        if y == 3:
            sleep(900)
            y = 0
            continue
            
        #print('low: ' + str(low))
        #print('lowList: ' + str(lowL))
        #print('high: ' + str(high))
        #print('highList: ' + str(highL))
       
        
if __name__ == '__main__':
    Main()
