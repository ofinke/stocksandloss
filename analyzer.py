#class which stores historical daily candles for a given ticker 
#it has different methods that each generate different buy/sell signals (different swing trading strategies)
#then the final method analyzes the profitability of the buy/sell signals
import indicators
import numpy as np
class Analyzer:

  def __init__(self,*,ticker ,data):
    self.data = data
    self.ticker = ticker

  def methodBuy_Simple(self): #first trading strategy for generating buy/sell signals, todo: name the methods
    buySignal = np.zeros(self.data["Close"].size, dtype=int)
    self.result = self.data.loc[:, ["Date"]]
    fl=12
    sl=26
    sig=9
    fastema = self.data["Close"].ewm(span=fl, adjust=False).mean()
    slowema = self.data["Close"].ewm(span=sl, adjust=False).mean()
    macd = fastema - slowema
    signal = macd.ewm(span=sig, adjust=False).mean()
    zero_crossings = np.add(np.where(np.diff(np.sign(signal))>0),1) #calculates indexes where macd signal crossed zero to positive
    buySignal[zero_crossings[0]] = 1
    return buySignal
  def methodSell_Simple(self): #first trading strategy for generating buy/sell signals, todo: name the methods
    sellSignal = np.zeros(self.data["Close"].size, dtype=int)
    self.result = self.data.loc[:, ["Date"]]
    fl=12
    sl=26
    sig=9
    fastema = self.data["Close"].ewm(span=fl, adjust=False).mean()
    slowema = self.data["Close"].ewm(span=sl, adjust=False).mean()
    macd = fastema - slowema
    signal = macd.ewm(span=sig, adjust=False).mean()
    zero_crossings = np.add(np.where(np.diff(np.sign(signal))<0),1) #calculates indexes where macd signal crossed zero to negative
    sellSignal[zero_crossings[0]] = 1
    return sellSignal
  def profit(self,*,methodName,capitalForEachTrade):   #method for calculating profit, inputs: how much money is spent on each trade and the name of the trading strategy
    print("Method not yet implemented")