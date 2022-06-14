# DAILY SCRAPER
# keeps last year of data for particular stock
# data are stored in csv and updated from last scrap from yahoo finance
# inputs:
#   ticker: string of stock ticker as presented on the stock exchange
# outputs:
#   self.data: pandas dataframe with 1 year of daily data

# IMPORTS
import pandas as pd
import datetime as dt
import yfinance as yf
import numpy as np
import os
import time

# scrapes daily data and supports saving and updating them in csv
class stock_daily():
    # CONSTRUCTOR
    def __init__(self, ticker, save=True, edate=dt.date.today(), delta=dt.timedelta(days=365), pth=os.getcwd()):
        # check if ticker is defined correctly
        self.ticker = ticker
        # try opening csv
        # if csv exists and , open it and update it
        if save == True:
            if os.path.isfile(pth + "\\" + self.ticker + "_daily.csv"):
                self.updatecsv(edate=edate, delta=delta, pth=pth)
            else:
                self.createcsv(edate=edate, delta=delta, pth=pth)
        else:
            self.scrap(startdate=edate-delta, enddate=edate)
            self.data = self.scraped
            del self.scraped
        return

    # METHODS
    def scrap(self, startdate, enddate):
        # create yfinance object
        st = yf.Ticker(self.ticker)
        # download daily data from startdate to enddate withou splits and dividends
        self.scraped = st.history(start=startdate, end=enddate, interval="1d", actions=False)
        self.scraped = self.scraped.reset_index().rename(columns={self.scraped.index.name:"Date"})
        return

    def createcsv(self, edate, delta, pth):
        # scrape data from today - 1 year
        try:
            self.scrap(startdate=edate-delta, enddate=edate)
            # save data into csv
            self.scraped.to_csv(pth + "\\" + self.ticker + "_daily.csv", index=False)
            # save data into self.data
            self.data = self.scraped
            del self.scraped    
        except:
            raise RuntimeError("Couldn't scrape data")
        return

    def updatecsv(self, edate, delta, pth):
        # load csv
        self.loaded = pd.read_csv(pth + "\\" + self.ticker + "_daily.csv")
        # changing date format back to timestamp
        self.loaded["Date"] = self.loaded["Date"].astype("datetime64[ns]")
        # check date of latest data in the csv
        # scrape missing data from last business day to latest stored day in csv
        lastDay = self.loaded.iloc[-1, 0]
        delta = edate - dt.date(lastDay.year, lastDay.month, lastDay.day)
        # add shift by weekday, on monday -2, on sunday -1
        if delta.days > 1:
            # try downloading new data, if it fails, pass loaded data from csv
            try:
                # scrap data from the last day in the table to today
                self.scrap(startdate=self.loaded.iloc[-1, 0], enddate=dt.date.today())
                # find index corresponding to lastDay variable in scraped data and delete everything before it 
                i = self.scraped.set_index("Date").index.get_loc(lastDay)
                self.scraped = self.scraped.drop(self.scraped.index[:i+1])
                # if no new data are present, return loaded data
                if self.scraped.empty:
                    self.data = self.loaded
                    del self.scraped
                # else add the data to the loaded table and save them into csv, and pass them
                else: 
                    self.data = pd.concat([self.loaded, self.scraped], ignore_index=True)
                    self.data.to_csv(pth + "\\" + self.ticker + "_daily.csv", index=False)
            except:
                # pass loaded data of the datascraping fails for some reason
                # (if the get_loc() doesnt find anything, it just throws error instead of -1 or something like that)
                print("Data scraping failed, passing old saved data")
                self.data = self.loaded 
        else:
            self.data = self.loaded 
        del self.loaded

        return

# scrapes weekly data, doesn't support save/load
class stock_weekly():
    def __init__(self, ticker, edate=dt.date.today(), delta=dt.timedelta(days=365)):
        self.ticker = ticker
        self.scrap(startdate=edate-delta, enddate=edate)
        self.data = self.scraped
        return
    
    # METHODS
    def scrap(self, startdate, enddate):
        # create yfinance object
        st = yf.Ticker(self.ticker)
        # download daily data from startdate to enddate withou splits and dividends
        self.scraped = st.history(start=startdate, end=enddate, interval="1wk", actions=False)
        self.scraped = self.scraped.reset_index().rename(columns={self.scraped.index.name:"Date"})
        return

# scrapes eps data, automatically updates them in file
class stock_eps():
    def __init__(self, ticker):
        self.ticker = ticker

        st = yf.Ticker(self.ticker)

        print(st.financials)
        return


# RUNTIME
# testing script runtime
def main():
    stock_eps("MSFT")
    return

if __name__ == "__main__":
    main()
