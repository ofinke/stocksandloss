import scraper as sc
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
import indicators as ind
import time
import datetime as dt

class setup_image():
    # CONSTRUCTOR
    # scrapes all the important data
    def __init__(self, ticker, lines=None):
        self.ticker = ticker
        
        self.day_data = sc.stock_daily(self.ticker, save=False, delta=dt.timedelta(days=730)).data
        time.sleep(1) # yfinance sometimes fucks up if I have too much requrests
        self.week_data = sc.stock_weekly(self.ticker).data

        # create the image figure
        self.create_figure()
        
        # add lines if defined
        return

    # METHODS
    def add_line(self, axis, prop):
        # add lines into the axes instance using line properties
        return axis
    def create_figure(self):
        # create the figure
        # define figure
        fig = plt.figure(figsize=(12,10))
        gs = gridspec.GridSpec(2,2, hspace=0.12, width_ratios=[1.5,1], height_ratios=[1,1.2])
        # plot weekly
        gw = self.week_data.index.where(self.week_data["Close"] >= self.week_data["Open"])
        rw = self.week_data.index.where(self.week_data["Close"] < self.week_data["Open"])
        smaw = ind.sma(self.week_data, 10)["SMA"]
        ngsw = gs[0,1].subgridspec(2,1, hspace=0, height_ratios=[3,1]) # subgridspec
        axw = fig.add_subplot(ngsw[0,0])
        axw.text(0.03, 0.96, "weekly, log", ha="left", va="top", transform=axw.transAxes, weight="bold")
        axw.vlines(gw, self.week_data["Low"], self.week_data["High"], color="g", alpha=0.7)
        axw.scatter(gw, self.week_data["Open"], marker="_", color="g", s=10, alpha=0.7)
        axw.scatter(gw, self.week_data["Close"], marker="_", color="g", s=10, alpha=0.7)
        axw.vlines(rw, self.week_data["Low"], self.week_data["High"], color="r", alpha=0.7)
        axw.scatter(rw, self.week_data["Open"], marker="_", color="r", s=10, alpha=0.7)
        axw.scatter(rw, self.week_data["Close"], marker="_", color="r", s=10, alpha=0.7)
        axw.plot(smaw, color="b", alpha=0.5)
        axw.set_yticks([])
        axw.set_xticklabels([])
        axw.set_xticks([])
        axw.set_yscale("log")
        # weekly volume
        smawv = ind.sma(self.week_data, 10, price="Volume")["SMA"]
        axwv = fig.add_subplot(ngsw[1,0])
        axwv.vlines(rw, 0, self.week_data["Volume"], color="r", alpha=0.7)
        axwv.vlines(gw, 0, self.week_data["Volume"], color="g", alpha=0.7)
        axwv.plot(smawv, color="b", alpha=0.5)
        axwv.set_yticklabels([])
        axwv.set_yticks([])

        # plot daily
        smadf = ind.sma(self.day_data, 50)["SMA"]
        smadh = ind.sma(self.day_data, 100)["SMA"]
        smadt = ind.sma(self.day_data, 200)["SMA"]
        gd = self.day_data.index.where(self.day_data["Close"] >= self.day_data["Open"])
        rd = self.day_data.index.where(self.day_data["Close"] < self.day_data["Open"])
        if (self.day_data.shape[0]-150) < 0:
            rang = [0, self.day_data.shape[0]]
        else:
            rang = [self.day_data.shape[0]-150, self.day_data.shape[0]]
        ngsd = gs[1,:].subgridspec(2,1, hspace=0, height_ratios=[3,1]) # subgridspec
        axd = fig.add_subplot(ngsd[0,0])
        axd.text(0.015, 0.95, "daily", ha="left", va="top", transform=axd.transAxes, weight="bold")
        axd.vlines(gd, self.day_data["Low"], self.day_data["High"], color="g", alpha=0.7)
        axd.scatter(gd, self.day_data["Open"], marker="_", color="g", s=10, alpha=0.7)
        axd.scatter(gd, self.day_data["Close"], marker="_", color="g", s=10, alpha=0.7)
        axd.vlines(rd, self.day_data["Low"], self.day_data["High"], color="r", alpha=0.7)
        axd.scatter(rd, self.day_data["Open"], marker="_", color="r", s=10, alpha=0.7)
        axd.scatter(rd, self.day_data["Close"], marker="_", color="r", s=10, alpha=0.7)
        axd.plot(smadf, color="k", alpha=0.5)
        axd.plot(smadh, color="seagreen", alpha=0.5)
        axd.plot(smadt, color="orange")
        axd.set_xlim(rang)
        avprice = np.mean(self.day_data["High"][-150:])/10
        axd.set_ylim([np.min(self.day_data["Low"][-150:]-avprice), np.max(self.day_data["High"][-150:])+avprice])
        axd.set_xticklabels([])
        axd.set_xticks([])
        # daily volume
        axdv = fig.add_subplot(ngsd[1,0])
        axdv.vlines(rd, 0, self.day_data["Volume"], color="r", alpha=0.7)
        axdv.vlines(gd, 0, self.day_data["Volume"], color="g", alpha=0.7)
        axdv.set_xlim(rang)
        axdv.set_ylim([0, np.max(self.day_data["Volume"][-150:])])
        tick = np.linspace(rang[0], rang[1]-1, 6, dtype=int)
        axdv.set_xticks(tick)
        axdv.set_xticklabels(self.day_data.loc[tick,"Date"].dt.strftime("%d/%m"))
        axdv.set_yticklabels([])
        axdv.set_yticks([])

        # write results
        axt = fig.add_subplot(gs[0,0])
        axt.set_axis_off()
        axt.text(0.015, 0.96, self.ticker, ha="left", va="top", transform=axt.transAxes, weight="bold")

        # save figure into the object instance
        self.figure = fig

        return
    def save_figure(self):
        # saves the figure as png
        return

# ------------------------- testing / editing of functions and classes
def main():
    s = setup_image("GDYN")
    plt.show()
    return

if __name__ == '__main__':
    main()
