import pandas as pd
import networkx as nx
import numpy as np
#import community as community_louvain
from src.stocks_network.cross_correlation import n_compute_cadjacency_matrix

# 1. Load historical stock price data
hist_data = pd.read_csv('historical_data.csv')

# 2. Load companies.csv file into a pandas DataFrame:
companies_df = pd.read_csv('companies.csv')

# 3. Load other data sources (location, industry, market cap, etc.)

# 4. Extract the Symbol and Headquarters Location columns to create locations.csv:
locations_df = companies_df[['Symbol', 'Headquarters Location']].copy()
locations_df.columns = ['Symbol', 'Location']
locations_df.to_csv('locations.csv', index=False)

# 5. Extract the Symbol and GICS Sector columns to create industries.csv:
industries_df = companies_df[['Symbol', 'GICS Sector']].copy()
industries_df.columns = ['Symbol', 'Industry']
industries_df.to_csv('industries.csv', index=False)

location_data = pd.read_csv('locations.csv')
industry_data = pd.read_csv('industries.csv')

# 6. Preprocess data and calculate correlations between stock price movements
correlation_matrix = n_compute_cadjacency_matrix(hist_data)

# 7. Create a basic network graph
G = nx.Graph()

# 8. Extract the unique company symbols from the historical data
company_list = hist_data['symbol'].unique()

# 9. Add nodes to the graph
G.add_nodes_from(company_list)


# 10. Set a correlation threshold to determine which pairs of stocks have significant correlations
correlation_threshold = 0.8

# 11. Iterate through the correlation matrix and add edges for pairs with correlations above the threshold
for i in range(correlation_matrix.shape[0]):
    for j in range(i + 1, correlation_matrix.shape[1]):
        if abs(correlation_matrix.iloc[i, j]) > correlation_threshold:
            G.add_edge(correlation_matrix.index[i], correlation_matrix.index[j], weight=correlation_matrix.iloc[i, j])



# ***************************************
# VISUALIZE 
# ***************************************

import matplotlib.pyplot as plt

# Visualize the graph
pos = nx.spring_layout(G, seed=42)  # Use a spring layout for node positions
plt.figure(figsize=(12, 12))  # Set the size of the figure
nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=10, font_weight='bold', width=0.5)
plt.title("Stock Price Correlation Network")
plt.show()




# Add attributes to the nodes
locations = dict(zip(location_data['Symbol'], location_data['Location']))
nx.set_node_attributes(G, locations, 'location')

industries = dict(zip(industry_data['Symbol'], industry_data['Industry']))
nx.set_node_attributes(G, industries, 'industry')

# Add other attributes (news sentiment, trading volume, social media sentiment)
# (This part will require gathering and preprocessing the relevant data)



'''
# ------------ community detection ------------------------


# Detect communities in the graph using the Louvain algorithm
partition = community_louvain.best_partition(G)

# Add community membership as an attribute to the nodes
nx.set_node_attributes(G, partition, 'community')

# Print the size of each community
community_sizes = pd.Series(partition).value_counts()
print('Community sizes:')
print(community_sizes)

# Print the nodes in each community
for community_id, nodes in nx.connected_components(G):
    print(f'Community {community_id}:')
    print(nodes)
'''