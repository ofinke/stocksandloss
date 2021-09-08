# I just have this script for testing when developing new shit

import scraper as sc
import analyzer as anal
import indicators as ind
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import as_strided
import matplotlib.pyplot as plt
import time
import yfinance as yf

# ----------------------------------------
ar = np.zeros(10)
ar[2] = 1
ar[6] = 1
ar = ar.astype(bool)
last = np.squeeze(np.where(ar == True))[-1]

stock = sc.stock_daily("TSLA", save=False)
print()


# ----------------------------------------
# writing VFI

# lol = np.array([1,2,3,4])

# print(lol)
# print(np.concatenate([np.array([np.NaN]),lol[:-1]]))

# print(lol - np.concatenate([np.array([np.NaN]),lol[:-1]]))

# settings
# coef = 0.2
# vcoef = 2.5
# w = 40

# stock = sc.stock_daily("TSLA", save=False)

# tp = (stock.data["High"] + stock.data["Low"] + stock.data["Close"])/3  # typical price
# inter = np.log(tp) - np.log(np.concatenate([np.array([np.NaN]),tp[:-1]]))
# vinter = inter.rolling(30).std()
# cutoff = coef * vinter * stock.data["Close"]
# vave = stock.data["Volume"].rolling(w).mean().shift(1)

# vmax = vave * vcoef
# vc = stock.data["Volume"].where(stock.data["Volume"] < vmax, vmax) # replaces volume spikes by max allowed volume 

# mf = tp - np.concatenate([np.array([np.NaN]),tp[:-1]]) # same as inter, without the logs
# vcp = vc.where(mf > cutoff, -vc.where(mf < -cutoff, 0))
# vcp[:w] = np.NaN # put NaNs in the beginning as they are replaced by 0 due to bool logic

# vfi = (vcp.rolling(w).sum() / vave).rolling(3).mean()
# vfiema = vfi.ewm(span=5, adjust=False, min_periods=5).mean()
# histo = vfi - vfiema

# print(vfi)
# print(vfiema)
# print(histo)

# plt.plot(stock.data["Volume"])
# plt.plot(vc)
# plt.plot(vcp)

# fig, ax = plt.subplots(nrows=2)

# ax[0].plot(stock.data["Close"])
# ax[0].set_xlim([0, stock.data.shape[0]])

# ax[1].plot(vfi)
# ax[1].plot(vfiema)
# ax[1].plot(histo)
# ax[1].set_xlim([0, stock.data.shape[0]])

# plt.show()

# ----------------------------------------
# building buy sell strategy based on stochastic oscilator nad up/down trend
# stock = sc.stock_daily("TSLA", save=False)

# f = ind.sma(stock.data, w=5)["SMA"].to_numpy()
# s = ind.sma(stock.data, w=10)["SMA"].to_numpy()

# condition = f < s
# change = np.concatenate((np.array([0]), (condition[:-1] < condition[1:]))).astype("int")

# print()

# ----------------------------------------
# building buy sell strategy based on sma crosses
# stock = sc.stock_daily("TSLA", save=False)

# f = ind.sma(stock.data, w=5)["SMA"].to_numpy()
# s = ind.sma(stock.data, w=10)["SMA"].to_numpy()

# condition = f > s
# res = np.concatenate((np.array([0]), (condition[:-1] < condition[1:]))).astype("int")
# i = np.squeeze(np.argwhere(res==1))

# fig, ax = plt.subplots(nrows=2)
# ax[0].plot(stock.data["Close"])
# ax[0].set_xlim([0, stock.data.shape[0]])
# ax[1].plot(f)
# ax[1].plot(s)
# ax[1].scatter(i, f[i])
# ax[1].set_xlim([0, stock.data.shape[0]])
# plt.show()

# condition = f < s
# change = np.concatenate((np.array([0]), (condition[:-1] < condition[1:]))).astype("int")


# # ----------------------------------------
# # TESTING VOL PRICE DIVERGENCE BUY SIGNALS
# stock = sc.stock_daily("TSLA")
# # fit close and volume by linear function
# # use rolling() to fit only certain number of days
# # buy signal next day if a for volume > 0 and for price < 0
# w = 10 # window
# # close price
# dt = stock.data["Close"].to_numpy()
# ap = np.polyfit(np.arange(w), as_strided(dt, (len(dt)-w+1, w), dt.strides+dt.strides).T, deg = 1)[0]
# e = np.empty(w-1)
# e[:] = np.NaN
# ap = np.concatenate([e, ap])
# # volume
# dt = stock.data["Volume"].to_numpy()
# vp = np.polyfit(np.arange(w), as_strided(dt, (len(dt)-w+1, w), dt.strides+dt.strides).T, deg = 1)[0]
# vp = np.concatenate([e, vp])
# bs = (vp > 0) & (ap < 0)
# # buy signal when true changes to false
# change = np.concatenate((np.array([0]), (bs[:-1] < bs[1:]).astype("int")))
# # print(len(stock.data["Close"].to_numpy()))
# print(bs)

# ----------------------------------------
# stock = sc.stock_daily("TSLA")
# test = anal.Analyzer(ticker="TSLA", data=stock.data)

# start = time.time()
# buy = test.methodBuy_Mcstoch_ut4()

#output2 = test.methodSell_Mcstoch()
# print("Buy signal calculation took " + str(np.round(time.time()-start,3)) + " sec.")
# print(buy.sum())
# plt.plot(buy)
# plt.show()

# testing detect in array change
# green = np.array([0,0,0,1,1,1,0,0,1,1,0,0])
# red = np.array([1,1,1,0,0,0,1,1,0,0,1,1])
# gchange = (green[:-1] < green[1:]).astype("int")
# gchange = np.concatenate((np.array([0]), gchange))
# rchange = (red[:-1] > red[1:]).astype("int")
# rchange = np.concatenate((np.array([0]), rchange))

# print(green)
# print(red)
# print(gchange)
# print(rchange)

# testing array change with dataframe
# mcs = ind.mcstoch(test.data, fl=12, sl=26, sig=9, price="Close", period=14, sk=2, sd=4)

# print(len(np.concatenate((np.array([0]), (mcs["green"].to_numpy()[:-1] < mcs["green"].to_numpy()[1:]).astype("int")))))
# print(len(mcs["green"]))
# print()