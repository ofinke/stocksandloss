# this is a group of functions for market status notebook to save space

from scraper import stock_daily
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import indicators as ind
import pandas as pd
import numpy as np
import datetime as dt
import ast
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


# print sector results (image)
def sectors():
    # define figure
    fig = plt.figure(figsize=(16,12))
    gs = gridspec.GridSpec(ncols=3,nrows=6, hspace=0.075, width_ratios=[1.2,1.2,1])
    # sectors and column names for performance
    indices = ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU", "FFTY"]
    performance = ["YTD", "MTD", "Day"]
    df = pd.DataFrame(index=indices, columns=performance)
    names = ["Communication Services", "Consumer Discretionary", "Consumer Staples", "Energy", "Financial", "Health", "Industrial", "Materials", "Real Estate", "Technology ", "Utilities", "IBDs top 50"]
    axpos = [[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [0,1], [1,1], [2,1], [3,1], [4,1], [5,1]]
    for i, val in enumerate(indices):
        sector = stock_daily(val, save=False)
        # calculating performance
        df.loc[val, "Day"] = np.round((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[len(sector.data)-2, "Close"]-1)*100,2)
        ytd =  np.where(sector.data["Date"].to_numpy() >= np.datetime64(dt.datetime(dt.datetime.today().year,1,1)))[0][0]
        df.loc[val,"YTD"] = np.round(((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[ytd, "Close"])-1)*100,2)
        df.loc[val,"MTD"] = np.round(((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[len(sector.data)-21, "Close"])-1)*100,2)
        
        sma = ind.sma(sector.data, 100)["SMA"]
        # plots
        ax = fig.add_subplot(gs[axpos[i][0], axpos[i][1]])
        lab = "Change: " + str(df.loc[val, "Day"]) + "%"
        if sector.data.iloc[-1,4] < sector.data.iloc[-2,4]:
            ax.plot(sector.data.index, sector.data["Close"], color="r", label=lab)
            ax.fill_between(sector.data.index, sector.data["Close"], color="r", alpha=0.5)
        else:
            ax.plot(sector.data.index, sector.data["Close"], color="g", label=lab)
            ax.fill_between(sector.data.index, sector.data["Close"], color="g", alpha=0.5)
        ax.plot(sma, color="k", alpha=0.5)
        ax.set_xlim([150, sector.data.shape[0]])
        ax.set_ylim([np.min(sector.data["Low"][150:])*0.9, np.max(sector.data["High"][150:])*1.05])
        ax.set_ylabel(indices[i], weight="bold")
        ax.legend(loc=3)
        ax.text(0.04, 0.92, names[i], ha="left", va="top", transform=ax.transAxes, weight="bold")
        if i == 5 or i == 11:
            tick = np.linspace(150, sector.data.shape[0]-1, 6, dtype=int)
            ax.set_xticks(tick)
            ax.set_xticklabels(sector.data.loc[tick,"Date"].dt.strftime("%d/%m"))
        else:
            ax.set_xticks([])
            ax.set_xticklabels([])
    
    # barcharts
    df = df.iloc[::-1] # reversing dataframe so its plotted better
    ngs = gs[:,2].subgridspec(2,1, hspace=0.15)# subgridspec
    # month
    bch1 = fig.add_subplot(ngs[0,0])
    col = np.array(["g"]*len(df))
    col[np.where(df["MTD"]<0)[0]] = "r"
    bch1.barh(df.index, df["MTD"], color=col, alpha=0.5, edgecolor=col)
    bch1.set_title("Last 20 Trading days", weight="bold", fontsize="medium")
    bch1.grid(axis="x", linestyle="--")

    bch2 = fig.add_subplot(ngs[1,0]) 
    col = np.array(["g"]*len(df))
    col[np.where(df["YTD"]<0)[0]] = "r"
    bch2.barh(df.index, df["YTD"], color=col, alpha=0.5, edgecolor=col)
    bch2.set_title("Last year", weight="bold", fontsize="medium")
    bch2.set_xlabel("Change [%]")
    bch2.grid(axis="x", linestyle="--")

    
    plt.show()

# print industries results (table)
class industries():
    # constructor = scrapes the table
    def __init__(self, sf=True, rank=True):
        # scrap new data
        self.scrap()
        # save if desired
        if sf:
            self.save()
        if rank:
            # load previous day
            self.load()
            # add rank column to the 
            self.addrank()
        return
        
    def scrap(self):
        url = "https://finviz.com/groups.ashx?g=industry&v=140&o=-perf4w"
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        
        # reading the table into the pandas dataframe, step by step
        # find the full table
        htmltable = soup.find_all("table", {"class": "table-light"})[0]
        # width="100%", cellspacing="1", cellpadding="2", border="0", bgcolor="#d3d3d3"
        rows = htmltable.find_all("tr") # Don't know why, but the first row has ~1800 lines and also holds rest of the table, I'll just extract the column names
        table_width = len(rows[1].find_all("td"))

        # extract column names
        cols = [None] * table_width
        cols_row = rows[0].find_all("td")
        for k in range(table_width):
            cols[k] = cols_row[k].text
        del cols_row
        # create empty DataFrame
        newdata = pd.DataFrame(index=np.arange(len(rows)-1), columns=cols)
        # fill the frame with data
        # start with rows
        for i in newdata.index+1: # index manipulated so I skip the column row
            scrapedrow = rows[i].find_all("td") 
            # go through rows
            for j, val in enumerate(cols):
                newdata.loc[i-1, val] = scrapedrow[j].string
        # manipulate the DataFrame (delete shit and set correct datatypes)
        newdata = newdata.drop(columns=["No."])
        perccols = ['Perf Week', 'Perf Month', 'Perf Quart', 'Perf Half', 'Perf Year', 'Perf YTD', 'Change']
        for i, val in enumerate(perccols):
            newdata[val] = newdata[val].map(lambda x: x.rstrip("%")).astype("float")
        # safe into the object
        self.table = newdata
        return
    
    def addrank(self):
        # I have to use names to find out the rank differences
        old = self.table_old.reset_index().set_index("Name")
        new = self.table.reset_index().set_index("Name")
        pos = old.reindex(new.index.values)["index"].values
        self.table["Position"] = np.round((pos - new["index"].values),0)
        return

    def prettify(self, table):
        # formats
        def style_negative(v, props=''):
            return np.where(v <= 0, props, None)
        def style_positive(v, props=''):
            return np.where(v > 0, props, None)
        table = table.drop(columns=["Recom", "Avg Volume", "Volume", "Perf Quart", "Perf YTD"])
        table["Position"] = table["Position"].astype("int32")
        numcols = ["Perf Week", "Perf Month", "Perf Half", "Perf Year", "Change"]
        # linkable rowname?
        return table.style.format("{:.2f}", subset=numcols).apply(style_negative, props='color:red;', subset=numcols)\
            .apply(style_positive, props='color:green;', subset=numcols)\
            .set_table_attributes("style='display:inline'")\
            .set_properties(subset=["Name"], **{'width': '300px'})\
            .hide_index()

    def save(self):
        date = ind.shifttolastmarketday(dt.date.today())
        with pd.ExcelWriter("Data/industry_"+str(date.strftime("%Y"))+".xlsx", mode="a") as writer:
            self.table.to_excel(writer, sheet_name=date.strftime("%Y-%m-%d"))
        return

    def load(self):
        # loads sheet names from the excel file and opens correct date
        lastday = ind.shifttolastmarketday(dt.date.today())
        file = pd.ExcelFile("Data/industry_"+str(dt.date.today().strftime("%Y"))+".xlsx")
        # check to load correct sheet (because it depends if I saved the data or not)
        # this won't work when transitioning years, but who gives a fuck
        if file.sheet_names[-1] == lastday.strftime("%Y-%m-%d"):
            sht = file.sheet_names[-2]
        else:
            sht = file.sheet_names[-1]
        # read the table
        self.table_old = pd.read_excel(file, sht, index_col=0)
        return

# print world market results (image)
def worldmarkets():
    fig = plt.figure(figsize=(16,6.5))
    gs = gridspec.GridSpec(ncols=3,nrows=3, hspace=0.075, width_ratios=[1.2,1.2,1])
    indices = ["^HSI", "^N225", "STW.AX", "^FTMC", "^GDAXI"]
    performance = ["YTD", "MTD", "Day"]
    # dataframe for performance
    df = pd.DataFrame(index=indices, columns=performance)
    names = ["Hong Kong: Hang Seng", "Japan: Nikkei 225", "Australia: ASX 200", "United Kingdom: FTSE250", "Germany: DAX"]
    axpos = [[0,0], [1,0], [2,0], [0,1], [1,1]]

    for i, val in enumerate(indices):
        sector = stock_daily(val, save=False)
        # calculating performance
        df.loc[val, "Day"] = np.round((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[len(sector.data)-2, "Close"]-1)*100,2)
        ytd =  np.where(sector.data["Date"].to_numpy() >= np.datetime64(dt.datetime(dt.datetime.today().year,1,1)))[0][0]
        df.loc[val,"YTD"] = np.round(((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[ytd, "Close"])-1)*100,2)
        df.loc[val,"MTD"] = np.round(((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[len(sector.data)-21, "Close"])-1)*100,2)
        
        sma = ind.sma(sector.data, 100)["SMA"]
        # plots
        ax = fig.add_subplot(gs[axpos[i][0], axpos[i][1]])
        lab = "Change: " + str(df.loc[val, "Day"]) + "%"
        if sector.data.iloc[-1,4] < sector.data.iloc[-2,4]:
            ax.plot(sector.data.index, sector.data["Close"], color="r", label=lab)
            ax.fill_between(sector.data.index, sector.data["Close"], color="r", alpha=0.5)
        else:
            ax.plot(sector.data.index, sector.data["Close"], color="g", label=lab)
            ax.fill_between(sector.data.index, sector.data["Close"], color="g", alpha=0.5)
        ax.plot(sma, color="k", alpha=0.5)
        ax.set_xlim([150, sector.data.shape[0]])
        ax.set_ylim([np.min(sector.data["Low"][150:])*0.9, np.max(sector.data["High"][150:])*1.05])
        ax.legend(loc=3)
        ax.text(0.04, 0.92, names[i], ha="left", va="top", transform=ax.transAxes, weight="bold")
        if i == 5 or i == 10:
            tick = np.linspace(150, sector.data.shape[0]-1, 6, dtype=int)
            ax.set_xticks(tick)
            ax.set_xticklabels(sector.data.loc[tick,"Date"].dt.strftime("%d/%m"))
        else:
            ax.set_xticks([])
            ax.set_xticklabels([])

    # barcharts
    df = df.iloc[::-1] # reversing dataframe so its plotted better
    ngs = gs[:,2].subgridspec(2,1, hspace=0.2)# subgridspec
    # month
    bch1 = fig.add_subplot(ngs[0,0])
    col = np.array(["g"]*len(df))
    col[np.where(df["MTD"]<0)[0]] = "r"
    bch1.barh(df.index, df["MTD"], color=col, alpha=0.5, edgecolor=col)
    bch1.set_title("Last 20 Trading days", weight="bold", fontsize="medium")
    bch1.grid(axis="x", linestyle="--")

    bch2 = fig.add_subplot(ngs[1,0]) 
    col = np.array(["g"]*len(df))
    col[np.where(df["YTD"]<0)[0]] = "r"
    bch2.barh(df.index, df["YTD"], color=col, alpha=0.5, edgecolor=col)
    bch2.set_title("Last year", weight="bold", fontsize="medium")
    bch2.set_xlabel("Change [%]")
    bch2.grid(axis="x", linestyle="--")
    plt.show()

# print us market results (image)
def usmarkets():
    # plan, gridspec 4 rows, 3 columns
    # 1 row: SPY, NASDAQ, IWM last year (without volume, line plot)
    # 2 row: SPY, NASDAQ, IWM last 6 months (volume, candlesticks, SMAs and others)
    # 3 row: VFI
    # 4 row: subgridspec containing barcharts with new high low, advancing, declining and others
    # INDICES PLOT
    fig = plt.figure(figsize=(16,14))
    gs = gridspec.GridSpec(nrows=4,ncols=3, height_ratios=[0.5,1,0.4,1])

    indices = ["SPY", "^IXIC", "IWM"]
    names = ["SPY [S&P500]", "Nasdaq Composite", "IWM [Russell 2000]"]
    ly = ["SPY Last Year", "Nasdaq Last Year", "IWM Last Year"]
    strat = np.zeros((2, len(indices)))

    for i, val in enumerate(indices):
        stock = stock_daily(val, save=False)
        # calculate change
        change = np.round((stock.data.loc[len(stock.data)-1, "Close"]/stock.data.loc[len(stock.data)-2, "Close"]-1)*100,2)
        lab = "Change: " + str(change) + "%"
        year_change = np.round(((stock.data.loc[len(stock.data)-1, "Close"]/stock.data.loc[0, "Close"])-1)*100,2)
        # 1 year plot
        ax1 = fig.add_subplot(gs[0,i])
        ax1.plot(stock.data["Close"], color="tab:blue", linewidth=2)
        ax1.fill_between(stock.data.index, stock.data["Close"], color="tab:blue", alpha=0.5)
        tick = np.linspace(stock.data.index[0], stock.data.index[-1]-1, 4, dtype=int)
        ax1.set_xticks(tick)
        ax1.set_xticklabels(stock.data.loc[tick,"Date"].dt.strftime("%d/%m"))
        ax1.set_xlim([stock.data.index[0], stock.data.index[-1]])
        ax1.set_ylim([np.min(stock.data["Low"])*0.9, np.max(stock.data["High"])*1.05])
        ax1.text(0.03, 0.92, ly[i] + ": (" + str(year_change) + "%)", ha="left", va="top", transform=ax1.transAxes)

        # 6 months candlesticks
        green = stock.data.index.where(stock.data["Close"] >= stock.data["Open"])
        red = stock.data.index.where(stock.data["Close"] < stock.data["Open"])
        rang = [150, stock.data.shape[0]]
        sma10 = ind.sma(stock.data,10)["SMA"]
        sma50 = ind.sma(stock.data,50)["SMA"]
        sma100 = ind.sma(stock.data,100)["SMA"]
        emacl1s = ind.ema(stock.data, 5)["EMA"] # ema cloud 1 short
        emacl1l = ind.ema(stock.data, 13)["EMA"] # ema cloud 1 long
        emacl2s = ind.ema(stock.data, 34)["EMA"] # ema cloud 1 short
        emacl2l = ind.ema(stock.data, 50)["EMA"] # ema cloud 1 long
        # plot
        ax2 = fig.add_subplot(gs[1,i])
        ax2.vlines(green, stock.data["Low"], stock.data["High"], color="g", alpha=0.7)
        ax2.scatter(green, stock.data["Open"], marker="_", color="g", s=10, alpha=0.7)
        ax2.scatter(green, stock.data["Close"], marker="_", color="g", s=10, alpha=0.7)
        ax2.vlines(red, stock.data["Low"], stock.data["High"], color="r", alpha=0.7)
        ax2.scatter(red, stock.data["Open"], marker="_", color="r", s=10, alpha=0.7)
        ax2.scatter(red, stock.data["Close"], marker="_", color="r", s=10, alpha=0.7)
        ax2.plot(sma100, color="darkgreen", alpha=0.8)
        ax2.plot(sma50, color="mediumpurple", alpha=0.8)
        ax2.fill_between(stock.data.index, emacl1l, emacl1s, where=(emacl1s>=emacl1l), color="g", alpha=0.3, interpolate=True)
        ax2.fill_between(stock.data.index, emacl1l, emacl1s, where=(emacl1s<emacl1l), color="r", alpha=0.3, interpolate=True)
        ax2.fill_between(stock.data.index, emacl2l, emacl2s, where=(emacl2s>=emacl2l), color="b", alpha=0.15, interpolate=True)
        ax2.fill_between(stock.data.index, emacl2l, emacl2s, where=(emacl2s<emacl2l), color="darkorange", alpha=0.3, interpolate=True)
        axy = ax2.twinx()
        axy.vlines(red, 0, stock.data["Volume"], color="r", alpha=0.7)
        axy.vlines(green, 0, stock.data["Volume"], color="g", alpha=0.7)
        axy.set_ylim([0, np.max(stock.data["Volume"][150:])*3.5])
        axy.set_yticklabels([])
        axy.set_yticks([])
        ax2.set_xlim(rang)
        tick = np.linspace(rang[0], rang[1]-1, 6, dtype=int)
        ax2.text(0.03, 0.96, names[i], ha="left", va="top", transform=ax2.transAxes, weight="bold")
        ax2.text(0.03, 0.88, lab, ha="left", va="top", transform=ax2.transAxes)
        ax2.set_xticks(tick)
        ax2.set_xticklabels(stock.data.loc[tick,"Date"].dt.strftime("%d/%m"))
        ax2.set_ylim([np.min(stock.data["Low"][150:])*0.9, np.max(stock.data["High"][150:])*1.05])
        # strategy status
        strat[0, i] = stock.data.iloc[-1]["Close"] > sma10.iloc[-1]
        strat[1, i] = stock.data.iloc[-1]["Close"] > sma50.iloc[-1]

    # VIX
    ngss = gs[2,:].subgridspec(1,2, wspace=0.13, width_ratios=[0.91,2]) # subgridspec
    stock = stock_daily("^VIX", save=False)
    axv = fig.add_subplot(ngss[0,1])
    green = stock.data.index.where(stock.data["Close"] >= stock.data["Open"])
    red = stock.data.index.where(stock.data["Close"] < stock.data["Open"])
    rang = [150, stock.data.shape[0]]
    axv.vlines(green, stock.data["Low"], stock.data["High"], color="g", alpha=0.7)
    axv.scatter(green, stock.data["Open"], marker="_", color="g", s=10, alpha=0.7)
    axv.scatter(green, stock.data["Close"], marker="_", color="g", s=10, alpha=0.7)
    axv.vlines(red, stock.data["Low"], stock.data["High"], color="r", alpha=0.7)
    axv.scatter(red, stock.data["Open"], marker="_", color="r", s=10, alpha=0.7)
    axv.scatter(red, stock.data["Close"], marker="_", color="r", s=10, alpha=0.7)
    axv.set_xlim(rang)
    tick = np.linspace(rang[0], rang[1]-1, 6, dtype=int)
    axv.set_xticks(tick)
    axv.set_xticklabels(stock.data.loc[tick,"Date"].dt.strftime("%d/%m"))
    axv.set_ylim([np.min(stock.data["Low"][150:])*0.9, np.max(stock.data["High"][150:])*1.05])
    change = np.round((stock.data.loc[len(stock.data)-1, "Close"]/stock.data.loc[len(stock.data)-2, "Close"]-1)*100,2)
    lab = "Change: " + str(change) + "%"
    axv.text(0.015, 0.94, "VIX volatility index", ha="left", va="top", transform=axv.transAxes, weight="bold")
    axv.text(0.015, 0.76, lab, ha="left", va="top", transform=axv.transAxes)
    vstrat = stock.data.iloc[-1]["Close"] > 22
    # MOMENTUM PLOT
    # scrap momentum data
    # load the dataframe and compare the dates
    df = pd.read_excel("Data/marketmomentum.xlsx", index_col=0)
    if df.loc[df.index[-1], "date"] != ind.shifttolastmarketday(dt.date.today()):
        # scrape the data
        url = "https://finviz.com/"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        ups = soup.findAll("div", {"class": "market-stats_labels_left"})
        downs = soup.findAll("div", {"class": "market-stats_labels_right"})

        # create dataframe with new data
        cols =["date", "advancing", "declining", "addiff", "highs", "lows", "hldiff", "above50", "below50", "abdiff"]
        ndf = pd.DataFrame([], columns=cols)
        # fill it with data
        ndf.loc[0, "date"] = ind.shifttolastmarketday(dt.datetime.today())
        ndf.loc[0, "advancing"] = int(ups[0].span.text)
        ndf.loc[0, "declining"] = int(downs[0].span.text)
        ndf.loc[0, "addiff"] = ndf.loc[0, "advancing"] - ndf.loc[0, "declining"]
        ndf.loc[0, "highs"] = int(ups[1].span.text)
        ndf.loc[0, "lows"] = int(downs[1].span.text)
        ndf.loc[0, "hldiff"] = ndf.loc[0, "highs"] - ndf.loc[0, "lows"]
        ndf.loc[0, "above50"] = int(ups[2].span.text)
        ndf.loc[0, "below50"] = int(downs[2].span.text)
        ndf.loc[0, "abdiff"] = ndf.loc[0, "above50"] - ndf.loc[0, "below50"]

        df = pd.concat([df, ndf], ignore_index=True)
        df.to_excel("Data/marketmomentum.xlsx")
        # there is bug with the dates, its unable to set the xtickslabels properly when new row is added

    print("Last update done: " + dt.datetime.today().strftime("%d-%m-%Y at %H:%M:%S"))
    df["date"] = pd.to_datetime(df["date"])
    # plot momentum results
    ngs = gs[3,:].subgridspec(2,1, hspace=0) # subgridspec
    axmom1 = fig.add_subplot(ngs[0,0])
    axmom1.bar(df.index, df["advancing"], color="g", alpha=0.5, edgecolor="g")
    axmom1.bar(df.index, -df["declining"], color="r", alpha=0.5, edgecolor="r")
    axmom1.grid(axis="y", linestyle="--")
    axmom1.set_xlim([-0.5, df.index[-1]+0.5])
    axmom1.text(0.01, 0.9, "Advancing & Declining", ha="left", va="top", transform=axmom1.transAxes, weight="bold",
        bbox=dict(facecolor="w", edgecolor="lightgray", pad=5))

    axmom2 = fig.add_subplot(ngs[1,0])
    col = np.array(["g"]*len(df["hldiff"]))
    col[np.where(df["hldiff"]<0)[0]] = "r"
    axmom2.bar(df.index, df["hldiff"], color=col, alpha=0.5, edgecolor=col)
    axmom2.grid(axis="y", linestyle="--")
    axmom2.set_xlim([-0.5, df.index[-1]+0.5])
    tick = np.linspace(df.index[0], df.index[-1], 15, dtype=int)
    axmom2.set_xticks(tick)
    axmom2.xaxis.set_tick_params(rotation=45)
    axmom2.set_xticklabels(df.loc[tick,"date"].dt.strftime("%d/%m"))
    axmom2.text(0.01, 0.9, "New Highs - New Lows", ha="left", va="top", transform=axmom2.transAxes, weight="bold", 
        bbox=dict(facecolor="w", edgecolor="lightgray", pad=5))
    
    # market status
    # this is positioned to the left of VIX, but code is here because I use data from the marketmomentum.xlsx
    axs = fig.add_subplot(ngss[0,0])
    # hide everything
    axs.axis("off")
    # texts
    axs.text(0.01, 0.98, "Market Snapshot", ha="left", va="top", transform=axs.transAxes, weight="bold")
    # vix status
    axs.text(0.01, 0.80, "VIX:", ha="left", va="top", transform=axs.transAxes)
    if vstrat == 1:
        axs.text(0.21, 0.80, "Elevated (>22)", ha="left", va="top", transform=axs.transAxes, color="r")
    else:
        axs.text(0.21, 0.80, "Safe (<22)", ha="left", va="top", transform=axs.transAxes, color="g")
    # SPY
    axs.text(0.01, 0.62, "SPY:", ha="left", va="top", transform=axs.transAxes)
    if strat[:,0].sum() == 0:
        axs.text(0.21, 0.62, "Protective (<SMA10, <SMA50)", ha="left", va="top", transform=axs.transAxes, color="r")
    elif strat[:,0].sum() == 1:
        axs.text(0.21, 0.62, "Defensive (>SMA10, <SMA50)", ha="left", va="top", transform=axs.transAxes, color="darkorange")
    else:
        axs.text(0.21, 0.62, "Aggresive (>SMA10, >SMA50)", ha="left", va="top", transform=axs.transAxes, color="g")
    #NASDAQ
    axs.text(0.01, 0.44, "NASDAQ:", ha="left", va="top", transform=axs.transAxes)
    if strat[:,1].sum() == 0:
        axs.text(0.21, 0.44, "Protective (<SMA10, <SMA50)", ha="left", va="top", transform=axs.transAxes, color="r")
    elif strat[:,1].sum() == 1:
        axs.text(0.21, 0.44, "Defensive (>SMA10, <SMA50)", ha="left", va="top", transform=axs.transAxes, color="darkorange")
    else:
        axs.text(0.21, 0.44, "Aggresive (>SMA10, >SMA50)", ha="left", va="top", transform=axs.transAxes, color="g")
    # IWM
    axs.text(0.01, 0.26, "IWM:", ha="left", va="top", transform=axs.transAxes)
    if strat[:,2].sum() == 0:
        axs.text(0.21, 0.26, "Protective (<SMA10, <SMA50)", ha="left", va="top", transform=axs.transAxes, color="r")
    elif strat[:,2].sum() == 1:
        axs.text(0.21, 0.26, "Defensive (>SMA10, <SMA50)", ha="left", va="top", transform=axs.transAxes, color="darkorange")
    else:
        axs.text(0.21, 0.26, "Aggresive (>SMA10, >SMA50)", ha="left", va="top", transform=axs.transAxes, color="g")

    plt.show()

# scrap and print results from finviz screeners (tables)
class screeners():
    def newhighs(self):
        # url for the specific screener
        time.sleep(2)
        url = "https://finviz.com/screener.ashx?v=411&s=ta_newhigh&f=ind_stocksonly,sh_avgvol_o100,sh_float_o2,sh_relvol_o1&o=-relativevolume"
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        # create dataframe with the ticker names

        tickers = soup.find_all("span", onclick=lambda onclick: onclick and onclick.startswith("window.location='quote.ashx?t"))
        text = [val.text for i, val in enumerate(tickers)]
        return pd.DataFrame(data={"Tickers": (val.text for i, val in enumerate(tickers))})

    def fiftyday(self):
        # url for the specific screener
        time.sleep(2)
        url = "https://finviz.com/screener.ashx?v=411&f=fa_debteq_u1,fa_epsyoy_pos,fa_epsyoy1_pos,fa_sales5years_o5,fa_salesqoq_pos,ind_stocksonly,sh_avgvol_o100,sh_float_o2,sh_relvol_o1,ta_highlow50d_nh&ft=2&o=-relativevolume"
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        # create dataframe with the ticker names

        tickers = soup.find_all("span", onclick=lambda onclick: onclick and onclick.startswith("window.location='quote.ashx?t"))
        return pd.DataFrame(data={"Tickers": (val.text for i, val in enumerate(tickers))})

    def potentialreversal(self):
        # url for the specific screener
        time.sleep(2)
        url = "https://finviz.com/screener.ashx?v=411&f=ind_stocksonly,sh_avgvol_o400,ta_pattern_channelup,ta_perf_1wdown&ft=3&o=perf1w"
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        # create dataframe with the ticker names

        tickers = soup.find_all("span", onclick=lambda onclick: onclick and onclick.startswith("window.location='quote.ashx?t"))
        return pd.DataFrame(data={"Tickers": (val.text for i, val in enumerate(tickers))})

    def smabounces(self):
        # url for the specific screener
        time.sleep(2)
        url = "https://finviz.com/screener.ashx?v=411&f=ind_stocksonly,sh_avgvol_o400,sh_curvol_o2000,sh_relvol_o1,ta_sma20_pa,ta_sma50_pb&o=-perf1w"
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        # create dataframe with the ticker names

        tickers = soup.find_all("span", onclick=lambda onclick: onclick and onclick.startswith("window.location='quote.ashx?t"))
        return pd.DataFrame(data={"Tickers": (val.text for i, val in enumerate(tickers))})

    def prettify(self, df, ncols=15):
        # nested function fot clickable links to results
        def make_clickable(val):
            # target _blank to open new window
            return '<a target="_blank" href="https://finviz.com/quote.ashx?t={}" style="text-decoration: none">{}</a>'.format(val, val)
        
        data = df["Tickers"].map(lambda x: x.lstrip("\xa0").rstrip("\xa0")).values

        if (data.shape[0] % ncols) > 0:
            em = np.zeros(ncols-(df.shape[0] % ncols)).astype(str)
            em[:] = " "
            arr = np.concatenate((data, em), axis=None)
        else:
            arr = data
        return pd.DataFrame(arr.reshape(-1, ncols)).style.format(make_clickable).hide_index()

    def newipos(self):
        # url for the specific screener
        url = "https://finviz.com/screener.ashx?v=151&f=ipodate_prevweek&o=ipodate"
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        # create dataframe with the ticker names
        return soup

# scrap and print commodity futures (table)
class futures():
    # to be implemented
    def save(self):
        return
    def load(self):
        return
    # scrap futures from finviz (relative, day, week, month, quarter, year)
    def scrapfutures(self, column, row):
        # scraps relative performance and returns all rows
        url = "https://finviz.com/futures_performance.ashx?v="+column
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        # EXTRACTING THE RESULTS
        # find corresponding script, values are hold in a messy string
        # possible future problem: index of correct javascript tag is hardcoded as 14, should think of something more future proof
        # this works for getting the data (27/11/2021)
        stringmess = soup.find_all("script", type="text/javascript")[14].string  # this string holds the results + some trash around it
        stringmess = stringmess.split("[")[1].split("]")[0] # extract the dictionary definition
        scrapedvals = pd.DataFrame(data=ast.literal_eval(stringmess)) # convert mess to dataframe
        scrapedvals = scrapedvals[scrapedvals["label"].isin(row)].reset_index(drop=True) #drop values Im not interested in
        scrapedvals = scrapedvals.set_index(scrapedvals["label"].values).reindex(row) # redefine index and sort it so it corresponds to how variable "row" is sorted
        return scrapedvals["perf"]

    def returnfutures(self):
        # define dataframe
        # problem, currently cannot scrap year as the ast.literal_eval() function get stuck on ethanol which returns null for some reason
        col = ["Day [%]", "Week [%]", "Month [%]", "Quarter [%]"] 
        finvizcolumn = ["11", "12", "13", "14"] # number is last part of finviz url for scraping, corresponds to columns in col
        row = ["Natural Gas", "Crude Oil WTI", "Crude Oil Brent", "Ethanol", "Palladium", "Copper", "Platinum", "Silver", "Gold", "Lumber", "Cotton", "Cocoa", "Sugar", "Coffee",
                "Rough Rice", "Wheat", "Corn", "Oats", "Live Cattle", "USD", "EUR", "5 Year Note", "10 Year Note", "30 Year Bond"]
        zer = np.zeros((len(row), len(col)))
        futu = pd.DataFrame(data=zer, index=row, columns=col)

        # run scraping for the columns
        for i, val in enumerate(col):
            futu[val] = self.scrapfutures(column=finvizcolumn[i], row=row)
            time.sleep(2)
        return futu

    def prettify(self, table):
        # formats
        def make_bold(val):
                # target _blank to open new window
                return "<b>{}</b>".format(val)
        def style_negative(v, props=''):
            return props if v <= 0 else None
        def style_positive(v, props=''):
            return props if v > 0 else None
        # assign color to value
        # add % (convert to string)
        # linkable rowname?
        return table.style.format("{:.2f}").applymap(style_negative, props='color:red;').applymap(style_positive, props='color:green;').set_table_attributes("style='display:inline'")

# ------------------------- testing / editing of functions and classes

def main():
    usmarkets()
    return

if __name__ == '__main__':
    main()


