# this is a group of functions for market status notebook to save space

from scraper import stock_daily
import matplotlib.pyplot as plt
import indicators as ind
import pandas as pd
import numpy as np

def show_indices():
    spy = stock_daily("SPY")
    iwm = stock_daily("IWM")

    fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(25,12), gridspec_kw={'height_ratios': [3, 1, 1]})
    rang = [150, spy.data.shape[0]]
    # SPY
    # plot closed prices and highlighted trades
    sma = ind.sma(spy.data, 100)["SMA"]
    ax[0,0].plot(spy.data["Close"], color="b")
    ax[0,0].plot(sma)
    ax[0,0].set_title("SPY", fontsize=20)
    ax[0,0].set_ylabel("Close price [USD]", fontsize=14)
    ax[0,0].set_xlim(rang)
    ax[0,0].set_ylim([np.min(sma[150:])*0.9, np.max(sma[150:])*1.1])
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
    # plot VFI
    vfi = ind.vfi(spy.data, period=30, coef=0.2, vcoef=1.5)
    ax[2,0].plot(vfi["vfi"])
    ax[2,0].plot(vfi["vfi_smooth"])
    ax[2,0].plot(np.arange(spy.data.shape[0]), np.zeros(spy.data.shape[0]), "k--", alpha=0.5)
    ax[2,0].set_xlim(rang)
    ax[2,0].set_xlabel("Index [-]", fontsize=16)
    ax[2,0].set_ylabel("VFI", fontsize=14)

    # IWM
    rang = [150, iwm.data.shape[0]]
    # plot closed prices and highlighted trades
    sma = ind.sma(iwm.data, 100)["SMA"]
    ax[0,1].plot(iwm.data["Close"], color="b")
    ax[0,1].plot(sma)
    ax[0,1].set_title("IWM", fontsize=20)
    ax[0,1].set_xlim(rang)
    ax[0,1].set_ylim([np.min(sma[150:])*0.9, np.max(sma[150:])*1.1])
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
    # plot VFI
    vfi = ind.vfi(iwm.data, period=30, coef=0.2, vcoef=1.5)
    ax[2,1].plot(vfi["vfi"])
    ax[2,1].plot(vfi["vfi_smooth"])
    ax[2,1].plot(np.arange(iwm.data.shape[0]), np.zeros(iwm.data.shape[0]), "k--", alpha=0.5)
    ax[2,1].set_xlim(rang)
    ax[2,1].set_xlabel("Index [-]", fontsize=16)
    plt.show()
    return