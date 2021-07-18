# Stocks & Loss
 Scrapping and analysis of stocks data.

## Requirements
* pandas
* numpy
* yfinance

and some others


# Scraper

Description of scraper.py for scraping data from yahoo finance using yfinance. Scraper automatically downloads data from last year and stores them in csv, which it also keeps updated.

## stock_daily()

Inputs
* ticker: string of stock ticker as used on the stock exchange

Outputs
* self.data: pandas DataFrame with following columns: Date (string), Open (float), High (float), Low (float), Close (float), Volume (int?). 

class saves scraped data into csv file named "ticker"_daily.csv, when called again, it opens data from this csv file and updates them according to dates.

### Known issues
* Finish updating data correctly. There are some things I'm not happy about. The scraped downloads last data from day before (even if the market is already closed), which causes some issues during the weekend. For example, if I say the scraper to download data from Friday 16. to Sunday 18., it downloads Thursday 17. and Friday 18. 

# Indicators

File containing several functions for calculating basic technical analysis indicators

## sma()
calculates simple moving average

Inputs:
* x: DataFrame with stock data
* w: length of the sma
* price: string which corresponds to column to use from x, default "Close"

Output
* result: DataFrame with "Date" and "SMA" columns

## ema()
calculates exp moving average

Inputs:
* x: DataFrame with stock data
* w: length of the sma
* price: string which corresponds to column to use from x, default "Close"

Output
* result: DataFrame with "Date" and "EMA" columns

## macd()
Calculates MACD

Inputs:
* x: DataFrame with stock data
* fl: length of the fast line, default = 12
* sl: length of the slow line, default = 26
* sig: length of the signal, default = 9
* price: string which corresponds to column to use from x, default "Close"

Output:
* result: DataFrame with "Date, "macd", "signal" and "histogram" columns

## stoch()
Stochastic Oscillator, not yet implemented