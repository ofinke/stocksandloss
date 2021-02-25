# ANALYZER
# group of functions to analyze stock data gathered from scraper.py

# IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.graph_objects as go
# there is a scraper.py import in testing runtime (it's not required anywhere else)!

def extract_unique(arr):
    unique = []
    for x in arr:
        if x not in unique:
            unique.append(x)
    unique = np.array(unique, dtype=int)
    return unique


def days_plot(data, info):

    # extract unique days 
    days = extract_unique(data["Datetime"].array.day)
    days = np.append(days,np.NaN)
    indexTime = []
    k = 0
    for i, val in enumerate(data["Datetime"]):
        if val.day == days[k]:
            indexTime.append(i)
            k = k + 1
    indexTime.append(data.index[-1])

    # create figure
    fig, ax = plt.subplots(figsize=(15,8))

    ax.plot(data.index, data["Low"])
    ax.plot(data.index, data["High"])
    ax.vlines(indexTime,min(data["Low"])-0.05*max(data["High"]),max(data["High"])+0.05*max(data["High"]), colors="k", alpha=0.3, linestyles="dashed")
    # xticks
    ax.set_xticks(indexTime)
    ax.set_xticklabels(data["Datetime"][indexTime].dt.strftime(date_format="%d/%m %H:%M"), rotation="vertical")

    plt.show()

def year_plot(data, info):
    
    # extract beginning of months
    months = extract_unique(data["Date"].array.month)
    months = np.append(months,[months[0], np.NaN])
    indexTime = []
    k = 0
    for i, val in enumerate(data["Date"]):
        if val.month == months[k]:
            indexTime.append(i)
            k = k + 1
    indexTime.append(data.index[-1])

    # create figure
    fig, ax = plt.subplots(figsize=(15,8))

    ax.plot(data.index, data["Low"])
    ax.plot(data.index, data["High"])
    ax.vlines(indexTime,min(data["Low"])-0.05*max(data["High"]),max(data["High"])+0.05*max(data["High"]), colors="k", alpha=0.3, linestyles="dashed")
    # xticks
    ax.set_xticks(indexTime)
    ax.set_xticklabels(data["Date"][indexTime].dt.strftime(date_format="%d/%m"),rotation="vertical")


    plt.show()

    return

def candlestick(df):
    
    fig = go.Figure(data=[go.Candlestick(x=df['Datetime'].dt.strftime("%m/%d %H:%M"),
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

    fig.show()
    return
# TESTING RUNTIME
def main():
    # import only for this function
    import scraper as sc
    stock = sc.scrap(stockHandle="TSLA", ndays=7)

    # days_plot(stock.datadays, stock.info)
    # year_plot(stock.datayear, stock.info)
    candlestick(stock.datadays)

    return

if __name__ == "__main__":
    main()