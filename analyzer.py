#class which stores historical daily candles for a given ticker 
#it has different methods that each generate different buy/sell signals (different swing trading strategies)
#then the final method analyzes the profitability of the buy/sell signals
import indicators
import numpy as np
import pandas as pd
class Analyzer:

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
  def methodSell_Simple(self): #first trading strategy for generating buy/sell signals, todo: name the methods
    sellSignal = np.zeros(self.data["Close"].size, dtype=int)
    #signal = macd.ewm(span=sig, adjust=False).mean()
    macd = indicators.macd(self.data, 12, 26, 9, "Close")
    zero_crossings = np.add(np.where(np.diff(np.sign(macd["signal"]))<0),1) #calculates indexes where macd signal crossed zero to positive, +1 to get the correct day
    sellSignal[zero_crossings[0]] = 1
    return sellSignal
  def signalSorter(self,buySignal,sellSignal):
    helper = 0
    zero_data = np.zeros(shape=(len(buySignal),2))
    d = pd.DataFrame(zero_data, columns=["buy","sell"])
    for j in range(0,len(buySignal)):
      if buySignal[j]==1&helper==0:
        d["buy"][j]=1
        helper = 1
      elif sellSignal[j]==1&helper==1: 
        d["sell"][j]=1
        helper = 0
    return d
    
  def profit(self,*,buyMethodName,sellMethodName,capitalForEachTrade):   #method for calculating profit, inputs: how much money is spent on each trade and the name of the trading strategy
    if buyMethodName == 'Simple':
        buySignal = self.methodBuy_Simple()
    else:
        print('This method is not impplemented')    
    if sellMethodName == 'Simple':    
        sellSignal = self.methodSell_Simple()
    else:
        print('This method is not implemented')    
    sorted_signals = self.signalSorter(buySignal,sellSignal)    
    print(sorted_signals)

