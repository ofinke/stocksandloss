# this is a group of functions for market status notebook to save space

from scraper import stock_daily
import matplotlib.pyplot as plt
import indicators as ind
import pandas as pd
import numpy as np
import datetime as dt

class sectors():
    def show(self):
        # define figure
        fig, ax = plt.subplots(ncols=3, nrows=4, figsize=(25,18))

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
            ax[axpos[i][0],axpos[i][1]].vlines(green, sector.data["Low"], sector.data["High"], color="g")
            # ax[axpos[i][0],axpos[i][1]].vlines(green, sector.data["Open"], sector.data["Close"], color="g", linewidth=3)
            ax[axpos[i][0],axpos[i][1]].scatter(green, sector.data["Open"], marker="_", color="g", s=10)
            ax[axpos[i][0],axpos[i][1]].scatter(green, sector.data["Close"], marker="_", color="g", s=10)
            
            ax[axpos[i][0],axpos[i][1]].vlines(red, sector.data["Low"], sector.data["High"], color="r")
            ax[axpos[i][0],axpos[i][1]].scatter(red, sector.data["Open"], marker="_", color="r", s=10)
            ax[axpos[i][0],axpos[i][1]].scatter(red, sector.data["Close"], marker="_", color="r", s=10)
            ax[axpos[i][0],axpos[i][1]].plot(sma, color="b")
            ax[axpos[i][0],axpos[i][1]].plot(ind.ema(sector.data, 13)["EMA"], "y")
            ax[axpos[i][0],axpos[i][1]].plot(ind.ema(sector.data, 26)["EMA"], color="tab:orange")
            axy = ax[axpos[i][0],axpos[i][1]].twinx()
            axy.vlines(red, 0, sector.data["Volume"], color="r", alpha=0.5)
            axy.vlines(green, 0, sector.data["Volume"], color="g", alpha=0.5)
            axy.set_ylim([0, np.max(sector.data["Volume"][150:])*3.5])
            axy.set_yticklabels([])
            axy.set_yticks([])
            ax[axpos[i][0],axpos[i][1]].set_title(names[i], fontsize=20)
            ax[axpos[i][0],axpos[i][1]].set_xlim([150, sector.data.shape[0]])
            ax[axpos[i][0],axpos[i][1]].set_ylim([np.min(sector.data["Low"][150:])*0.9, np.max(sector.data["High"][150:])*1.05])
        ax[3,2].axis("off") 
        self.perf = df
        plt.show()

    def performance(self):
        perf = self.perf
        fig, ax = plt.subplots(ncols=3, figsize=(25,4))
        # day
        col = np.array(["g"]*len(perf))
        col[np.where(perf["Day"]<0)[0]] = "r"
        ax[0].bar(perf.index, perf["Day"], color=col, alpha=0.8)
        ax[0].set_title("Day performance", fontsize=20)
        ax[0].set_ylabel("Change [%]", fontsize=16)

        # month
        col = np.array(["g"]*len(perf))
        col[np.where(perf["MTD"]<0)[0]] = "r"
        ax[1].bar(perf.index, perf["MTD"], color=col, alpha=0.8)
        ax[1].set_title("MTD (20 trading days)", fontsize=20)

        # year
        col = np.array(["g"]*len(perf))
        col[np.where(perf["YTD"]<0)[0]] = "r"
        ax[2].bar(perf.index, perf["YTD"], color=col, alpha=0.8)
        ax[2].set_title("YTD", fontsize=20)

        plt.show()
        

class worldmarkets():
    def show(self):
        fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(25,9))

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
            ax[axpos[i][0],axpos[i][1]].vlines(green, sector.data["Low"], sector.data["High"], color="g")
            ax[axpos[i][0],axpos[i][1]].scatter(green, sector.data["Open"], marker="_", color="g", s=10)
            ax[axpos[i][0],axpos[i][1]].scatter(green, sector.data["Close"], marker="_", color="g", s=10)
            ax[axpos[i][0],axpos[i][1]].vlines(red, sector.data["Low"], sector.data["High"], color="r")
            ax[axpos[i][0],axpos[i][1]].scatter(red, sector.data["Open"], marker="_", color="r", s=10)
            ax[axpos[i][0],axpos[i][1]].scatter(red, sector.data["Close"], marker="_", color="r", s=10)
            ax[axpos[i][0],axpos[i][1]].plot(sma, color="b")
            ax[axpos[i][0],axpos[i][1]].plot(ind.ema(sector.data, 13)["EMA"], "y")
            ax[axpos[i][0],axpos[i][1]].plot(ind.ema(sector.data, 26)["EMA"], color="tab:orange")
            axy = ax[axpos[i][0],axpos[i][1]].twinx()
            axy.vlines(red, 0, sector.data["Volume"], color="r", alpha=0.5)
            axy.vlines(green, 0, sector.data["Volume"], color="g", alpha=0.5)
            axy.set_ylim([0, np.max(sector.data["Volume"][150:])*3.5])
            axy.set_yticklabels([])
            axy.set_yticks([])
            ax[axpos[i][0],axpos[i][1]].set_title(names[i], fontsize=20)
            ax[axpos[i][0],axpos[i][1]].set_xlim([150, sector.data.shape[0]])
            ax[axpos[i][0],axpos[i][1]].set_ylim([np.min(sector.data["Low"][150:])*0.9, np.max(sector.data["High"][150:])*1.05])
        self.perf = df
        ax[1,2].axis("off")
        plt.show()

    def performance(self):
            perf = self.perf
            fig, ax = plt.subplots(ncols=3, figsize=(25,4))
            # day
            col = np.array(["g"]*len(perf))
            col[np.where(perf["Day"]<0)[0]] = "r"
            ax[0].bar(perf.index, perf["Day"], color=col, alpha=0.8)
            ax[0].set_title("Day performance", fontsize=20)
            ax[0].set_ylabel("Change [%]", fontsize=16)

            # month
            col = np.array(["g"]*len(perf))
            col[np.where(perf["MTD"]<0)[0]] = "r"
            ax[1].bar(perf.index, perf["MTD"], color=col, alpha=0.8)
            ax[1].set_title("MTD (20 trading days)", fontsize=20)

            # year
            col = np.array(["g"]*len(perf))
            col[np.where(perf["YTD"]<0)[0]] = "r"
            ax[2].bar(perf.index, perf["YTD"], color=col, alpha=0.8)
            ax[2].set_title("YTD", fontsize=20)

            plt.show()

def show_usmarkets():
    spy = stock_daily("SPY", save=False)
    # calculating green and red days
    green = spy.data.index.where(spy.data["Close"] >= spy.data["Open"])
    red = spy.data.index.where(spy.data["Close"] < spy.data["Open"])
    # defining the figures
    fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(25,12), gridspec_kw={'height_ratios': [3, 1, 1]})
    rang = [150, spy.data.shape[0]]
    # SPY
    # plot closed prices and highlighted trades
    sma = ind.sma(spy.data, 100)["SMA"]
    ax[0,0].vlines(green, spy.data["Low"], spy.data["High"], color="g")
    ax[0,0].scatter(green, spy.data["Open"], marker="_", color="g", s=10)
    ax[0,0].scatter(green, spy.data["Close"], marker="_", color="g", s=10)
    ax[0,0].vlines(red, spy.data["Low"], spy.data["High"], color="r")
    ax[0,0].scatter(red, spy.data["Open"], marker="_", color="r", s=10)
    ax[0,0].scatter(red, spy.data["Close"], marker="_", color="r", s=10)
    ax[0,0].plot(sma, color="b")
    ax[0,0].plot(ind.ema(spy.data, 13)["EMA"], "y")
    ax[0,0].plot(ind.ema(spy.data, 26)["EMA"], color="tab:orange")
    axy = ax[0,0].twinx()
    axy.vlines(red, 0, spy.data["Volume"], color="r")
    axy.vlines(green, 0, spy.data["Volume"], color="g")
    axy.set_ylim([0, np.max(spy.data["Volume"][150:])*3.5])
    axy.set_yticklabels([])
    axy.set_yticks([])
    ax[0,0].set_title("SPY", fontsize=20)
    ax[0,0].set_ylabel("Close price [USD]", fontsize=14)
    ax[0,0].set_xlim(rang)
    ax[0,0].set_ylim([np.min(spy.data["Low"][150:])*0.9, np.max(spy.data["High"][150:])*1.05])
    # Plot double stochastic oscillator, 21 and 5
    st_fast = ind.stoch(spy.data, period=21, sk=2, sd=5)
    st_slow = ind.stoch(spy.data, period=5, sk=2, sd=3)
    ax[1,0].plot(st_slow["k"], "b--", alpha=0.4)
    ax[1,0].plot(st_slow["d"], "b", alpha=0.4)
    ax[1,0].plot(st_fast["k"], "c--", alpha=0.4)
    ax[1,0].plot(st_fast["d"], "c", alpha=0.4)
    ax[1,0].fill_between(np.arange(spy.data.shape[0]), st_slow["k"], st_slow["d"], where=(st_slow["k"] >= st_slow["d"]), interpolate=True, facecolor="green", alpha=0.4)
    ax[1,0].fill_between(np.arange(spy.data.shape[0]), st_slow["k"], st_slow["d"], where=(st_slow["k"] < st_slow["d"]), interpolate=True, facecolor="red", alpha=0.4)
    ax[1,0].fill_between(np.arange(spy.data.shape[0]), st_fast["k"], st_fast["d"], where=(st_fast["k"] >= st_fast["d"]), interpolate=True, facecolor="green", alpha=0.4)
    ax[1,0].fill_between(np.arange(spy.data.shape[0]), st_fast["k"], st_fast["d"], where=(st_fast["k"] < st_fast["d"]), interpolate=True, facecolor="red", alpha=0.4)
    # y lines for stochastic
    ax[1,0].plot(np.arange(spy.data.shape[0]), 80*np.ones(spy.data.shape[0]), "k--", alpha=0.5)
    ax[1,0].plot(np.arange(spy.data.shape[0]), 50*np.ones(spy.data.shape[0]), "r--", alpha=0.5)
    ax[1,0].plot(np.arange(spy.data.shape[0]), 20*np.ones(spy.data.shape[0]), "k--", alpha=0.5)
    ax[1,0].set_xlim(rang)
    ax[1,0].set_ylabel("Double stochastic", fontsize=14)
    ax[1,0].set_xticks([])
    ax[1,0].set_xticklabels([])
    # plot VFI
    vfi = ind.vfi(spy.data, period=30, coef=0.2, vcoef=1.5)
    ax[2,0].plot(vfi["vfi"])
    ax[2,0].plot(vfi["vfi_smooth"])
    ax[2,0].vlines(spy.data.index, 0, vfi["histogram"], "k", alpha=0.5)
    ax[2,0].set_xlim(rang)
    ax[2,0].set_ylabel("VFI", fontsize=14)
    ax[2,0].set_xticks([])
    ax[2,0].set_xticklabels([])


    # IWM
    iwm = stock_daily("IWM", save=False)
    # calculating green and red days
    green = iwm.data.index.where(iwm.data["Close"] >= iwm.data["Open"])
    red = iwm.data.index.where(iwm.data["Close"] < iwm.data["Open"])
    rang = [150, iwm.data.shape[0]]
    # plot closed prices and highlighted trades
    sma = ind.sma(iwm.data, 100)["SMA"]
    ax[0,1].vlines(green, iwm.data["Low"], iwm.data["High"], color="g")
    ax[0,1].scatter(green, iwm.data["Open"], marker="_", color="g", s=10)
    ax[0,1].scatter(green, iwm.data["Close"], marker="_", color="g", s=10)
    ax[0,1].vlines(red, iwm.data["Low"], iwm.data["High"], color="r")
    ax[0,1].scatter(red, iwm.data["Open"], marker="_", color="r", s=10)
    ax[0,1].scatter(red, iwm.data["Close"], marker="_", color="r", s=10)
    ax[0,1].plot(sma, "b")
    ax[0,1].plot(ind.ema(iwm.data, 13)["EMA"], "y")
    ax[0,1].plot(ind.ema(iwm.data, 26)["EMA"], color="tab:orange")
    # volume
    axy = ax[0,1].twinx()
    axy.vlines(red, 0, iwm.data["Volume"], color="r")
    axy.vlines(green, 0, iwm.data["Volume"], color="g")
    axy.set_ylim([0, np.max(iwm.data["Volume"][150:])*3.5])
    axy.set_yticklabels([])
    axy.set_yticks([])
    ax[0,1].set_title("IWM", fontsize=20)
    ax[0,1].set_xlim(rang)
    ax[0,1].set_ylim([np.min(iwm.data["Low"][150:])*0.9, np.max(iwm.data["High"][150:])*1.05])
    # Plot double stochastic oscillator, 21 and 5
    st_fast = ind.stoch(iwm.data, period=21, sk=2, sd=5)
    st_slow = ind.stoch(iwm.data, period=5, sk=2, sd=3)
    ax[1,1].plot(st_slow["k"], "b--", alpha=0.4)
    ax[1,1].plot(st_slow["d"], "b", alpha=0.4)
    ax[1,1].plot(st_fast["k"], "c--", alpha=0.4)
    ax[1,1].plot(st_fast["d"], "c", alpha=0.4)
    ax[1,1].fill_between(np.arange(iwm.data.shape[0]), st_slow["k"], st_slow["d"], where=(st_slow["k"] >= st_slow["d"]), interpolate=True, facecolor="green", alpha=0.4)
    ax[1,1].fill_between(np.arange(iwm.data.shape[0]), st_slow["k"], st_slow["d"], where=(st_slow["k"] < st_slow["d"]), interpolate=True, facecolor="red", alpha=0.4)
    ax[1,1].fill_between(np.arange(iwm.data.shape[0]), st_fast["k"], st_fast["d"], where=(st_fast["k"] >= st_fast["d"]), interpolate=True, facecolor="green", alpha=0.4)
    ax[1,1].fill_between(np.arange(iwm.data.shape[0]), st_fast["k"], st_fast["d"], where=(st_fast["k"] < st_fast["d"]), interpolate=True, facecolor="red", alpha=0.4)
    # y lines for stochastic
    ax[1,1].plot(np.arange(iwm.data.shape[0]), 80*np.ones(iwm.data.shape[0]), "k--", alpha=0.5)
    ax[1,1].plot(np.arange(iwm.data.shape[0]), 50*np.ones(iwm.data.shape[0]), "r--", alpha=0.5)
    ax[1,1].plot(np.arange(iwm.data.shape[0]), 20*np.ones(iwm.data.shape[0]), "k--", alpha=0.5)
    ax[1,1].set_xlim(rang)
    ax[1,1].set_xticks([])
    ax[1,1].set_xticklabels([])
    # plot VFI
    vfi = ind.vfi(iwm.data, period=30, coef=0.2, vcoef=1.5)
    ax[2,1].plot(vfi["vfi"])
    ax[2,1].plot(vfi["vfi_smooth"])
    ax[2,1].vlines(iwm.data.index, 0, vfi["histogram"], "k", alpha=0.5)
    ax[2,1].set_xlim(rang)
    ax[2,1].set_xticks([])
    ax[2,1].set_xticklabels([])

    plt.show()