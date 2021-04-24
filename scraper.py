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

def scraptwitter(stockHandle):
     
    print("\nScraping https://twitter.com/")
    print("Status: Failed (scraper not implemented)")
    
    # query

def scrapstockdata(stockHandle, d, i, ed):
    # d = days
    # i = interval
    # ed = end date
    # use yfinance
    print("\nScraping https://finance.yahoo.com/")
    print("Status: started")

    stockTicket = yf.Ticker(stockHandle)

    # scrape relevant data
    data = stockTicket.history(start=(ed - dt.timedelta(days=d)), end=ed, interval=i, actions=False)
    data.reset_index(inplace=True)

    info = stockTicket.info

    print("Status: completed")
    return (data, info)


# RUNTIME
# script runtime
def main():
    
    return

if __name__ == "__main__":
    main()
