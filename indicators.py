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
import time

# SIMPLE MOVING AVERAGE
def sma(x, w, price="Close"):
    # x - dataframe from scraper
    # w - size of sma
    # price - strong, name of which column to use, default "Close"
    result = x.loc[:,["Date"]]
    result["SMA"] = x[price].rolling(w).mean()
    return result

# EXPONENTIAL MOVING AVERAGE
def ema(x, w, price="Close"):
    # x - dataframe from scraper
    # w - size of ema
    # price - strong, name of which column to use, default "Close"
    result = x.loc[:, ["Date"]]
    result["EMA"] = x[price].ewm(span=w, adjust=False, min_periods=w).mean()
    return result

# MACD
def macd(x, fl=12, sl=26, sig=9, price="Close"):
    result = x.loc[:, ["Date"]]
    fastema = x[price].ewm(span=fl, adjust=False).mean()
    fastema[:fl] = np.NaN
    slowema = x[price].ewm(span=sl, adjust=False).mean()
    slowema[:sl] = np.NaN
    result["macd"] = fastema - slowema
    result["signal"] = result["macd"].ewm(span=sig, adjust=False).mean()
    result["histogram"] = result["macd"] - result["signal"]
    return result

# STOCHASTIC OSCILLATOR
def stoch(x, period=14, sk=2, sd=4):
    result = x.loc[:, ["Date"]]
    
    high = x["High"].rolling(period).max()
    low = x["Low"].rolling(period).min()

    result["k"] = (((x["Close"] - low)*100)/(high - low)).rolling(sk).mean()
    result["d"] = result["k"].rolling(sd).mean()
    
    return result

# MCSTOCH
def mcstoch(x, fl=12, sl=26, sig=9, price="Close", period=14, sk=2, sd=4):
    result = x.loc[:, ["Date"]]

    md = macd(x, fl=fl, sl=sl, sig=sig, price=price)
    so = stoch(x, period=period, sk=sk, sd=sd)

    # comparing macd with signal
    result["md_good"] = md["macd"].gt(md["signal"])
    # comparing stoch k with k
    result["so_good"] = so["k"].gt(so["d"])

    # create colors
    result["green"] = result["md_good"].eq(True) & result["so_good"].eq(True)
    result["green"] = result["green"].astype("int")
    result["yellow"] = result["md_good"].gt(result["so_good"]).astype("int")
    result["blue"] = result["so_good"].gt(result["md_good"]).astype("int")
    result["red"] = result["md_good"].eq(False) & result["so_good"].eq(False)
    result["red"] = result["red"].astype("int")

    return result

# Bollinger Bands as defined at https://www.investopedia.com/terms/b/bollingerbands.asp
def bollbands(x, period=20, stdn=2):
    result = x.loc[:, ["Date"]]

    tp = (x["High"] + x["Low"] + x["Close"])/3  # typical price
    ma = tp.rolling(period).mean()
    std = tp.rolling(period).std()

    result["lower"] = ma - stdn*std
    result["upper"] = ma + stdn*std

    return result

# Relative Strength Index
def rsi(x, w=14, price="Close", ema=True):
    result = x.loc[:, ["Date"]]
    delta = x[price].diff()
    # Make two series: one for lower closes and one for higher closes
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    if ema is True:
        # Use exponential moving average
        ma_up = up.ewm(span=w, adjust=False, min_periods=w).mean()
        ma_down = down.ewm(span=w, adjust=False, min_periods=w).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(w).mean()
        ma_down = down.rolling(w).mean()
    # calculate RSI
    rs = ma_up / ma_down
    result["RSI"] = 100 - (100/(1 + rs))
    return result 

# Volume Flow Indicator
# tbh I don't understand this calculation much
# Corresponds to lazybears implementation on tradingview
def vfi(x, period=40, coef=0.2, vcoef=2.5, ssmooth=5):
    
    result = x.loc[:, ["Date"]]

    tp = (x["High"] + x["Low"] + x["Close"])/3  # typical price
    inter = np.log(tp) - np.log(np.concatenate([np.array([np.NaN]),tp[:-1]]))
    vinter = inter.rolling(30).std()
    cutoff = coef * vinter * x["Close"]
    vave = x["Volume"].rolling(period).mean().shift(1)

    vmax = vave * vcoef
    vc = x["Volume"].where(x["Volume"] < vmax, vmax) # replaces volume spikes by max allowed volume 

    mf = tp - np.concatenate([np.array([np.NaN]),tp[:-1]]) # same as inter, without the logs
    vcp = vc.where(mf > cutoff, -vc.where(mf < -cutoff, 0))
    vcp[:period] = np.NaN # put NaNs in the beginning as they are replaced by 0 due to bool logic

    result["vfi"] = (vcp.rolling(period).sum() / vave).rolling(3).mean()
    result["vfi_smooth"] = result["vfi"].ewm(span=ssmooth, adjust=False, min_periods=ssmooth).mean()
    result["histogram"] = result["vfi"] - result["vfi_smooth"]

    return result

# TESTING RUNTIME
def main():
    # import only for this function
    stock = sc.stock_daily("NET", save=False)
    start = time.time()
    x = ema(stock.data, 26)
    print("EMA calculation took " + str(np.round(time.time()-start,3)) + " sec.")
    
    start = time.time()
    y = sma(stock.data, 50)
    print("SMA calculation took " + str(np.round(time.time()-start,3)) + " sec.")
    
    start = time.time()
    md = macd(stock.data)
    print("MACD calculation took " + str(np.round(time.time()-start,3)) + " sec.")

    start = time.time()
    so = stoch(stock.data, period=21, sk=3, sd=5)
    print("Stochastic osc. calculation took " + str(np.round(time.time()-start,3)) + " sec.")

    start = time.time()
    ms = mcstoch(stock.data)
    print("McStoch calculation took " + str(np.round(time.time()-start,3)) + " sec.")

    start = time.time()
    bb = bollbands(stock.data)
    print("Bollinger bands calculation took " + str(np.round(time.time()-start,3)) + " sec.")

    start = time.time()
    rs = rsi(stock.data)
    print("RSI calculation took " + str(np.round(time.time()-start,3)) + " sec.")

    fig, ax = plt.subplots(nrows=5)
    # plot stock + sma / ema
    ax[0].plot(stock.data["Close"], label="Close")
    ax[0].plot(bb["lower"], label="bb low")
    ax[0].plot(bb["upper"], label="bb upper")
    # ax[0].set(xlim=(200, 250))
    ax[0].legend()
    # plot macd
    ax[1].plot(md["macd"], label="macd")
    ax[1].plot(md["signal"], label="signal")
    # ax[1].set(xlim=(200, 250))
    ax[1].legend()
    # plot stochastic oscillator
    ax[2].plot(so["k"], label="k")
    ax[2].plot(so["d"], label="d")
    ax[2].set(xlim=(0, 250))
    ax[2].legend()
    # plot McStoch
    ax[3].scatter(ms.index, ms["green"], color="green", marker="1", alpha=0.5)
    ax[3].scatter(ms.index, ms["blue"], color="blue", marker="1", alpha=0.5)
    ax[3].scatter(ms.index, ms["yellow"], color="yellow", marker="1", alpha=0.5)
    ax[3].scatter(ms.index, ms["red"], color="red", marker="1", alpha=0.5)
    ax[3].set(ylim=(0.9, 1.1))
    # plot rsi
    ax[4].plot(rs["RSI"])
    plt.show()
    return

if __name__ == "__main__":
    main()