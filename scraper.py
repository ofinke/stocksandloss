#      _____                                      
#     / ___/______________ _____  ____  ___  _____
#     \__ \/ ___/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
#    ___/ / /__/ /  / /_/ / /_/ / /_/ /  __/ /    
#   /____/\___/_/   \__,_/ .___/ .___/\___/_/     
#                       /_/   /_/                 
#
# ================================================
#
# Program to scrap useful data about stocks from the web

# IMPORTS
import pandas as pd
import datetime as dt

from twitterscraper import query_tweets

class scrap():

    def __init__(self, stockHandle, ndays):
        print("      _____                                      ")
        print("     / ___/______________ _____  ____  ___  _____")
        print("     \__ \/ ___/ ___/ __ `/ __ \/ __ \/ _ \/ ___/")
        print("    ___/ / /__/ /  / /_/ / /_/ / /_/ /  __/ /    ")
        print("   /____/\___/_/   \__,_/ .___/ .___/\___/_/     ")
        print("                       /_/   /_/                 ")
        print("\nVersion 0.1")
        print("\nScraping for stock(s): " + stockHandle)

        self.scraptwitter(stockHandle, ndays)

    def scraptwitter(self, stockHandle, ndays):
        
        print("Twitter scraper currently dead")
        
        # query


# RUNTIME
# script runtime
def main():

    d = scrap(stockHandle="TSLA", ndays=0)

if __name__ == "__main__":
	main()
