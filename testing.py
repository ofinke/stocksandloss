# I just have this script for testing when developing new shit

import scraper as sc
import analyzer as anal
import indicators as ind
import numpy as np
import matplotlib.pyplot as plt
import time

stock = sc.stock_daily("TSLA")


test = anal.Analyzer(ticker="TSLA", data=stock.data)

start = time.time()
buy1 = test.methodBuy_Mcstoch_ut1()
buy2 = test.methodBuy_Mcstoch_ut3()
buy = test.signalOr(buy1, buy2)
#output2 = test.methodSell_Mcstoch()
print("Buy signal calculation took " + str(np.round(time.time()-start,3)) + " sec.")

print(buy.sum())

plt.plot(buy)
plt.show()

# testing detect in array change

green = np.array([0,0,0,1,1,1,0,0,1,1,0,0])
red = np.array([1,1,1,0,0,0,1,1,0,0,1,1])
gchange = (green[:-1] < green[1:]).astype("int")
gchange = np.concatenate((np.array([0]), gchange))
rchange = (red[:-1] > red[1:]).astype("int")
rchange = np.concatenate((np.array([0]), rchange))

print(green)
print(red)
print(gchange)
print(rchange)

# testing array change with dataframe
mcs = ind.mcstoch(test.data, fl=12, sl=26, sig=9, price="Close", period=14, sk=2, sd=4)

print(len(np.concatenate((np.array([0]), (mcs["green"].to_numpy()[:-1] < mcs["green"].to_numpy()[1:]).astype("int")))))
print(len(mcs["green"]))
print()