# this is a group of functions for market status notebook to save space

from scraper import stock_daily
import matplotlib.pyplot as plt
import indicators as ind
import pandas as pd
import numpy as np
import datetime as dt
import ast
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


class sectors():
    def show(self):
        # define figure
        fig, ax = plt.subplots(ncols=3, nrows=4, figsize=(20,16))

        indices = ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"]
        performance = ["YTD", "MTD", "Day"]
        # dataframe for performance
        df = pd.DataFrame(index=indices, columns=performance)
        names = ["XLC = Communication Services", "XLY = Consumer Discretionary", "XLP = Consumer Staples", "XLE = Energy", "XLF = Financial", "XLV = Health", "XLI = Industrial", "XLB = Materials", "XLRE = Real Estate", "XLK = Technology ", "XLU = Utilities"]
        axpos = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2], [3,0], [3,1], [3,2]]

        for i, val in enumerate(indices):
            sector = stock_daily(val, save=False)
            # calculating performance
            df.loc[val, "Day"] = np.round((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[len(sector.data)-2, "Close"]-1)*100,2)
            ytd =  np.where(sector.data["Date"].to_numpy() >= np.datetime64(dt.datetime(dt.datetime.today().year,1,1)))[0][0]
            df.loc[val,"YTD"] = np.round(((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[ytd, "Close"])-1)*100,2)
            df.loc[val,"MTD"] = np.round(((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[len(sector.data)-21, "Close"])-1)*100,2)
            # plots
            # red and green days
            green = sector.data.index.where(sector.data["Close"] >= sector.data["Open"])
            red = sector.data.index.where(sector.data["Close"] < sector.data["Open"])
            sma = ind.sma(sector.data, 100)["SMA"]
            bollb = ind.bollbands(sector.data, stdn=1)
            ax[axpos[i][0],axpos[i][1]].vlines(green, sector.data["Low"], sector.data["High"], color="g")
            # ax[axpos[i][0],axpos[i][1]].vlines(green, sector.data["Open"], sector.data["Close"], color="g", linewidth=3)
            ax[axpos[i][0],axpos[i][1]].scatter(green, sector.data["Open"], marker="_", color="g", s=10)
            ax[axpos[i][0],axpos[i][1]].scatter(green, sector.data["Close"], marker="_", color="g", s=10)
            
            ax[axpos[i][0],axpos[i][1]].vlines(red, sector.data["Low"], sector.data["High"], color="r")
            ax[axpos[i][0],axpos[i][1]].scatter(red, sector.data["Open"], marker="_", color="r", s=10)
            ax[axpos[i][0],axpos[i][1]].scatter(red, sector.data["Close"], marker="_", color="r", s=10)
            ax[axpos[i][0],axpos[i][1]].plot(sma, color="b")
            ax[axpos[i][0],axpos[i][1]].plot(bollb["upper"], color="b", alpha=0.3)
            ax[axpos[i][0],axpos[i][1]].plot(bollb["lower"], color="b", alpha=0.3)
            ax[axpos[i][0],axpos[i][1]].fill_between(np.arange(bollb.shape[0]), bollb["lower"], bollb["upper"], color="b", alpha=0.05)
            axy = ax[axpos[i][0],axpos[i][1]].twinx()
            axy.vlines(red, 0, sector.data["Volume"], color="r", alpha=0.5)
            axy.vlines(green, 0, sector.data["Volume"], color="g", alpha=0.5)
            axy.set_ylim([0, np.max(sector.data["Volume"][150:])*3.5])
            axy.set_yticklabels([])
            axy.set_yticks([])
            tick = np.linspace(150, sector.data.shape[0]-1, 6, dtype=int)
            ax[axpos[i][0],axpos[i][1]].set_xticks(tick)
            ax[axpos[i][0],axpos[i][1]].set_xticklabels(sector.data.loc[tick,"Date"].dt.strftime("%d/%m"))
            ax[axpos[i][0],axpos[i][1]].set_title(names[i], fontsize=20)
            ax[axpos[i][0],axpos[i][1]].set_xlim([150, sector.data.shape[0]])
            ax[axpos[i][0],axpos[i][1]].set_ylim([np.min(sector.data["Low"][150:])*0.9, np.max(sector.data["High"][150:])*1.05])
        ax[3,2].axis("off") 
        self.perf = df
        plt.show()

    def performance(self):
        perf = self.perf
        fig, ax = plt.subplots(ncols=3, figsize=(20,3))
        # day
        col = np.array(["g"]*len(perf))
        col[np.where(perf["Day"]<0)[0]] = "r"
        ax[0].bar(perf.index, perf["Day"], color=col, alpha=0.8, edgecolor="k")
        ax[0].set_title("Day performance", fontsize=20)
        ax[0].set_ylabel("Change [%]", fontsize=16)

        # month
        col = np.array(["g"]*len(perf))
        col[np.where(perf["MTD"]<0)[0]] = "r"
        ax[1].bar(perf.index, perf["MTD"], color=col, alpha=0.8, edgecolor="k")
        ax[1].set_title("MTD (20 trading days)", fontsize=20)

        # year
        col = np.array(["g"]*len(perf))
        col[np.where(perf["YTD"]<0)[0]] = "r"
        ax[2].bar(perf.index, perf["YTD"], color=col, alpha=0.8, edgecolor="k")
        ax[2].set_title("YTD", fontsize=20)

        plt.show()
        

class worldmarkets():
    def show(self):
        fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(20,8))

        indices = ["^HSI", "^N225", "STW.AX", "^FTMC", "^GDAXI"]
        performance = ["YTD", "MTD", "Day"]
        # dataframe for performance
        df = pd.DataFrame(index=indices, columns=performance)
        names = ["Hong Kong Hang Seng", "Japan Nikkei 225", "Australia ASX 200", "UK FTSE250", "Germany DAX"]
        axpos = [[0,0], [0,1], [0,2], [1,0], [1,1]]

        for i, val in enumerate(indices):
            sector = stock_daily(val, save=False)
            # calculating performance
            df.loc[val, "Day"] = np.round((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[len(sector.data)-2, "Close"]-1)*100,2)
            ytd =  np.where(sector.data["Date"].to_numpy() >= np.datetime64(dt.datetime(dt.datetime.today().year,1,1)))[0][0]
            df.loc[val,"YTD"] = np.round(((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[ytd, "Close"])-1)*100,2)
            df.loc[val,"MTD"] = np.round(((sector.data.loc[len(sector.data)-1, "Close"]/sector.data.loc[len(sector.data)-21, "Close"])-1)*100,2)
            # plots
            # red and green days
            green = sector.data.index.where(sector.data["Close"] >= sector.data["Open"])
            red = sector.data.index.where(sector.data["Close"] < sector.data["Open"])
            sma = ind.sma(sector.data, 100)["SMA"]
            bollb = ind.bollbands(sector.data, stdn=1)
            ax[axpos[i][0],axpos[i][1]].vlines(green, sector.data["Low"], sector.data["High"], color="g")
            ax[axpos[i][0],axpos[i][1]].scatter(green, sector.data["Open"], marker="_", color="g", s=10)
            ax[axpos[i][0],axpos[i][1]].scatter(green, sector.data["Close"], marker="_", color="g", s=10)
            ax[axpos[i][0],axpos[i][1]].vlines(red, sector.data["Low"], sector.data["High"], color="r")
            ax[axpos[i][0],axpos[i][1]].scatter(red, sector.data["Open"], marker="_", color="r", s=10)
            ax[axpos[i][0],axpos[i][1]].scatter(red, sector.data["Close"], marker="_", color="r", s=10)
            ax[axpos[i][0],axpos[i][1]].plot(sma, color="b")
            ax[axpos[i][0],axpos[i][1]].plot(bollb["upper"], color="b", alpha=0.3)
            ax[axpos[i][0],axpos[i][1]].plot(bollb["lower"], color="b", alpha=0.3)
            ax[axpos[i][0],axpos[i][1]].fill_between(np.arange(bollb.shape[0]), bollb["lower"], bollb["upper"], color="b", alpha=0.05)
            axy = ax[axpos[i][0],axpos[i][1]].twinx()
            axy.vlines(red, 0, sector.data["Volume"], color="r", alpha=0.5)
            axy.vlines(green, 0, sector.data["Volume"], color="g", alpha=0.5)
            axy.set_ylim([0, np.max(sector.data["Volume"][150:])*3.5])
            axy.set_yticklabels([])
            axy.set_yticks([])
            tick = np.linspace(150, sector.data.shape[0]-1, 6, dtype=int)
            ax[axpos[i][0],axpos[i][1]].set_xticks(tick)
            ax[axpos[i][0],axpos[i][1]].set_xticklabels(sector.data.loc[tick,"Date"].dt.strftime("%d/%m"))
            ax[axpos[i][0],axpos[i][1]].set_title(names[i], fontsize=20)
            ax[axpos[i][0],axpos[i][1]].set_xlim([150, sector.data.shape[0]])
            ax[axpos[i][0],axpos[i][1]].set_ylim([np.min(sector.data["Low"][150:])*0.9, np.max(sector.data["High"][150:])*1.05])
        self.perf = df
        ax[1,2].axis("off")
        plt.show()

    def performance(self):
            perf = self.perf
            fig, ax = plt.subplots(ncols=3, figsize=(20,3))
            # day
            col = np.array(["g"]*len(perf))
            col[np.where(perf["Day"]<0)[0]] = "r"
            ax[0].bar(perf.index, perf["Day"], color=col, alpha=0.8, edgecolor="k")
            ax[0].set_title("Day performance", fontsize=20)
            ax[0].set_ylabel("Change [%]", fontsize=16)

            # month
            col = np.array(["g"]*len(perf))
            col[np.where(perf["MTD"]<0)[0]] = "r"
            ax[1].bar(perf.index, perf["MTD"], color=col, alpha=0.8, edgecolor="k")
            ax[1].set_title("MTD (20 trading days)", fontsize=20)

            # year
            col = np.array(["g"]*len(perf))
            col[np.where(perf["YTD"]<0)[0]] = "r"
            ax[2].bar(perf.index, perf["YTD"], color=col, alpha=0.8, edgecolor="k")
            ax[2].set_title("YTD", fontsize=20)

            plt.show()

def show_usmarkets():
    spy = stock_daily("SPY", save=False)
    # calculating green and red days
    green = spy.data.index.where(spy.data["Close"] >= spy.data["Open"])
    red = spy.data.index.where(spy.data["Close"] < spy.data["Open"])
    # defining the figures
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20,6), gridspec_kw={'height_ratios': [3, 1]})
    rang = [150, spy.data.shape[0]]
    # SPY
    # plot closed prices and highlighted trades
    sma = ind.sma(spy.data, 100)["SMA"]
    bollb = ind.bollbands(spy.data, stdn=1)
    ax[0,0].vlines(green, spy.data["Low"], spy.data["High"], color="g")
    ax[0,0].scatter(green, spy.data["Open"], marker="_", color="g", s=10)
    ax[0,0].scatter(green, spy.data["Close"], marker="_", color="g", s=10)
    ax[0,0].vlines(red, spy.data["Low"], spy.data["High"], color="r")
    ax[0,0].scatter(red, spy.data["Open"], marker="_", color="r", s=10)
    ax[0,0].scatter(red, spy.data["Close"], marker="_", color="r", s=10)
    ax[0,0].plot(sma, color="b")
    ax[0,0].plot(bollb["upper"], color="b", alpha=0.3)
    ax[0,0].plot(bollb["lower"], color="b", alpha=0.3)
    ax[0,0].fill_between(np.arange(bollb.shape[0]), bollb["lower"], bollb["upper"], color="b", alpha=0.05)
    axy = ax[0,0].twinx()
    axy.vlines(red, 0, spy.data["Volume"], color="r")
    axy.vlines(green, 0, spy.data["Volume"], color="g")
    axy.set_ylim([0, np.max(spy.data["Volume"][150:])*3.5])
    axy.set_yticklabels([])
    axy.set_yticks([])
    ax[0,0].set_title("SPY", fontsize=16)
    ax[0,0].set_ylabel("Close price [USD]", fontsize=14)
    ax[0,0].set_xlim(rang)
    tick = np.linspace(rang[0], rang[1]-1, 6, dtype=int)
    ax[0,0].set_xticks(tick)
    ax[0,0].set_xticklabels(spy.data.loc[tick,"Date"].dt.strftime("%d/%m"))
    ax[0,0].set_ylim([np.min(spy.data["Low"][150:])*0.9, np.max(spy.data["High"][150:])*1.05])
    # plot VFI
    vfi = ind.vfi(spy.data, period=30, coef=0.2, vcoef=1.5)
    ax[1,0].plot(vfi["vfi"])
    ax[1,0].plot(vfi["vfi_smooth"])
    ax[1,0].vlines(spy.data.index, 0, vfi["histogram"], "k", alpha=0.5)
    ax[1,0].set_xlim(rang)
    ax[1,0].set_ylabel("VFI", fontsize=14)
    ax[1,0].set_xticks([])
    ax[1,0].set_xticklabels([])


    # IWM
    iwm = stock_daily("IWM", save=False)
    # calculating green and red days
    green = iwm.data.index.where(iwm.data["Close"] >= iwm.data["Open"])
    red = iwm.data.index.where(iwm.data["Close"] < iwm.data["Open"])
    rang = [150, iwm.data.shape[0]]
    # plot closed prices and highlighted trades
    sma = ind.sma(iwm.data, 100)["SMA"]
    bollb = ind.bollbands(iwm.data, stdn=1)
    ax[0,1].vlines(green, iwm.data["Low"], iwm.data["High"], color="g")
    ax[0,1].scatter(green, iwm.data["Open"], marker="_", color="g", s=10)
    ax[0,1].scatter(green, iwm.data["Close"], marker="_", color="g", s=10)
    ax[0,1].vlines(red, iwm.data["Low"], iwm.data["High"], color="r")
    ax[0,1].scatter(red, iwm.data["Open"], marker="_", color="r", s=10)
    ax[0,1].scatter(red, iwm.data["Close"], marker="_", color="r", s=10)
    ax[0,1].plot(sma, color="b")
    ax[0,1].plot(bollb["upper"], color="b", alpha=0.3)
    ax[0,1].plot(bollb["lower"], color="b", alpha=0.3)
    ax[0,1].fill_between(np.arange(bollb.shape[0]), bollb["lower"], bollb["upper"], color="b", alpha=0.05)
    # volume
    axy = ax[0,1].twinx()
    axy.vlines(red, 0, iwm.data["Volume"], color="r")
    axy.vlines(green, 0, iwm.data["Volume"], color="g")
    axy.set_ylim([0, np.max(iwm.data["Volume"][150:])*3.5])
    axy.set_yticklabels([])
    axy.set_yticks([])
    tick = np.linspace(rang[0], rang[1]-1, 6, dtype=int)
    ax[0,1].set_xticks(tick)
    ax[0,1].set_xticklabels(iwm.data.loc[tick,"Date"].dt.strftime("%d/%m"))
    ax[0,1].set_title("IWM", fontsize=16)
    ax[0,1].set_xlim(rang)
    ax[0,1].set_ylim([np.min(iwm.data["Low"][150:])*0.9, np.max(iwm.data["High"][150:])*1.05])
    # plot VFI
    vfi = ind.vfi(iwm.data, period=30, coef=0.2, vcoef=1.5)
    ax[1,1].plot(vfi["vfi"])
    ax[1,1].plot(vfi["vfi_smooth"])
    ax[1,1].vlines(iwm.data.index, 0, vfi["histogram"], "k", alpha=0.5)
    ax[1,1].set_xlim(rang)
    ax[1,1].set_xticks([])
    ax[1,1].set_xticklabels([])

    plt.show()

def longterm_usmarkets():
    tickers = ["SPY", "IWM"]

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20,3))

    for i, val in enumerate(tickers):
        stock = stock_daily(val, save=False)
        ax[i].set_title(val + " last year", fontsize=20)
        ax[i].plot(stock.data["Close"], color="b", linewidth=2)
        axy = ax[i].twinx()
        axy.fill_between(stock.data.index, stock.data["Volume"], alpha=0.5)
        # axy.vlines(stock.data.index, 0, stock.data["Volume"], color="tab:blue", linewidth=0.75, alpha=0.8)
        axy.set_ylim([0, np.max(stock.data["Volume"][150:])*3.5])
        axy.set_xlim([stock.data.index[0], stock.data.index[-1]])
        axy.set_yticklabels([])
        axy.set_yticks([])
        tick = np.linspace(stock.data.index[0], stock.data.index[-1]-1, 6, dtype=int)
        ax[i].set_xticks(tick)
        ax[i].set_xticklabels(stock.data.loc[tick,"Date"].dt.strftime("%d/%m"))
    ax[0].set_ylabel("Close price [USD]", fontsize=14)

    plt.show()

def momentum_usmarkets():
    # load the dataframe and compare the dates
    df = pd.read_excel("marketmomentum.xlsx", index_col=0)
    if df.loc[df.index[-1], "date"] != dt.date.today():
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
        ndf.loc[0, "date"] = dt.datetime.today()
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
        df.to_excel("marketmomentum.xlsx")
        # there is bug with the dates, its unable to set the xtickslabels properly when new row is added

    df["date"] = pd.to_datetime(df["date"])
    # plot the data
    fig, ax = plt.subplots(nrows=2, figsize=(20,6))
    # advancing
    ax[0].bar(df.index, df["advancing"], color="g", alpha=0.8, edgecolor="k")
    ax[0].bar(df.index, -df["declining"], color="r", alpha=0.8, edgecolor="k")
    ax[0].set_ylabel("Advancing & Declining", fontsize=14)
    ax[0].hlines(0, df.index[0]-1, df.index[-1]+1, color="k", linestyle="--", linewidth=1)
    ax[0].set_xlim([-0.5, df.index[-1]+0.5])
    ax[0].set_xticks(df.index)
    ax[0].set_xticklabels(df["date"].dt.strftime("%d/%m"))
    ax[0].yaxis.tick_right()
    # high lows
    col = np.array(["g"]*len(df["hldiff"]))
    col[np.where(df["hldiff"]<0)[0]] = "r"
    ax[1].bar(df.index, df["hldiff"], color=col, alpha=0.8, edgecolor="k")
    ax[1].set_ylabel("Highs-Lows", fontsize=14)
    ax[1].hlines(0, df.index[0]-1, df.index[-1]+1, color="k", linestyle="--", linewidth=1)
    ax[1].set_xlim([-0.5, df.index[-1]+0.5])
    ax[1].set_xticks(df.index)
    ax[1].set_xticklabels(df["date"].dt.strftime("%d/%m"))
    ax[1].yaxis.tick_right()
    # above 50sma
    # ax[2].bar(df.index, df["above50"], color="g", alpha=0.8, edgecolor="k")
    # ax[2].bar(df.index, -df["below50"], color="r", alpha=0.8, edgecolor="k")
    # ax[2].hlines(0, df.index[0]-1, df.index[-1]+1, color="k", linestyle="--", linewidth=1)
    # ax[2].set_xlim([-0.5, df.index[-1]+0.5])
    # ax[2].set_xticks(df.index)
    # ax[2].set_xticklabels(df["date"].dt.strftime("%d/%m"))
    # ax[2].set_title("Above and below 50 day SMA", fontsize=20)

    plt.show()

class screeners():
    def newhighs(self):
        # url for the specific screener
        url = "https://finviz.com/screener.ashx?v=411&s=ta_newhigh&f=ind_stocksonly,sh_avgvol_o100,sh_float_o5,sh_relvol_o1"
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
        url = "https://finviz.com/screener.ashx?v=411&f=fa_debteq_u1,fa_eps5years_o10,fa_sales5years_o10,ind_stocksonly,sh_avgvol_o100,sh_float_o5,sh_relvol_o1,ta_highlow50d_nh"
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        # create dataframe with the ticker names

        tickers = soup.find_all("span", onclick=lambda onclick: onclick and onclick.startswith("window.location='quote.ashx?t"))
        return pd.DataFrame(data={"Tickers": (val.text for i, val in enumerate(tickers))})

    def potentialreversal(self):
        # url for the specific screener
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
        url = "https://finviz.com/screener.ashx?v=411&f=ind_stocksonly,sh_avgvol_o400,sh_curvol_o2000,sh_relvol_o1,ta_sma20_pa,ta_sma50_pb&o=-perf1w"
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        # create dataframe with the ticker names

        tickers = soup.find_all("span", onclick=lambda onclick: onclick and onclick.startswith("window.location='quote.ashx?t"))
        return pd.DataFrame(data={"Tickers": (val.text for i, val in enumerate(tickers))})

    def prettify(self, df, nrows=10):
        # nested function fot clickable links to results
        def make_clickable(val):
            # target _blank to open new window
            return '<a target="_blank" href="https://finviz.com/quote.ashx?t={}" style="text-decoration: none">{}</a>'.format(val, val)
        
        if (df.shape[0] % nrows) > 0:
            em = np.zeros(nrows-(df.shape[0] % nrows)).astype(str)
            em[:] = " "
            arr = np.concatenate((np.array([df["Tickers"].values]), em), axis=None)
        else:
            arr = np.array([df["Tickers"].values])
        return pd.DataFrame(arr.reshape(nrows, -1)).style.format(make_clickable)

    def newipos(self):
        # url for the specific screener
        url = "https://finviz.com/screener.ashx?v=151&f=ipodate_prevweek&o=ipodate"
        # scrape the data
        req = Request(url, headers={'User-Agent': "Chrome/95.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        # create dataframe with the ticker names
        return soup

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
        scrapedvals = scrapedvals.set_index(scrapedvals["label"].values).reindex(row) # redefine index and sort it so it corresponds to how "row" is sorted
        return scrapedvals["perf"]

    def returnfutures(self):
        # define dataframe
        # problem, currently cannot scrap year as the ast.literal_eval() function get stuck on ethanol which returns null for some reason
        col = ["Day [%]", "Week [%]", "Month [%]", "Quarter [%]"] 
        finvizcolumn = ["11", "12", "13", "14"] # number is last part of finviz url for scraping, corresponds to columns in col
        row = ["Natural Gas", "Crude Oil WTI", "Crude Oil Brent", "Ethanol", "Palladium", "Copper", "Platinum", "Silver", "Gold", "Lumber", "Cotton", "Cocoa", "Sugar", "Coffee",
                "Rough Rice", "Wheat", "Corn", "Oats", "USD", "EUR", "5 Year Note", "10 Year Note", "30 Year Bond"]
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
        return table.style.format("{:.2f}").applymap(style_negative, props='color:red;').applymap(style_positive, props='color:green;')

# ------------------------- testing / editing of functions and classes

def main():

    return

if __name__ == '__main__':
    main()


