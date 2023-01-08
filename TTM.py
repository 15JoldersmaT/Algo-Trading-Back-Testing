import datetime
import numpy as np
import pandas as pd
import Manson2
import time
import matplotlib as mp
from matplotlib import pyplot as plt
from binance.client import Client
import talib

#The Time Machine
#PURPOSE: Backtesting crypto trading strategies

#Time lengths are in minutes
#1440 = 1 day
#

prices = []
volume = []
priceCheck = []


def backtest(strategy, timeLength):

#Use your keys
    client = Client('*******','**********',tld='us')


    data = client.get_klines(symbol='ETHUSDT', interval='5m', limit=999)
    data = client.get_historical_klines("ETHUSDT", '1m', "1 week ago UTC")

    
    
    for x in data:
        prices.append(x[3])
        volume.append(x[5])

    print(len(prices))
    
 
        
    
    

    #mansonVol(timeLength, 500, 1500, 120)
    #Jolde(timeLength, 440,440)

   Flores(timeLength, 20,180, 200, 20)


 
    #best = 0
    #bestX = 0
    #bestY = 0
    #for x in range(100):
        #for y in range(100):
            #amount = Flores(timeLength, 100 + x ,100 +y, 120, 25)

            #if(amount > best):
                #best = amount
                #bestX = x
                #bestY = y
    #print("Best = " + str(bestX) + " " + str(bestY) + " " + str(best))

    #mansonPlus(timeLength, 1000, 2000, 3000, 60, 1000)


#Manson uses two SMA's to generate price signals
def manson(timeLength, fast, med):
    currentTime = 0
    money = 0
    coins = 0
    fast = fast
    fastAvg = 0
    med = med
    medAvg = 0
    boughtAt = 0
    soldAt = 0
    while currentTime<timeLength:
       # print(-(timeLength)+currentTime)
        currentPrice = prices[-(timeLength)+currentTime]

        ######################fast Average
        numFast = 0
        for x in range(fast):
            numFast += float(prices[-x - (timeLength-currentTime)])
        fastAvg = float(numFast/fast)
        #print("Fast Average : " + str(fastAvg))
        ###############################

        ######################med Average
        numMed = 0
        for x in range(med):
            #print(-x - (timeLength-currentTime))
            numMed += float(prices[-x - (timeLength-currentTime)])
        medAvg = float(numMed/med)
        #print("Medium Average : " + str(medAvg))
        ###############################

        #Signals
        if float(fastAvg) > float(medAvg) and coins == 0:
            boughtAt = float(currentPrice) + (float(currentPrice) * .00075)
            coins+=1
            #print("Bought At : " + str(currentPrice))
            
        if float(fastAvg) < float(medAvg) and coins > 0:
            soldAt = float(currentPrice) - (float(currentPrice) * .00075)
            coins-=1
            money += (soldAt - boughtAt)
            #print("Sold At : " + str(currentPrice))

        currentTime+=1

    print(money)

def mansonLong(timeLength, fast, med, long):
    currentTime = 0
    money = 0
    coins = 0
    fast = fast
    fastAvg = 0
    med = med
    medAvg = 0
    long = long
    longAvg = 0
    boughtAt = 0
    soldAt = 0
    while currentTime<timeLength:
       # print(-(timeLength)+currentTime)
        currentPrice = prices[-(timeLength)+currentTime]

        ######################fast Average
        numFast = 0
        for x in range(fast):
            numFast += float(prices[-x - (timeLength-currentTime)])
        fastAvg = float(numFast/fast)
        #print("Fast Average : " + str(fastAvg))
        ###############################

        ######################med Average
        numMed = 0
        for x in range(med):
            #print(-x - (timeLength-currentTime))
            numMed += float(prices[-x - (timeLength-currentTime)])
        medAvg = float(numMed/med)
        #print("Medium Average : " + str(medAvg))
        ###############################
        numLong = 0
        for x in range(long):
            #print(-x - (timeLength-currentTime))
            numLong += float(prices[-x - (timeLength-currentTime)])
        longAvg = float(numLong/long)
        #print("Medium Average : " + str(medAvg))
        ###############################
        #Signals
        if float(fastAvg) > float(longAvg) and coins == 0:
            boughtAt = float(currentPrice) + (float(currentPrice) * .00075)
            coins+=1
            #print("Bought At : " + str(currentPrice))
            
        if float(fastAvg) < float(medAvg) and coins > 0:
            soldAt = float(currentPrice) - (float(currentPrice) * .00075)
            coins-=1
            money += (soldAt - boughtAt)
            #print("Sold At : " + str(currentPrice))

        currentTime+=1

    print(money)
        
        
#uses three averages and volume
def mansonVol(timeLength, fast, med, volTime):
    currentTime = 0
    money = 0
    coins = 0
    fast = fast
    fastAvg = 0
    med = med
    medAvg = 0
    boughtAt = 0
    soldAt = 0
    volAvg = 0
    while currentTime<timeLength:
       # print(-(timeLength)+currentTime)
        currentPrice = prices[-(timeLength)+currentTime]
        currentVolume = volume[-(timeLength)+currentTime]
        
        #Average Volume for volTime
        volNum = 0
        for x in range(volTime):
            volNum += float(volume[-x - (timeLength-currentTime)])
        volAvg = float(volNum/volTime)
        
        
        ######################fast Average
        numFast = 0
        for x in range(fast):
            numFast += float(prices[-x - (timeLength-currentTime)])
        fastAvg = float(numFast/fast)
        #print("Fast Average : " + str(fastAvg))
        ###############################

        ######################med Average
        numMed = 0
        for x in range(med):
            #print(-x - (timeLength-currentTime))
            numMed += float(prices[-x - (timeLength-currentTime)])
        medAvg = float(numMed/med)
        #print("Medium Average : " + str(medAvg))
        ###############################

        #Signals
        if float(fastAvg) > float(medAvg) and float(currentVolume) > float(volAvg) and coins == 0:
            boughtAt = float(currentPrice) + (float(currentPrice) * .00075)
            coins+=1
            #print("Bought At : " + str(currentPrice))
            
        if float(fastAvg) < float(medAvg) and coins > 0:
            soldAt = float(currentPrice) - (float(currentPrice) * .00075)
            coins-=1
            money += (soldAt - boughtAt)
            #print("Sold At : " + str(currentPrice))

        currentTime+=1

    print(money)

#Buys at dip, holds for certain amount of time
def Jolde(timeLength, dipPeriod, holdTime):
    currentTime = 0
    money = 0
    coins = 0
    boughtAt = 0
    initHT = holdTime
    holdTime = holdTime
    soldAt = 0
    listValues = []

    while currentTime<timeLength:
       # print(-(timeLength)+currentTime)
        currentPrice = prices[-(timeLength)+currentTime]

        if coins >= 1:
            holdTime -= 1
        low = 999999
        for x in range(dipPeriod):
            if float(prices[-x - (timeLength-currentTime)]) < low:
                low = float(prices[-x - (timeLength-currentTime)])
        

        #Signals
        if  float(currentPrice) <= float(low) and coins == 0:
            holdTime = initHT
            boughtAt = float(currentPrice) + (float(currentPrice) * .00075)
            coins+=1
            #print("Bought At : " + str(currentPrice))
            
        if holdTime <= 0 and coins > 0:
            soldAt = float(currentPrice) - (float(currentPrice) * .00075)
            coins-=1
            money += (soldAt - boughtAt)
            #print("Sold At : " + str(currentPrice))

        currentTime+=1

        listValues.append(money)
    #plt.plot(priceCheck)
    plt.plot(listValues)
    plt.savefig("Jolde2.png")
    print(money)


def Flores(timeLength, dipPeriod, upPeriod, volTime, volTimeFast):

 
        
    currentTime = 0
    money = 0
    coins = 0
    boughtAt = 0
    volAvg = 0
    volAvgFast = 0
    priceInital = prices[-(timeLength)+currentTime]
    lastPrice = prices[-1]
    buyHoldValue= float(float(lastPrice) - float(priceInital))
    listValues = []
    soldAt = 0
    while currentTime<timeLength:
       # print(-(timeLength)+currentTime)
        currentPrice = prices[-(timeLength)+currentTime]
        priceCheck.append(currentPrice)

        currentVolume = volume[-(timeLength)+currentTime]
        
        #Average Volume for volTime
        volNum = 0
        for x in range(volTime):
            volNum += float(volume[-x - (timeLength-currentTime)])
        volAvg = float(volNum/volTime)

        volNumFast = 0
        for x in range(volTimeFast):
            volNumFast += float(volume[-x - (timeLength-currentTime)])
        volAvgFast = float(volNumFast/volTimeFast)
      
        low = 999999
        for x in range(dipPeriod):
            if float(prices[-x - (timeLength-currentTime)]) < low:
                low = float(prices[-x - (timeLength-currentTime)])

        high = 0
        for x in range(upPeriod):
            if float(prices[-x - (timeLength-currentTime)]) > high:
                high = float(prices[-x - (timeLength-currentTime)])

    
        #Signals
        if  float(currentPrice) <= float(low) and coins == 0 and float(volAvgFast) < float(volAvg):
            boughtAt = float(currentPrice) + (float(currentPrice) * .00075)
            coins+=1
          
            #print("Bought At : " + str(currentPrice))
            
        if float(currentPrice) >= float(high) and coins >= 1 or float(currentPrice) < float(boughtAt * .95) and coins >= 1:
            soldAt = float(currentPrice) - (float(currentPrice) * .00075)
            coins-=1
            money += (soldAt - boughtAt)
           
            #print("Sold At : " + str(currentPrice))

        currentTime+=1
        listValues.append(money)
    plt.plot(priceCheck)
    plt.plot(listValues)
    plt.savefig("Flores2.png")
    print("Money made/lost : " + str(money))
    print("Money made/lost if bought and hold : " + str(buyHoldValue))
    return money


def mansonPlus(timeLength, fast, med, long, volFast, volSlow):
    currentTime = 0
    money = 0
    coins = 0
    fast = fast
    fastAvg = 0
    med = med
    medAvg = 0
    longAvg = 0
    boughtAt = 0
    soldAt = 0
    volFastAvg = 0
    volSlowAvg = 0
    listValues = []

    while currentTime<timeLength:
       # print(-(timeLength)+currentTime)
        currentPrice = prices[-(timeLength)+currentTime]
        currentVolume = volume[-(timeLength)+currentTime]
        
        #Average Volume for volFast
        volFastNum = 0
        for x in range(volFast):
            volFastNum += float(volume[-x - (timeLength-currentTime)])
        volFastAvg = float(volFastNum/volFast)


        #Average Volume for volSlow
        volSlowNum = 0
        for x in range(volSlow):
            volSlowNum += float(volume[-x - (timeLength-currentTime)])
        volSlowAvg = float(volSlowNum/volSlow)
        
        ######################fast Average
        numFast = 0
        for x in range(fast):
            numFast += float(prices[-x - (timeLength-currentTime)])
        fastAvg = float(numFast/fast)
        #print("Fast Average : " + str(fastAvg))
        ###############################

        ######################med Average
        numMed = 0
        for x in range(med):
            #print(-x - (timeLength-currentTime))
            numMed += float(prices[-x - (timeLength-currentTime)])
        medAvg = float(numMed/med)
        #print("Medium Average : " + str(medAvg))
        ###############################
        numLong = 0
        for x in range(long):
            #print(-x - (timeLength-currentTime))
            numLong += float(prices[-x - (timeLength-currentTime)])
        longAvg = float(numLong/long)
        
        #Signals
        if float(fastAvg) > float(longAvg) and coins == 0:
            boughtAt = float(currentPrice) + (float(currentPrice) * .00075)
            coins+=1
            #print("Bought At : " + str(currentPrice))
            
        if float(fastAvg) < float(medAvg)and float(volFastAvg) <= float(volSlowAvg) and coins > 0:
            soldAt = float(currentPrice) - (float(currentPrice) * .00075)
            coins-=1
            money += (soldAt - boughtAt)
            #print("Sold At : " + str(currentPrice))

        currentTime+=1
        listValues.append(money)

    #Create graph
    #plt.plot(priceCheck)
    plt.plot(listValues)
    plt.savefig("mansonPlus.png")

    print(money)



#Run Test
backtest("test", 3440)

    
    
        




    


