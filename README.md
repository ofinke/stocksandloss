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
* Data are always from the day before, this is property of the yfinance package for data scraping

# Indicators

File containing several functions for calculating basic technical analysis indicators

### Known issues
* For some reason I didn't manage to plot results from mcstoch in the testing routine, mostly as I'm lazy, but the calculation should be good.

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
* result: DataFrame with "Date", "macd", "signal" and "histogram" columns

## stoch()
Stochastic Oscillator, copied from https://www.learnpythonwithrune.org/pandas-calculate-the-stochastic-oscillator-indicator-for-stocks/

Inputs:
* x: DataFrame with stock data
* period: period for data comparison, default = 14
* sk: smoothing of k line, default = 2
* sd: smoothing of d line, default = 4

Output:
* result: DataFrame with "Date", "macd", "signal" and "histogram" columns

## mcstoch()
Color indicator based on combination of macd and stochastic oscillator data, not yet implemnted

Inputs:
* x: DataFrame with stock data
* same settings as for macd and stochastic oscillator

output:
* result: DataFrame with "Date", "green", "blue", "yellow" and "red" columns (colors are represented as integers 1 and 0)
