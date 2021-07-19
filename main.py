from scraper import stock_daily
from analyzer import Analyzer
TSLA = Analyzer('TSLA',stock_daily('TSLA').data)
print(TSLA.ticker)