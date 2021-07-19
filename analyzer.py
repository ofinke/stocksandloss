#class which stores historical daily candles for a given ticker 
#it has different methods that each generate different buy/sell signals (different swing trading strategies)
#then the final method analyzes the profitability of the buy/sell signals
import indicators
class Analyzer:
  def __init__(self,ticker ,data):
    self.data = data
    self.ticker = ticker

  def method1(self): #first trading strategy for generating buy/sell signals, todo: name the methods
    print("Method not yet implemented")
  def profit(self,capitalForEachTrade, tradingStrategy):   #method for calculating profit, inputs: how much money is spent on each trade and the name of the trading strategy
    print("Method not yet implemented")