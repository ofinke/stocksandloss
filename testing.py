# I just have this script for testing when developing new shit

import scraper as sc
import analyzer as anal
import indicators as ind
import numpy as np
from numpy.lib.stride_tricks import as_strided
import matplotlib.pyplot as plt
import time

# ----------------------------------------
# TESTING VOL PRICE DIVERGENCE BUY SIGNALS
stock = sc.stock_daily("TSLA")

# fit close and volume by linear function
# use rolling() to fit only certain number of days
# buy signal next day if a for volume > 0 and for price < 0

w = 10 # window
# close price
dt = stock.data["Close"].to_numpy()
ap = np.polyfit(np.arange(w), as_strided(dt, (len(dt)-w+1, w), dt.strides+dt.strides).T, deg = 1)[0]
e = np.empty(w-1)
e[:] = np.NaN
ap = np.concatenate([e, ap])
# volume
dt = stock.data["Volume"].to_numpy()
vp = np.polyfit(np.arange(w), as_strided(dt, (len(dt)-w+1, w), dt.strides+dt.strides).T, deg = 1)[0]
vp = np.concatenate([e, vp])

bs = (vp > 0) & (ap < 0)
# buy signal when true changes to false
change = np.concatenate((np.array([0]), (bs[:-1] < bs[1:]).astype("int")))

# print(len(stock.data["Close"].to_numpy()))
print(bs)



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