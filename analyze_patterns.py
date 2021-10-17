# imports 
import pandas as pd
import numpy as np
import scipy.signal as ss
import scraper as sc
import indicators as ind
import analyze_patterns as ap
import datetime as dt
import matplotlib.pyplot as plt

def filter_trend(data, sensitivity=2):
    filtered_close = ind.ema(data, 3, price="Close")["EMA"].to_numpy()
    bollb = ind.bollbands(data, stdn=1)
    bollb["dif"] = bollb["upper"] - bollb["lower"]
    sensitivity = bollb["dif"].mean()/sensitivity
    # determine points of interest
    top_points = ss.find_peaks(filtered_close, prominence=sensitivity)[0]
    bottom_points = ss.find_peaks(-filtered_close, prominence=sensitivity)[0]
    # create table with points of interest
    poi = np.sort(np.concatenate((top_points, bottom_points)))
    test = np.repeat(poi[1:], repeats=2)
    poi = np.concatenate([[poi[0]], np.repeat(poi[1:], repeats=2), [data.shape[0]-1]])
    p1 = poi[::2]
    p2 = poi[1::2]
    val1 = filtered_close[poi[::2]]
    val2 = filtered_close[poi[1::2]]
    # RESULT DATAFRAME
    # p1 - entry point
    # p2 - exit point
    # val1 - entry point filtered price
    # val2 - exit point filtered price
    # length - length of the trend in days
    # uptrend - bool, true if uptrend
    # fit - a in ax+b, b is p1
    # potential - % entry close to exit close
    # ppd - potential per day - average change per day
    # error - calculated as average distance of the lin fit from the close price
    # risk - worst possible loss from entry (- for long, + for short)

    reg = pd.DataFrame({"p1":p1, "p2":p2, "val1": val1, "val2": val2})
    del p1, p2, val1, val2
    reg["length"] = reg["p2"] - reg["p1"]
    reg["uptrend"] = reg["val1"] < reg["val2"]
    reg["fit"] = np.NaN
    reg["std"] = np.NaN
    reg["risk_%"] = np.NaN
    reg["potential_%"] = ((data.loc[reg["p2"],"Close"].to_numpy()/data.loc[reg["p1"],"Close"].to_numpy()-1)*100)
    reg["ppd_%"] = reg["potential_%"]/reg["length"]
    # fit and risk
    for i in reg.index:
        # calculate a in ax + b
        x = np.concatenate([[reg.loc[i,"p1"]], [reg.loc[i,"p2"]]])
        y = np.concatenate([[reg.loc[i,"val1"]], [reg.loc[i,"val2"]]])
        reg.loc[i,"fit"] = np.polyfit(x, y, deg=1)[0]
        # calculate average distance
        yfit = reg.loc[i, "fit"]*np.arange(reg.loc[i,"length"]+1) + reg.loc[i,"val1"] # values of y = ax + b
        yorig = data.loc[reg.loc[i,"p1"]:reg.loc[i,"p2"], "Close"]
        reg.loc[i, "std"] = np.sqrt(np.sum((yfit-yorig)**2/reg.loc[i, "length"])) # np.mean(np.abs((yfit-yorig)))
        if reg.loc[i, "uptrend"] == True:
            reg.loc[i, "risk_%"] = ((data.loc[reg.loc[i,"p1"]:reg.loc[i,"p2"], "Low"].min()/data.loc[reg.loc[i,"p1"], "Close"])-1)*100
        else:
            reg.loc[i, "risk_%"] = ((data.loc[reg.loc[i,"p1"]:reg.loc[i,"p2"], "High"].max()/data.loc[reg.loc[i,"p1"], "Close"])-1)*100
    
    return reg