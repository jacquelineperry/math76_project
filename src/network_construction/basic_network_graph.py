import pandas as pd
import networkx as nx
import numpy as np
import community as community_louvain

# 1. Load historical stock price data
hist_data = pd.read_csv('data/historical_data.csv')

# 2. Load companies.csv file into a pandas DataFrame:
companies_df = pd.read_csv('data/companies.csv')


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


# Preprocess data and calculate correlations between stock price movements
# (This part will require additional data processing and calculations)

# Create a basic network graph
G = nx.Graph()

# Add nodes to the graph
#comps_list = list(data/historical_data['symbol'].unique())
G.add_nodes_from('data/company_list')

# Add edges to the graph based on stock price correlations
# (This part will require additional calculations using the stock price data)

# Add attributes to the nodes
locations = dict(zip(location_data['Symbol'], location_data['Location']))
nx.set_node_attributes(G, locations, 'location')

industries = dict(zip(industry_data['Symbol'], industry_data['Industry']))
nx.set_node_attributes(G, industries, 'industry')


# Add other attributes (news sentiment, trading volume, social media sentiment)
# (This part will require gathering and preprocessing the relevant data)



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
