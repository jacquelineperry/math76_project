import pandas as pd
import numpy as np

hist_data = pd.read_csv('data/historical_data.csv')

comps_list = list(hist_data['symbol'].unique())
# saved comps_list to csv:
# pd.DataFrame(comps_list, columns=['symbol']).to_csv(r'company_list.csv')
print(comps_list)

adj_matrix = np.zeros((len(comps_list), len(comps_list)))
# adj_matrix[0][1] += 1
print(adj_matrix)

print(len(hist_data.loc[hist_data['symbol'] == 'CARR']['close']))
print(len(hist_data.loc[hist_data['symbol'] == 'ZTS']['close']))
print(hist_data.loc[hist_data['symbol'] == 'ZTS'])

def ccf_values(series1, series2):
    p = series1
    q = series2
    p = (p - np.mean(p)) / (np.std(p) * len(p))
    q = (q - np.mean(q)) / (np.std(q))
    c = np.correlate(p, q, 'full')
    return c


for j in range(len(comps_list)-1, -1, -1):
    for i in range(0, j+1):
        comp1 = comps_list[i]
        comp2 = comps_list[j]
        series1 = hist_data.loc[hist_data['symbol'] == comp1]['close']
        series2 = hist_data.loc[hist_data['symbol'] == comp2]['close']
            
        # ccf = ccf_values(series1, series2)
        # ccf = np.corrcoef(series1,series2)
        # print(ccf[0][1])
        # ccf = series1.corr(series2)
        try:
            cor = np.cov(series1, series2) / (np.std(series1)*np.std(series2))
        except:
            print(comp1)
            print(comp2)

        print(cor[0][1])

        if ~(i == j) and abs(cor[0][1]) >= 0.6:
            adj_matrix[i][j] += 1

    print('j: ', j)

print('before reflection: ', adj_matrix)
adj_matrix = adj_matrix + adj_matrix.T - np.diag(np.diag(adj_matrix))

np.savetxt('data/adj_matrix.csv', adj_matrix)
print('after reflection: ', adj_matrix)



