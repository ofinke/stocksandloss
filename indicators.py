# ANALYZER
# group of functions to analyze stock data
# all functions work followingly:
# input:
#   dataframe with stock data 
# output:
#   new dataframe with indicators

# IMPORTS
import pandas as pd
import numpy as np
import scraper as sc
import matplotlib.pyplot as plt

# SIMPLE MOVING AVERAGE
def sma(x, w, price="Close"):
    # x - dataframe from scraper
    # w - size of sma
    # price - strong, name of which column to use, default "Close"
    res = np.convolve(x[price], np.ones(w), 'valid') / w
    ma = np.empty(len(x[price])-len(res))
    ma[:] = np.NaN
    result = x.loc[:,["Date"]]
    result["SMA"] = np.insert(res, 0, ma, axis=0)
    return result

# EXPONENTIAL MOVING AVERAGE
def ema(x, w, price="Close"):
    # x - dataframe from scraper
    # w - size of ema
    # price - strong, name of which column to use, default "Close"
    result = x.loc[:, ["Date"]]
    result["EMA"] = x[price].ewm(span=w, adjust=False).mean()
    return result

# MACD
def macd(x, fl=12, sl=26, sig=9, price="Close"):
    result = x.loc[:, ["Date"]]
    fastema = x[price].ewm(span=fl, adjust=False).mean()
    slowema = x[price].ewm(span=sl, adjust=False).mean()
    result["macd"] = fastema - slowema
    result["signal"] = result["macd"].ewm(span=sig, adjust=False).mean()
    result["histogram"] = result["macd"] - result["signal"]
    return result

# STOCHASTIC OSCILLATOR
def stoch(x, period=14, sk=2, sd=9):
    result = x.loc[:, ["Date"]]
    return result

# MCSTOCH
def mcstoch(x):

    return result

# TESTING RUNTIME
def main():
    # import only for this function
    stock = sc.stock_daily("TSLA")
    x = ema(stock.data, 26)
    y = sma(stock.data, 50)
    md = macd(stock.data)

    fig, ax = plt.subplots(nrows=2)
    # plot stock + sma / ema
    ax[0].plot(stock.data["Close"], label="Close")
    ax[0].plot(x["EMA"], label="EMA26")
    ax[0].plot(y["SMA"], label="SMA50")
    ax[0].legend()
    # plot macd
    ax[1].plot(md["macd"], label="macd")
    ax[1].plot(md["signal"], label="signal")
    ax[1].legend()
    plt.show()
    return

if __name__ == "__main__":
    main()