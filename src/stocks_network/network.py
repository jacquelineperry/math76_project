import pandas as pd
import numpy as np

hist_data = pd.read_csv('../data/historical_data.csv')

comps_list = list(hist_data['symbol'].unique())
# saved comps_list to csv:
# pd.DataFrame(comps_list, columns=['symbol']).to_csv(r'company_list.csv')
#print(comps_list)

adj_matrix = np.zeros((len(comps_list), len(comps_list)))
# adj_matrix[0][1] += 1
# print(adj_matrix)


def ccf_values(series1, series2):
    p = series1
    q = series2
    p = (p - np.mean(p)) / (np.std(p) * len(p))
    q = (q - np.mean(q)) / (np.std(q))
    c = np.correlate(p, q, 'full')
    return c


for j in range(len(comps_list)):
    for i in range(len(comps_list)):
        comp1 = comps_list[i]
        comp2 = comps_list[j]
        series1 = hist_data.loc[hist_data['symbol'] == comp1]['close']
        series2 = hist_data.loc[hist_data['symbol'] == comp2]['close']
            
        ccf = ccf_values(series1, series2)

        if ~(i == j):
            adj_matrix[i][j] += ccf[0]

    print('j: ', j)

print(adj_matrix)



