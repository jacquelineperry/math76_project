import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

hist_data = pd.read_csv('data/historical_data.csv')

comps_list = list(hist_data.columns)[1:]
# saved comps_list to csv:
# pd.DataFrame(comps_list, columns=['symbol']).to_csv(r'company_list.csv')
print(comps_list)

adj_matrix = np.zeros((len(comps_list), len(comps_list)))

corr_df = hist_data.corr(method='pearson')


for j in range(len(comps_list)-1, -1, -1):
    for i in range(0, j+1):
        comp1 = comps_list[i]
        comp2 = comps_list[j]

        if ~(i == j) and corr_df.at[comp1, comp2] >= 0.6:
            adj_matrix[i][j] += 1


adj_matrix = adj_matrix + adj_matrix.T - np.diag(np.diag(adj_matrix))

# np.savetxt('data/adj_matrix.csv', adj_matrix)
print('adjacency matrix: ', adj_matrix)

G = nx.from_numpy_matrix(adj_matrix)
# pos = nx.spring_layout(G, seed=42)  # Use a spring layout for node positions
# plt.figure(figsize=(12, 12))  # Set the size of the figure
# nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=10, font_weight='bold', width=0.5)
# plt.title("Stock Price Correlation Network")
# plt.show()


