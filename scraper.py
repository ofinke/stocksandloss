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
import os

class stock_daily():
    def __init__(self, ticker):
        # check if ticker is defined correctly

        self.ticker = ticker
        # try opening csv
        #   if csv exists, open it and update it
        if os.path.isfile(os.getcwd() + "\\" + self.ticker + "_daily.csv"):
            self.updatecsv()
        #   if csv doesnt exists, create new one
        else:
            self.createcsv()
        return
    
    def scrap(self, startdate, enddate):
        # create yfinance object
        st = yf.Ticker(self.ticker)
        # download daily data from startdate to enddate withou splits and dividends
        self.scraped = st.history(start=startdate, end=enddate, interval="1d", actions=False)
        return

    def createcsv(self):
        # scrape data from today - 1 year
        # (update in the future to scrape from last bussiness day)
        self.scrap(startdate=dt.date.today()-dt.timedelta(days=365), enddate=dt.date.today())
        # save data into csv
        self.scraped.to_csv(self.ticker + "_daily.csv")
        # save data into self.data
        self.data = self.scraped
        del self.scraped
        return

    def updatecsv(self):
        # load csv
        self.loaded = pd.read_csv(os.getcwd() + "\\" + self.ticker + "_daily.csv")
        # check date of latest data in the csv
        # scrape missing data from last business day to latest stored day in csv
        lastDay = dt.datetime.strptime(self.loaded["Date"].iloc[-1], "%Y-%m-%d").date()
        offset = max(1, (dt.date.today().weekday() + 6) % 7 - 3) 
        delta = dt.date.today() - dt.timedelta(days=offset) - lastDay
        if delta.days > 0:
            self.scrap(startdate=self.loaded["Date"].iloc[-1], enddate=dt.date.today())
            return
        # merge scraped and loaded data

        # update csv

        # save current data in self.data
        self.data = self.loaded 
        return


# RUNTIME
# testing script runtime
def main():
    s = stock_daily("TSLA")
    return

if __name__ == "__main__":
    main()
