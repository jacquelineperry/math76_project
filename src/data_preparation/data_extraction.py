# file to download historical data for S&P 500 companies

import yfinance as yf
from yahooquery import Ticker
import pandas as pd
import time

# getting list of S&P 500 companies
df = pd.read_csv('companies.csv')
ticker_list = list(df['Symbol'])
all_symbols = " ".join(ticker_list)

# hist_data is temp variable for holding the historical data in eac
hist_data = {}
data = pd.DataFrame()

start = time.time()

# get historical data for each ticker in the list of S&P 500 companies
for ticker in ticker_list:
    tick = Ticker(ticker)
    hist = tick.history(start='2018-01-01', end='2022-12-31', interval='1wk')
    ticker = str(ticker)
    hist_data[ticker] = hist
    temp = [data, hist]
    data = pd.concat(temp)

end = time.time()

print(hist_data)
print(end-start)
print(len(hist_data))
print(data)

# uncomment this part to save CSV

# data.to_csv(r'historical_data.csv')