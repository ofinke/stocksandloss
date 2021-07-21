from scraper import stock_daily
from analyzer import Analyzer
import numpy as np
ticker_name = "AAPL"
anal = Analyzer(ticker=ticker_name,data=stock_daily(ticker_name, save=False).data)

anal.strategy(buyStrategy=['Mcstoch_ut1','Mcstoch_ut2', 'Mcstoch_ut3', 'Mcstoch_ut4'],sellStrategy=['Mcstoch'],stopLoss=False)
tradeSummary = anal.profit(capitalForEachTrade=400,comission=2)
profitAbsolute = tradeSummary["profit[$]"].sum()
profitRelative = tradeSummary["profit[%]"].sum()
profitByHolding = 100*((anal.data["Close"].iloc[-1]-anal.data["Close"].iloc[0])/anal.data["Close"].iloc[0])
print(tradeSummary)
print('Absolute profit during last year: ',np.round(profitAbsolute,2),'$')
print('Relative profit during last year: ',np.round(profitRelative,2),'%')
print('Relative profit by holding during last year: ',np.round(profitByHolding,2),'%')


