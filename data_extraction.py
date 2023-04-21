import yfinance as yf
from yahooquery import Ticker
import pandas as pd
import time

df = pd.read_csv('companies.csv')

print(Ticker('BRK.B').price)
ticker_list = list(df['Symbol'])
# ticker_list = ["A", "AL", "AAP", "AAPL", "ZBRA", "ZION", "ZTS"]
all_symbols = " ".join(ticker_list)
# myInfo = Ticker(all_symbols)
# myDict = myInfo.price
# print(myDict)
hist_data = {}
print(hist_data)
data = pd.DataFrame()

start = time.time()
for ticker in ticker_list:
    tick = Ticker(ticker)
    hist = tick.history(start='2018-01-01', end='2022-12-31', interval='1wk')
    ticker = str(ticker)
    # print(hist)
    hist_data[ticker] = hist
    temp = [data, hist]
    data = pd.concat(temp)
    # longName = myDict[ticker]['longName']
    # market_cap = myDict[ticker]['marketCap']
    # price = myDict[ticker]['regularMarketPrice']
    # print(ticker, longName, price)

end = time.time()
print(hist_data)
print(end-start)
print(len(hist_data))
print(data)

data.to_csv(r'historical_data.csv')
