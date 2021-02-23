# ANALYZER
# group of functions to analyze stock data gathered from scraper.py

# IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# there is a scraper.py import in testing runtime (it's not required anywhere else)!


def simp_plot(data, info):
    # simple plot
    # creates classic stocks plot with volume

    fig, ax = plt.subplots(figsize=(15,8))

    ax.plot(data["Low"])
    ax.plot(data["High"])

    plt.show()
    return



# TESTING RUNTIME
def main():
    # import only for this function
    import scraper as sc
    stock = sc.scrap(stockHandle="TSLA", ndays=7)

    simp_plot(stock.data, stock.info)

    return

if __name__ == "__main__":
    main()