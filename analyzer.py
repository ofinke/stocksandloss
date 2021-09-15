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

    # ======== BUY SIGNAL METHODS ========

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
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=21, sk=3, sd=5)
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
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=21, sk=3, sd=5)
    macd = indicators.macd(self.data, fl=12, sl=26, sig=9, price="Close")
    # find changes from red day to blue day
    bchange = np.concatenate((np.array([0]), (mcs["blue"].to_numpy()[:-1] < mcs["blue"].to_numpy()[1:]).astype("int")))
    rchange = np.concatenate((np.array([0]), (mcs["red"].to_numpy()[:-1] > mcs["red"].to_numpy()[1:]).astype("int")))
    # find situations where close > open (green candle)
    gcandle = self.data["Close"] > self.data["Open"]
    buySignal = bchange & rchange & (macd["signal"] > 0) & gcandle
    return buySignal.astype("int").to_numpy()
  
  def methodBuy_Mcstoch_ut3(self):
    # McStoch 3 buy signal in uptrend (macd signal > 0)
    # previous day blue, today green 
    buySignal = np.zeros(self.data["Close"].size, dtype=int)
    # calculate mcstoch
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=21, sk=3, sd=5)
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
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=21, sk=3, sd=5)
    macd = indicators.macd(self.data, fl=12, sl=26, sig=9, price="Close")
    # find green and red candle days
    gcandle = (self.data["Close"] > self.data["Open"]).to_numpy().astype("int")
    rcandle = (self.data["Close"] < self.data["Open"]).to_numpy().astype("int")
    # find changes from red candle days to green candle days
    gchange = np.concatenate((np.array([0]), gcandle[:-1] < gcandle[1:])).astype("int")
    rchange = np.concatenate((np.array([0]), rcandle[:-1] > rcandle[1:])).astype("int")
    # create buy signal
    buySignal = gchange & rchange & (macd["signal"] > 0) & (mcs["blue"])
    return buySignal.astype("int").to_numpy()

  def methodBuy_Mcstoch_dt1(self):
    # McStoch buy signal in downtrend
    # previous day close pod ema50 and today close > ema50 and green or blue day
    buySignal = np.zeros(self.data["Close"].size, dtype=int)
    # calculate required indicators
    mcs = indicators.mcstoch(self.data, fl=12, sl=26, sig=9, price="Close", period=21, sk=3, sd=5)
    macd = indicators.macd(self.data, fl=12, sl=26, sig=9, price="Close")
    ma = indicators.ema(self.data, 50)
    # find days where ema 50 > close 
    abma = (ma["EMA"] > self.data["Close"]).to_numpy().astype("int")
    # find change days when close > ema50
    machange = np.concatenate((np.array([0]), abma[:-1] > abma[1:])).astype("int")
    # create buy signal
    buySignal = (macd["signal"] < 0).astype("int") & machange & (mcs["blue"] | mcs["green"])
    return buySignal.astype("int").to_numpy()
  
  def methodBuy_pvdiv(self):
    w = 10 # window
    # close price
    dt = self.data["Close"].to_numpy()
    ap = np.polyfit(np.arange(w), np.lib.stride_tricks.as_strided(dt, (len(dt)-w+1, w), dt.strides+dt.strides).T, deg = 1)[0]
    e = np.empty(w-1)
    e[:] = np.NaN
    ap = np.concatenate([e, ap])
    # volume
    dt = self.data["Volume"].to_numpy()
    vp = np.polyfit(np.arange(w), np.lib.stride_tricks.as_strided(dt, (len(dt)-w+1, w), dt.strides+dt.strides).T, deg = 1)[0]
    vp = np.concatenate([e, vp])

    bs = (vp > 0) & (ap < 0)
    # buy signal when true changes to false
    change = np.concatenate((np.array([0]), (bs[:-1] < bs[1:]).astype("int")))
    return change

  def mb_stoch(self, period=14, sk=3, sd=5, treshold=20, tcross="d"):
    # buy signal when k crosses d and is above certain treshold
    so = indicators.stoch(self.data, period=period, sk=sk, sd=sd)
    conditions = np.logical_and((so["k"] > so["d"]).to_numpy(), (so[tcross] >= treshold).to_numpy())
    return np.concatenate((np.array([0]), (conditions[:-1] < conditions[1:]))).astype("int")

  def mb_smacross(self, fast=5, slow=10):
    f = indicators.sma(self.data, w=fast)["SMA"].to_numpy()
    s = indicators.sma(self.data, w=slow)["SMA"].to_numpy()
    condition = f > s
    res = np.concatenate((np.array([0]), (condition[:-1] < condition[1:]))).astype("int")
    return res

# ======== SELL SIGNAL METHODS ========

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

  def ms_smacross(self, fast=5, slow=10):
    f = indicators.sma(self.data, w=fast)["SMA"].to_numpy()
    s = indicators.sma(self.data, w=slow)["SMA"].to_numpy()
    condition = f < s
    # np.concatenate((np.array([0]), (condition[:-1] < condition[1:]))).astype("int")
    # currently outputs sell signal everytime this condtion is met
    return condition.astype("int")

  def ms_emacross(self, fast=5, slow=10):
    f = indicators.ema(self.data, w=fast)["EMA"].to_numpy()
    s = indicators.ema(self.data, w=slow)["EMA"].to_numpy()
    condition = f < s
    # np.concatenate((np.array([0]), (condition[:-1] < condition[1:]))).astype("int")
    # currently outputs sell signal everytime this condtion is met
    return condition.astype("int")

  # takes buy signals from self.trades and checks if stop loss is triggered
  # if its triggered sooner than defined stop loss, overwrites it
  def stopLoss(self,*,sl):
    for i in range(len(self.trades["Buy price"])):
      sl_price = self.trades["Buy price"][i] - sl*self.trades["Buy price"][i]
      wherePriceLower = np.where(self.data["Low"]<sl_price)[0]
      whereDateLater = np.where(self.data["Date"]>self.trades["Buy date"][i])[0]
      afterBuy = np.where(wherePriceLower >= whereDateLater[0])[0]
      if afterBuy.size != 0 and self.data["Date"][wherePriceLower[afterBuy[0]]]<=self.trades["Sell date"][i]:
        self.trades.loc[i,["Sell date"]] = self.data["Date"][wherePriceLower[afterBuy[0]]]
        self.trades.loc[i,["Sell price"]] = sl_price
    return
  def profitTaker(self,*,profitValue):
    for i in range(len(self.trades["Buy price"])):
      profit_price = self.trades["Buy price"][i] + profitValue*self.trades["Buy price"][i]
      wherePriceHigher = np.where(self.data["High"]>profit_price)[0]
      whereDateLater = np.where(self.data["Date"]>self.trades["Buy date"][i])[0]
      afterBuy = np.where(wherePriceHigher >= whereDateLater[0])[0]
      if afterBuy.size != 0 and self.data["Date"][wherePriceHigher[afterBuy[0]]]<=self.trades["Sell date"][i]:
        self.trades.loc[i,["Sell date"]] = self.data["Date"][wherePriceHigher[afterBuy[0]]]
        self.trades.loc[i,["Sell price"]] = profit_price
    return 
  
  def signalOr(self, signal1, signal2):
    # takes two signals and return their boolean OR
    return np.logical_or(signal1, signal2).astype("int")
  
  def signalSorter(self,buySignal,sellSignal,repeated_buys):
    if repeated_buys:
      helper = 0
      zero_data = np.zeros(shape=(np.sum(buySignal),2))
      Buy_number = 0
      d = pd.DataFrame(zero_data, columns=["Buy","Sell"])
      for j in range(0,len(buySignal)): #we go through the whole buySignal vector
        if buySignal[j]==1:
          k = j
          d.loc[Buy_number,["Buy"]]=j      
          while sellSignal[Buy_number,k]==0: 
            k = k+1 
            if k>len(sellSignal[Buy_number,])-1: 
              break#we save the index in the sell signal vector where it is 1 after the buy
          if k<=len(sellSignal[Buy_number,])-1:
            d.loc[Buy_number,["Sell"]]=k
          Buy_number += 1         
    else:
      helper = 0
      zero_data = np.zeros(shape=(np.sum(buySignal),2))
      Buy_number = 0
      d = pd.DataFrame(zero_data, columns=["Buy","Sell"])
      for j in range(0,len(buySignal)-1): #we go through the whole buySignal vector
        if buySignal[j]==1 and helper==0:
          helper = 1
          k = j
          d.loc[Buy_number,["Buy"]]=j      
        if helper==1 and sellSignal[Buy_number,j+1]==1:
          d.loc[Buy_number,["Sell"]]=j+1
          helper = 0
          Buy_number += 1
    while d["Sell"].iloc[-1]==0: d = d[:-1]   #we delete the last rows where the trades were not yet closed
    return d
  
  def strategy(self,sorted_signals,*,stopLoss=False,stopLossValue=0,profitTaker=False,profitTakerValue=0):
    Nbuys = len(sorted_signals["Buy"])
    self.trades = pd.DataFrame(np.zeros(shape=(Nbuys,4)), columns=["Buy date","Buy price","Sell date","Sell price"])
    self.trades["Buy date"] = self.data.loc[sorted_signals["Buy"],"Date"].reset_index(drop=True)
    self.trades["Buy price"] = self.data.loc[sorted_signals["Buy"],"Close"].reset_index(drop=True)
    self.trades["Sell date"] = self.data.loc[sorted_signals["Sell"],"Date"].reset_index(drop=True)
    self.trades["Sell price"] = self.data.loc[sorted_signals["Sell"],"Close"].reset_index(drop=True)
    # Check if the SL got triggered before the Sell date for each trade, if so, overwrite the Date and Price
    if bool(stopLoss):
      self.stopLoss(sl=stopLossValue)
    if bool(profitTaker):
      self.profitTaker(profitValue=profitTakerValue)  
    return  
  def bouncesFrom_SMA(self,sma):
    smaLine = indicators.sma(self.data,sma,price="Close")
    bounces = np.where(np.abs(self.data["Low"]-smaLine["SMA"])/smaLine["SMA"]<0.01)[0]
    for i in range(1,bounces.size):
      if bounces[i] - bounces[i-1] < 10:
        bounces = np.delete(bounces,i)
    return bounces
  def profit(self,capitalForEachTrade,comission):   #method for calculating profit, inputs: how much money is spent on each trade and the name of the trading strategy
    outputFrame = pd.DataFrame(np.zeros(shape=(len(self.trades["Buy date"]),11)), columns=["Buy date","Buy price","Buy value","Position","Sell date","Sell price","Sell value","Comission","Good trade?","Profit[$]","Profit[%]"])
    outputFrame["Buy date"] = self.trades["Buy date"]
    outputFrame["Buy price"] = self.trades["Buy price"]
    outputFrame["Sell date"] = self.trades["Sell date"]
    outputFrame["Sell price"] = self.trades["Sell price"]
    outputFrame["Buy value"] = capitalForEachTrade
    outputFrame["Position"] = outputFrame["Buy value"]/outputFrame["Buy price"]
    outputFrame["Sell value"] = outputFrame["Position"]*outputFrame["Sell price"]
    outputFrame["Comission"] = comission
    outputFrame.loc[outputFrame["Sell value"]>outputFrame["Buy value"] ,"Good trade?"] = 1
    outputFrame["Profit[$]"] = outputFrame["Sell value"]-outputFrame["Buy value"]-outputFrame["Comission"]
    outputFrame["Profit[%]"] = 100*(outputFrame["Profit[$]"]/outputFrame["Buy value"])
    return outputFrame