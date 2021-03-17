# ANALYZER
# group of functions to analyze stock data gathered from scraper.py

# IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# import plotly.graph_objects as go
# there is a scraper.py import in testing runtime (it's not required anywhere else)!

# PLOT
def stock_plot(d, i):
    # d = pandas dataframe, i = stock information
    # FIGURE DEFINITION
    fig, ax = plt.subplots(figsize=(21,8))
    fig.suptitle("Last 3 weeks of " + i["longName"])
    # PLOTS
    # basic open, close etc.
    ax.plot(d["Open"], color="cornflowerblue")
    ax.plot(d["Close"], color="cornflowerblue")
    ax.plot(d["High"], color="silver")
    ax.plot(d["Low"], color="silver")
    # moving averages
    if "MA5" in d.columns:
        ax.plot(d["MA5"], label="MA5", color="b")
    if "MA25" in d.columns:
        ax.plot(d["MA50"], label="MA25", color="orange")
    if "MA50" in d.columns:
        ax.plot(d["MA50"], label="MA50", color="orange")
    if "MA100" in d.columns:
        ax.plot(d["MA100"], label="MA100", color="darkviolet")
    if "MA200" in d.columns:
        ax.plot(d["MA200"], label="MA200", color="red")
    # death / golden crosses 
    if "gcross" in d.columns:
        ax.vlines(d.reset_index()["index"][d["gcross"] == 1], min(d["Close"]), max(d["Close"]), label="Golden cross", color="yellow")
    if "dcross" in d.columns:
        ax.vlines(d.reset_index()["index"][d["dcross"] == 1], min(d["Close"]), max(d["Close"]), label="Death cross", color="k")
    # set axis and other plot settings
    ax.set(xlabel="Date [integer]", ylabel="Price [USD]")
    ax.legend()
    # show result plot
    plt.show()
    return

# MOVING AVERAGE
def mov_average(x, w):
    # plot supports 5,, 25, 50, 100, 200
    res = np.convolve(x["Close"], np.ones(w), 'valid') / w
    ma = np.empty(len(x["Close"])-len(res))
    ma[:] = np.NaN
    x["MA"+str(w)] = np.insert(res, 0, ma, axis=0)
    return x

# CROSSES
# golden cross - lowMA crosses highMA, death cross - opposite
def find_crosses(x, col1=None, col2=None):
    # INPUTS
    # x = stock.data dataframe
    # col1 = name of first column
    # col2 = name of second column
    try:
        int(col1[2:])
        int(col2[2:])
    except ValueError:
        print("col1 and col2 need to specify moving averages (MA100 etc.)")

    # calculate sign change
    dif = x[col1]-x[col2] # substract
    res = ((np.diff(np.sign(dif)) != 0)*1).astype("float64") # find sign change (nans change to 1!)
    # insert back NaNs
    an = np.count_nonzero(np.isnan(x[col1]))
    bn = np.count_nonzero(np.isnan(x[col2]))
    if an > bn:
        res[0:an] = np.NaN
    else:
        res[0:bn] = np.NaN
    
    # determine which cross is the first one
    res = np.append(res,[0]) # append 0 to the end for same vector length
    gcross = np.zeros(len(res))
    dcross = np.zeros(len(res))
    # find which cross is first
    for i, val in enumerate(res):
        if val == 1:
            if int(col1[2:]) < int(col2[2:]):
                nextDeath = True # first cross is death cross
                break
            else:
                nextDeath = False # first cross is golden cross
                break
    # delete 
    # nextDeath oscillates which cross shoudl follow
    for i, val in enumerate(res):
        if val == 1:
            if nextDeath is True:
                dcross[i] = 1
                nextDeath = False
            else:
                gcross[i] = 1
                nextDeath = True
    
    # save results into x
    x["gcross"] = gcross
    x["dcross"] = dcross
    return x

# TESTING RUNTIME
def main():
    # import only for this function
    import scraper as sc
    stock = sc.scrap(stockHandle="TSLA")

    # basic_plot(stock.data, stock.info)
    stock.data = mov_average(stock.data, 5)
    stock.data = mov_average(stock.data, 50)
    stock.data = mov_average(stock.data, 100)
    # analyzed_plot(stock.data, stock.info)
    stock.data = find_crosses(stock.data, col1="MA50", col2="MA100")
    stock_plot(stock.data, stock.info)

    return

if __name__ == "__main__":
    main()