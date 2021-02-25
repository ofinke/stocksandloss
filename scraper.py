#    _____                                
#   / ___/______________ _____  ___  _____
#   \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
#  ___/ / /__/ /  / /_/ / /_/ /  __/ /    
# /____/\___/_/   \__,_/ .___/\___/_/     
#                     /_/                 
#
# ================================================
#
# Program to scrap useful data about stocks from the web

# IMPORTS
import pandas as pd
import datetime as dt

# scraping modules
#import twitterscraper as ts check if this doesnt send some weird shit somewhere
import yfinance as yf

class scrap():

    def __init__(self, stockHandle, ndays=7, method="All", period="1m"):
        # constructor calls methods specified by the user 
        # modyfies data and returns object with:
        # self.data => pandas dataframe with stock market data
        # self.info => information about scraped stock

        print("   _____                                ")
        print("  / ___/______________ _____  ___  _____")
        print("  \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/")
        print(" ___/ / /__/ /  / /_/ / /_/ /  __/ /    ")
        print("/____/\___/_/   \__,_/ .___/\___/_/     ")
        print("                    /_/                 ")
        print("\nVersion 0.1")
        print("\nScraping for stock(s): " + stockHandle)


        self.scrapstockdata(stockHandle, ndays, period)
        # self.scraptwitter(stockHandle, ndays)
        
        print("\nScraping completed")

    def scraptwitter(self, stockHandle, ndays):
        
        print("\nScraping https://twitter.com/")
        print("Status: Failed (scraper not implemented)")
        
        # query

    def scrapstockdata(self, stockHandle, ndays, period):
        # use yfinance
        print("\nScraping https://finance.yahoo.com/")
        print("Status: started")

        stockTicket = yf.Ticker(stockHandle)

        # scrape relevant data
        print("Status: scraping last " + str(ndays) + " day(s)")
        self.datadays = stockTicket.history(start=(dt.date.today() - dt.timedelta(days=ndays)), end=dt.date.today(), interval=period)
        self.datadays.reset_index(inplace=True)
        # Calculate elapsed days
        base_date = self.datadays['Datetime'][0]
        self.datadays['day_num'] = self.datadays['Datetime'].map(lambda date:(date - base_date).days)

        print("Status: scraping last year")
        self.datayear = stockTicket.history(start=(dt.date.today() - dt.timedelta(days=365)), end=dt.date.today(), interval="1d")
        self.datayear.reset_index(inplace=True)
        base_date = self.datayear['Date'][0]
        self.datayear['day_num'] = self.datayear['Date'].map(lambda date:(date - base_date).days)
        
        self.info = stockTicket.info


        print("Status: completed")
        print("data saved as .datadays, .datayear, and .info")
        return


# RUNTIME
# script runtime
def main():
    d = scrap(stockHandle="TSLA", ndays=7)

if __name__ == "__main__":
    main()
