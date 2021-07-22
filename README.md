# Stocks & Loss
Framework for developing and backtesting strategies for swing trading based on technical analysis indicators. Compromises of multiple self-functioning blocks. ```scraper.py``` holds class for storing, loading and scraping stock data from [yahoo finance](https://finance.yahoo.com/). ```indicators.py``` holds multiple functions for technical indicators and ```analyzer.py``` holds trading strategies and methods for evaluating trades.

### Requirements
* pandas
* numpy
* yfinance

# Scraper

Scraped data can be stored into corresponding csv file, if called on the same stock again, it loads the data from the csv file and updates them if required. Saving data can be disabled if desired. Currently, scraper automatically scrapes data from last year. 

Class | Parameters | Outputs 
------|------------|--------
```stock_daily()``` | am too lazy now | am too lazy now

### Known issues
* Data are always from the day before, this is property of the yfinance package for data scraping

# Indicators

File containing several functions for calculating basic technical analysis indicators. List of implemented indicators follows, definitions for more complex indicators are taken from investopedia or URL link is present in the description. Output is always defined as a DataFrame with first column ```["Date"]``` copied from the stock data and other columns corresponding to the indicator are written in the "Output columns" column.

Name | Function | Parameters | Output columns | Description
-----|----------|------------|---------|-------------
SMA | ```sma()``` | w: length <br> price: which price column to use, default = ```"Close"``` | ```"SMA"``` | Simple moving average
EMA | ```ema()``` | same as ```sma()``` | ```"EMA"``` | Exponential moving average
MACD | ```macd()``` | fl: fast line length, def = ```12``` <br> sl: slow line length, def = ```26``` <br> sig: signal length, def = ```9``` <br> price: same as ```sma()``` | ```"macd", "signal", "histogram"``` | MACD (Moving average convergence divergence) <br> as defined by [Investopedia](https://www.investopedia.com/terms/m/macd.asp)
Stoch | ```stoch()``` | period: length of data period, def = ```14``` <br> sk: k line smoothing, def = ```2``` <br> sd: d line smoothing, def = ```4``` | ```"k", "d"``` | Stochastic Oscillator. Code copied from [here](https://www.learnpythonwithrune.org/pandas-calculate-the-stochastic-oscillator-indicator-for-stocks/)
McStoch | ```mcstoch()``` | Same inputs as ```macd()``` and ```stoch()``` | ```"green", "yellow", "red", "blue"``` | Combination of macd and stoch indicators to filter opportunities
Bollinger bands | ```bollbands()``` | period: length of data period, def = ```20``` <br> stdn: # of std multipliers, def = ```2``` | ```"lower", "upper"``` | Bollinger bands as defined by [investopedia](https://www.investopedia.com/terms/b/bollingerbands.asp)

Other indicators will be added in the future

# Analyzer