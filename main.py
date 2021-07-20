from scraper import stock_daily
from analyzer import Analyzer

TSLA = Analyzer(ticker='TSLA',data=stock_daily('TSLA').data)
TSLA.profit(buyMethodName='Simple',sellMethodName='Simple',capitalForEachTrade=200)