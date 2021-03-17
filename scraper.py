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

    def __init__(self, stockHandle):
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
        print("\nScraping for stock(s) " + stockHandle + " data.")


        self.scrapstockdata(stockHandle)
        # self.scraptwitter(stockHandle)
        
        print("\nScraping completed")

    def scraptwitter(self, stockHandle):
        
        print("\nScraping https://twitter.com/")
        print("Status: Failed (scraper not implemented)")
        
        # query

    def scrapstockdata(self, stockHandle):
        # use yfinance
        print("\nScraping https://finance.yahoo.com/")
        print("Status: started")

        stockTicket = yf.Ticker(stockHandle)

        # scrape relevant data
        print("Status: scraping last 3 weeks")
        self.data = stockTicket.history(start=(dt.date.today() - dt.timedelta(days=21)), end=dt.date.today(), interval="5m", actions=False)
        self.data.reset_index(inplace=True)

        self.info = stockTicket.info


        print("Status: completed")
        print("data saved as .dataweeks and .info")
        return


# RUNTIME
# script runtime
def main():
    d = scrap(stockHandle="TSLA")
    return

if __name__ == "__main__":
    main()
