# file to download historical data for S&P 500 companies
#%%
import yfinance as yf
from yahooquery import Ticker
import pandas as pd
import time

#%%
# getting list of S&P 500 companies
df = pd.read_csv('../data/companies.csv')
comps_df = df.loc[df['Founded'].str.slice(0, 4).astype(int) <= 2017]
comps_df.reset_index(drop=True, inplace=True)
print(comps_df)
ticker_list = list(comps_df['Symbol'])
all_symbols = " ".join(ticker_list)

data = pd.DataFrame()

data = yf.download(ticker_list, start="2018-01-01", end="2022-12-31")['Close']

data.dropna(axis=1, how='all', inplace=True)
# uncomment this part to save CSV

#data.to_csv(r'historical_prices_daily.csv')

# #%%
# sbux = yf.Ticker("SBUX")
# print(sbux.info['sector'])
# print(sbux.info)

# df = pd.read_csv('../company_list_aft2018.csv')
# yf.Ticker(str(df['symbol'][1])).info['sector']
# df['sector'] = df['symbol']
# #df['sector'] = yf.Ticker(str(df['symbol'])).info['sector']
# df
# %%

#symbols = ['TSHA', 'GRAMF', 'VFC', 'ABOS', 'INLX', 'INVO', 'IONM', 'IONQ']
symbols = df['symbol'].head(20)

tickers = Ticker(symbols, asynchronous=True)

datasi = tickers.get_modules("summaryProfile quoteType")
dfsi = pd.DataFrame.from_dict(datasi).T
dataframes = [pd.json_normalize([x for x in dfsi[module] if isinstance(x, dict)]) for
module in ['summaryProfile', 'quoteType']]

dfsi = pd.concat(dataframes, axis=1)

dfsi = dfsi.set_index('symbol')
dfsi = dfsi.loc[symbols]

print(dfsi[['industry', 'sector']])


# %%
dfsi[['industry', 'sector']].to_csv(r'industry_sector_test.csv')
# %%
