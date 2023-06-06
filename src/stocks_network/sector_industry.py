#%%

import pandas as pd
from yahooquery import Ticker
import matplotlib.pyplot as plt
import numpy as np

#%%

hist_data_weekly = pd.read_csv(r'C:\Users\coope\Documents\Math 76\math76_project\data\historical_prices.csv')
historical_data =  hist_data_weekly
company_list = list(historical_data.columns)[1:]


# below code looks up sector and industry from company list
tickers = Ticker(company_list, asynchronous=True)

datasi = tickers.get_modules("summaryProfile quoteType")
dfsi = pd.DataFrame.from_dict(datasi).T
dataframes = [pd.json_normalize([x for x in dfsi[module] if isinstance(x, dict)]) for
module in ['summaryProfile', 'quoteType']]

dfsi = pd.concat(dataframes, axis=1)

dfsi = dfsi.set_index('symbol')
dfsi = dfsi.loc[company_list]

# 1. setting up data files
industry_list =  list(dfsi['industry'])
sector_list   =  list(dfsi['sector'])
# %%
print(sector_list)
# %%
def plot_sector_distribution(sectors):
    sector_counts = {}
    for sector in sectors:
        if sector in sector_counts:
            sector_counts[sector] += 1
        else:
            sector_counts[sector] = 1
    
    labels = list(sector_counts.keys())[:-1]
    #labels2 = labels[:-1]
    counts = list(sector_counts.values())[:-1]
    
    print(labels)
    #print(labels2)
    print(counts)
    color = plt.cm.Blues(.9)
    plt.bar(labels, counts,color = color)
    #plt.xlabel('Sectors')
    plt.ylabel('Count')
    plt.title('Sector Distribution')
    plt.xticks(rotation=45)
    #plt.gca().set_xticklabels([])
    plt.show()

    plt.pie(counts)
    plt.show()
# %%
plot_sector_distribution(industry_list)
# %%
print(len(np.unique(industry_list)))
print(len(np.unique(sector_list)))

