import pandas as pd
import numpy as np

# low modularity means community detection is def bad. BUT high modularity does not necessarily mean it is good

hist_data = pd.read_csv('historical_data.csv')
companies_info = pd.read_csv('companies.csv')
companies_list = list(companies_info['Symbol'])
print(hist_data)

adj_matrix = np.zeros((len(companies_list), len(companies_list)))
# adj_matrix[0][1] += 1
# print(adj_matrix)


def ccf_values(series1, series2):
    p = series1
    q = series2
    p = (p - np.mean(p)) / (np.std(p) * len(p))
    q = (q - np.mean(q)) / (np.std(q))
    c = np.correlate(p, q, 'full')
    return c


for j in range(len(companies_list)):
    for i in range(len(companies_list)):
        comp1 = companies_list[i]
        comp2 = companies_list[j]
        series1 = hist_data.loc[hist_data['symbol'] == comp1]['close']
        series2 = hist_data.loc[hist_data['symbol'] == comp2]['close']
        ccf = ccf_values(series1, series2)
        # print(ccf)

        if ~(i == j):
            adj_matrix[i][j] += ccf[0]

print(adj_matrix)



