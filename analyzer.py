#class which stores historical daily candles for a given ticker 
#it has different methods that each generate different buy/sell signals (different swing trading strategies)
#then the final method analyzes the profitability of the buy/sell signals
import indicators
class Analyzer:

  def __init__(self,*,ticker ,data):
    self.data = data
    self.ticker = ticker

  def methodBuy_Simple(self): #first trading strategy for generating buy/sell signals, todo: name the methods
    self.result = self.data.loc[:,["Date"]]
    self.result["SMA"] = self.data["Close"].rolling(26).mean()
    return self.result
  def methodSell_Simple(self): #first trading strategy for generating buy/sell signals, todo: name the methods
    self.result = self.data.loc[:,["Date"]]
    self.result["SMA"] = self.data["Close"].rolling(26).mean()
    return self.result
  def profit(self,*,methodName,capitalForEachTrade):   #method for calculating profit, inputs: how much money is spent on each trade and the name of the trading strategy
    print("Method not yet implemented")