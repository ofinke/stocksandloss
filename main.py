from scraper import stock_daily
from analyzer import Analyzer

TSLA = Analyzer(ticker='TSLA',data=stock_daily('TSLA').data)
tradeSummary = TSLA.profit(buyMethodName='Mcstoch_ut1',sellMethodName='Mcstoch',capitalForEachTrade=300,comission=2)
profitAbsolute = tradeSummary["profit[$]"].sum()
print(profitAbsolute)

