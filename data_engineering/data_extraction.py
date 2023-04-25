# file to download historical data for S&P 500 companies

import yfinance as yf
from yahooquery import Ticker
import pandas as pd
import time

# getting list of S&P 500 companies
df = pd.read_csv('../data/companies.csv')
comps_df = df.loc[df['Founded'].str.slice(0, 4).astype(int) <= 2018]
comps_df.reset_index(drop=True, inplace=True)
print(comps_df)
ticker_list = list(comps_df['Symbol'])
all_symbols = " ".join(ticker_list)

data = pd.DataFrame()

data = yf.download(ticker_list, start="2018-01-01", end="2022-12-31", interval="1wk")['Close']

# uncomment this part to save CSV

# data.to_csv(r'historical_prices.csv')