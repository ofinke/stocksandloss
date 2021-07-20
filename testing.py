# I just have this script for testing when developing new shit

import scraper as sc
import analyzer as anal
import numpy as np
import matplotlib.pyplot as plt
import time

stock = sc.stock_daily("TSLA")

test = anal.Analyzer(ticker="TSLA", data=stock.data)

start = time.time()
output = test.methodBuy_Mcstoch_ut1()
print("Buy signal calculation took " + str(np.round(time.time()-start,3)) + " sec.")