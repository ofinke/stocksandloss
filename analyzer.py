#class which stores historical daily candles for a given ticker 
#it has different methods that each generate different buy/sell signals (different swing trading strategies)
#then the final method analyzes the profitability of the buy/sell signals
import indicators
import numpy as np
import pandas as pd
class Analyzer:
  trades = pd.DataFrame()
  def __init__(self,*,ticker ,data):
    self.data = data
    self.ticker = ticker

  def methodBuy_Simple(self): #first trading strategy for generating buy/sell signals, todo: name the methods
    buySignal = np.zeros(self.data["Close"].size, dtype=int)
    #signal = macd.ewm(span=sig, adjust=False).mean()
    macd = indicators.macd(self.data, 12, 26, 9, "Close")
    zero_crossings = np.add(np.where(np.diff(np.sign(macd["signal"]))>0),1) #calculates indexes where macd signal crossed zero to positive, +1 to get the correct day
    buySignal[zero_crossings[0]] = 1 
    return buySignal
  
  def methodBuy_Mcstoch_ut1(self):
    # McStoch 1 buy signal in uptrend (macd signal > 0)
    # Previous day red and today green
    buySignal = np.zeros(self.data["Close"].size, dtype=int)
    # calculate mcstoch
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=14, sk=2, sd=4)
    macd = indicators.macd(self.data, fl=12, sl=26, sig=9, price="Close")
    # find changes from red days to green days
    gchange = np.concatenate((np.array([0]), (mcs["green"].to_numpy()[:-1] < mcs["green"].to_numpy()[1:]).astype("int")))
    rchange = np.concatenate((np.array([0]), (mcs["red"].to_numpy()[:-1] > mcs["red"].to_numpy()[1:]).astype("int")))
    # create buy signal
    buySignal = gchange & rchange & (macd["signal"] > 0)
    return buySignal.astype("int").to_numpy()

  def methodBuy_Mcstoch_ut2(self):
    # McStoch 2 buy signal in uptrend
    # previous day red, today blue and close higher
    buySignal = np.zeros(self.data["Close"].size, dtype=int)
    # calculate mcstoch
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=14, sk=2, sd=4)

    return buySignal
  
  def methodBuy_Mcstoch_ut3(self):
    # McStoch 3 buy signal in uptrend (macd signal > 0)
    # previous day blue, today green 
    buySignal = np.zeros(self.data["Close"].size, dtype=int)
    # calculate mcstoch
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=14, sk=2, sd=4)
    macd = indicators.macd(self.data, fl=12, sl=26, sig=9, price="Close")
    # find changes from blue days to green days
    gchange = np.concatenate((np.array([0]), (mcs["green"].to_numpy()[:-1] < mcs["green"].to_numpy()[1:]).astype("int")))
    bchange = np.concatenate((np.array([0]), (mcs["blue"].to_numpy()[:-1] > mcs["blue"].to_numpy()[1:]).astype("int")))
    # create buy signal
    buySignal = gchange & bchange & (macd["signal"] > 0)
    return buySignal.astype("int").to_numpy()

  def methodBuy_Mcstoch_ut4(self):
    # McStoch 4 buy signal in uptrend
    # previous day blue a close < open, today blue and close > open 
    buySignal = np.zeros(self.data["Close"].size, dtype=int)
    # calculate mcstoch
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=14, sk=2, sd=4)
    
    return buySignal
  
  def methodSell_Mcstoch(self):
    # McStoch sell signal
    # red day is a sell signal
    # calculate mcstoch
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=14, sk=2, sd=4)
    return mcs["red"].to_numpy()

  def methodSell_Simple(self): #first trading strategy for generating buy/sell signals, todo: name the methods
    sellSignal = np.zeros(self.data["Close"].size, dtype=int)
    #signal = macd.ewm(span=sig, adjust=False).mean()
    macd = indicators.macd(self.data, 12, 26, 9, "Close")
    zero_crossings = np.add(np.where(np.diff(np.sign(macd["signal"]))<0),1) #calculates indexes where macd signal crossed zero to positive, +1 to get the correct day
    sellSignal[zero_crossings[0]] = 1
    return sellSignal

  def signalOr(self, signal1, signal2):
  # takes two signals and return their boolean OR
    return np.logical_or(signal1, signal2).astype("int")
  
  def signalSorter(self,buySignal,sellSignal):
    helper = 0
    zero_data = np.zeros(shape=(len(buySignal),2))
    Buy_number = 0
    d = pd.DataFrame(zero_data, columns=["Buy","Sell"])
    for j in range(0,len(buySignal)): #we go through the whole buySignal vector
      if buySignal[j]==1 and helper==0:
        d["Buy"][j]=1
        helper = 1
        Buy_number += 1       
      elif sellSignal[Buy_number-1,j]==1 and helper==1: 
        d["Sell"][j]=1
        helper = 0
    if helper == 1:
      d = d[:-1]
    return d
  def strategy(self,*,buyStrategy,sellStrategy,stopLoss):
    buyHelper = np.zeros(shape=(len(self.data["Close"]),1))
    for j in range(len(buyStrategy)): #this cycle will load all the signals from the different buy stragies and join them to one signal vector
      if buyStrategy[j] == 'Simple':
          buyHelper = self.methodBuy_Simple()
      elif buyStrategy[j] == 'Mcstoch_ut1':
          buyHelper = self.methodBuy_Mcstoch_ut1()
      elif buyStrategy[j] == 'Mcstoch_ut3':
          buyHelper = self.methodBuy_Mcstoch_ut3()    
      else:
          print('This buy method is not impplemented')                 
      if j==0:
        buySignal = buyHelper
      else:  
        buySignal = self.signalOr(buyHelper, buySignal)
    #for N buy signals, create N sell vectors where Nth column will be the sell signal for Nth buy signal, some sell methods that are independent will have copied columns
    sellHelper = np.zeros(shape=(len(self.data["Close"]),1))
    for j in range(len(sellStrategy)): #this cycle will load all the signals from the different sell stragies and join them to one signal vector
      if sellStrategy[j] == 'Simple':
          sellHelper = self.methodSell_Simple()
          sellHelper = np.repeat([sellHelper,], repeats=np.sum(buySignal), axis=0)
      elif sellStrategy[j] == 'Mcstoch':
          sellHelper= self.methodSell_Mcstoch()
          sellHelper = np.repeat([sellHelper,], repeats=np.sum(buySignal), axis=0)
      else:
          print('This buy method is not implemented')
      if j==0:
        sellSignal = sellHelper
      else:  
        sellSignal = self.signalOr(sellHelper, sellSignal)
    
    sorted_signals = self.signalSorter(buySignal,sellSignal)  
    Nbuys = np.sum(sorted_signals["Buy"])
    self.trades = pd.DataFrame(np.zeros(shape=(Nbuys.astype("int"),4)), columns=["Buy date","Buy price","Sell Date","Sell price"])
    self.trades["Buy date"] = self.data.loc[np.where(sorted_signals["Buy"]==1)[0],"Date"].reset_index(drop=True)
    self.trades["Buy price"] = self.data.loc[np.where(sorted_signals["Buy"]==1)[0],"Close"].reset_index(drop=True)
    self.trades["Sell date"] = self.data.loc[np.where(sorted_signals["Sell"]==1)[0],"Date"].reset_index(drop=True)
    self.trades["Sell price"] = self.data.loc[np.where(sorted_signals["Sell"]==1)[0],"Close"].reset_index(drop=True)
    if bool(stopLoss): #Check if the SL got triggered before the Sell date for each trade, if so, overwrite the Date and Price
      self.stopLoss()
    return  
  def profit(self,capitalForEachTrade,comission):   #method for calculating profit, inputs: how much money is spent on each trade and the name of the trading strategy
    outputFrame = pd.DataFrame(np.zeros(shape=(len(self.trades["Buy date"]),11)), columns=["buy_date","buy_price","buy_value","position","sell_date","sell_price","sell_value","comission","good_trade?","profit[%]","profit[$]"])
    outputFrame["buy_date"] = self.trades["Buy date"]
    outputFrame["buy_price"] = self.trades["Buy price"]
    outputFrame["sell_date"] = self.trades["Sell date"]
    outputFrame["sell_price"] = self.trades["Sell price"]
    outputFrame["buy_value"] = capitalForEachTrade
    outputFrame["position"] = outputFrame["buy_value"]/outputFrame["buy_price"]
    outputFrame["sell_value"] = outputFrame["position"]*outputFrame["sell_price"]
    outputFrame["comission"] = comission
    outputFrame.loc[outputFrame["sell_value"]>outputFrame["buy_value"] ,"good_trade?"] = 1
    outputFrame["profit[$]"] = outputFrame["sell_value"]-outputFrame["buy_value"]-outputFrame["comission"]
    outputFrame["profit[%]"] = 100*outputFrame["profit[$]"]/outputFrame["buy_value"]
    return outputFrame

