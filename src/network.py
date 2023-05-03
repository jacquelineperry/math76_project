# This file mainly serves as a way for me to test stuff
# I have moved most of what is below into other files

#%%
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import community.community_louvain as louvain

#%%
hist_data_weekly = pd.read_csv('../data/historical_prices.csv')
hist_data_daily = pd.read_csv('../data/historical_prices_daily.csv')
comps_list = list(hist_data_weekly.columns)[1:]

# saved comps_list to csv:
# pd.DataFrame(comps_list, columns=['symbol']).to_csv(r'company_list.csv')

# corr_df = hist_data.corr(method='pearson')

#%%
data_2018_q1 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-01-01", "2018-03-31", inclusive="both")]
data_2018_q2 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-04-01", "2018-06-30", inclusive="both")]
data_2018_q3 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-07-01", "2018-09-30", inclusive="both")]
data_2018_q4 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-10-01", "2018-12-31", inclusive="both")]

#%%
def get_adj_matrix(hist_data, comps_list): 
    adj_matrix = np.zeros((len(comps_list), len(comps_list)))

    for j in range(len(comps_list)-1, -1, -1):
        for i in range(0, j+1):
            comp1 = comps_list[i]
            comp2 = comps_list[j]

            if (comp1 != comp2):
                prices = hist_data[[comp1, comp2]].copy()
                prices.dropna(inplace=True)
                if prices.empty:
                    continue
                
                corr, p_val = pearsonr(prices[comp1], prices[comp2])

                if abs(corr) >= 0.8 and p_val <= 0.05:
                    adj_matrix[i][j] += 1

    adj_matrix = adj_matrix + adj_matrix.T - np.diag(np.diag(adj_matrix))

    # np.savetxt('data/adj_matrix.csv', adj_matrix)
    print('adjacency matrix: ', adj_matrix)

    print('Number of edges: ', np.sum(adj_matrix)/2)
    print('Average degree: ', np.sum(adj_matrix)/len(adj_matrix))

    # G = nx.from_numpy_matrix(adj_matrix)

    return adj_matrix

#%%

matrices_2018 = {}
matrices_2018['q1'] = get_adj_matrix(data_2018_q1, comps_list)
matrices_2018['q2'] = get_adj_matrix(data_2018_q2, comps_list)
matrices_2018['q3'] = get_adj_matrix(data_2018_q3, comps_list)
matrices_2018['q4'] = get_adj_matrix(data_2018_q4, comps_list)

print(matrices_2018)

#%%
G = nx.from_numpy_matrix(matrices_2018['q1'])
print(list(G.nodes))
labels_mapping = dict(zip(list(range(0, len(comps_list))), comps_list))
G = nx.relabel_nodes(G, labels_mapping)
print(list(G.nodes))
print(G)

#%%
partition = louvain.best_partition(G)
print('louvain partition: \n', partition)
print(np.unique(np.array(partition.values())))
print('average degree connectivity: ', nx.average_degree_connectivity(G))

plt.figure(num=None, figsize=(15, 15), dpi=80)
plt.axis('off')
pos = nx.spring_layout(G, seed=42)

nx.draw_networkx_nodes(G,pos, node_size=5)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos)
plt.show()


# nx.draw_networkx_edges(G, pos, alpha=0.4)
# nx.draw_networkx_nodes(
#     G,
#     pos,
#     nodelist=list(p.keys()),
#     node_size=80,
#     node_color=list(p.values()),
#     cmap=plt.cm.Reds_r,
# )

# nx.draw(G)
