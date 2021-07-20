from scraper import stock_daily
from analyzer import Analyzer

x=stock_daily('TSLA')
print(x.data)
# TSLA = Analyzer(ticker='TSLA',data=stock_daily('TSLA').data)

# testBuy = TSLA.methodBuy_Simple()
# print(testBuy)
# testSell = TSLA.methodSell_Simple()
# print(testSell)
# TSLA.profit(buyMethodName='Simple',sellMethodName='Simple',capitalForEachTrade=5000)