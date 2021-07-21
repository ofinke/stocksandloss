from scraper import stock_daily
from analyzer import Analyzer
import numpy as np
ticker_name = 'TMDX'
anal = Analyzer(ticker=ticker_name,data=stock_daily(ticker_name).data)

tradeSummary = anal.profit(buyMethodName='Mcstoch_ut1',sellMethodName='Mcstoch',capitalForEachTrade=400,comission=2)
profitAbsolute = tradeSummary["profit[$]"].sum()
profitRelative = tradeSummary["profit[%]"].sum()
profitByHolding = 100*((anal.data["Close"].iloc[-1]-anal.data["Close"].iloc[0])/anal.data["Close"].iloc[0])
print(tradeSummary)
print('Absolute profit during last year: ',profitAbsolute,'$')
print('Relative profit during last year: ',profitRelative,'%')
print('Relative profit by holding during last year: ',profitByHolding,'%')


