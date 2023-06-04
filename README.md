# math76_project

## data:
- contains list of S&P 500 companies with some info about each company, downloaded from Wikipedia
- also contains historical data of S&P 500 companies on a weekly and daily basis from beginning of 2018 through end of 2022.

## data_extraction.py
- use to get historical data as CSV

## partition.py
- creates network from weekly historical data and partitions using leiden algorithm
- also creates quarterly networks

## src/stocks_network
### correlation.py:
- calculates various matrices based on correlation types and ways of valuing stock
### network_graph.py
- creates actual network instances

## company_list.csv
- simply a list of all the companies
## company_list_aft2018.csv
- list of companies founded before 2018