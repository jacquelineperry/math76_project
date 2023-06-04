#%%
from src.stocks_network.network_graph import NetworkGraph
import pandas as pd
import networkx as nx
import yfinance as yf
import matplotlib.pyplot as plt
import sys
import numpy as np
import leidenalg as la
import igraph as ig
import cairo
import seaborn as sns

def get_la_partition(network, res_param):
    G = ig.Graph.from_networkx(network.G)
    partition = la.find_partition(G, la.CPMVertexPartition,
                                   resolution_parameter = res_param)
    clusters_sectors = {}
    part_list = list(partition)
    for i in range(0, len(part_list)):
        clusters_sectors[i] = []

        for j in part_list[i]:
            # node_name = comp_list[j]
            node = G.vs.find(j)
            sector = node.attributes()['sector']

            clusters_sectors[i].append(sector)

    return G, partition, clusters_sectors

#%%
if __name__ == '__main__':
    # read in csvs 
    all_comps = pd.read_csv('data/constituents.csv')
    hist_data_weekly = pd.read_csv('data/historical_prices.csv')
    hist_data_daily = pd.read_csv('data/historical_prices_daily.csv')
    comps = list(all_comps['Symbol'])
    adj_comps = list(hist_data_weekly.columns)[1:]
    new_comp_list = []

    ## filtering companies by market cap
    market_caps = []
    for i in range(0, len(comps)):
        comp = comps[i].replace(".", "-")
        tick = yf.Ticker(comp)
        market_cap = tick.info['marketCap']
        market_caps.append(market_cap)

    # market cap for whole S&P 500
    sp_market_cap = sum(market_caps)

    for i in range(0, len(adj_comps)):
        tick = yf.Ticker(adj_comps[i])
        market_cap = tick.info['marketCap']

        if (market_cap/sp_market_cap) > 0.0008:
            new_comp_list.append(adj_comps[i])

    print(new_comp_list)
    print(len(new_comp_list))

    filt_data_weekly = hist_data_weekly.loc[:, new_comp_list]

    #%%
    # can change to create network with different value types
    filt_network = NetworkGraph(filt_data_weekly)
    filt_network.create_basic_network(corr_type="pearsonr", val_type='returns')

    #%%
    # filter out nodes with degree >= 1
    filt_network.G.remove_nodes_from(node for node, degree in dict(filt_network.G.degree()).items() if degree < 2)    
    G = ig.Graph.from_networkx(filt_network.G)

    #%%
    # Leiden partition
    filt_partition = la.find_partition(G, la.CPMVertexPartition,
                                   resolution_parameter = .01)
    print(filt_partition.summary())
    G.vs['label'] = G.vs['_nx_name']
    print(list(G.vs()))
    ig.plot(filt_partition, layout='graphopt', vertex_label = G.vs['label'])

    print(filt_partition.summary())

    #%%
    # getting partition for each company to make attribute and save as .gexf if want to see in Gephi
    partitions = filt_partition.membership
    attribute_dict = {}
    comp_list = list(filt_network.G.nodes)
    for i in range(0, len(comp_list)):
        comp = comp_list[i]
        attribute_dict[comp] = partitions[i]

    nx.set_node_attributes(filt_network.G, attribute_dict, "leiden partition")

    nx.write_gexf(filt_network.G, 'leiden-part.gexf')

    #%%
    # seeing what sectors are in each cluster
    clusters = {}
    part_list = list(filt_partition)
    for i in range(0, len(part_list)):
        clusters[i] = []

        for j in part_list[i]:
            node = G.vs.find(j)
            sector = node.attributes()['sector']

            clusters[i].append(sector)

    print(clusters)

    for i in range(0, len(clusters)):
        print(np.unique(np.array(clusters[i])))

    #%%
    np.set_printoptions(threshold=sys.maxsize)
    print(filt_network.adj_matrix)
    #%%

    # Data splits into quarters 2018-2022

    data_2018_q1 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-01-01", "2018-03-31", inclusive="both")]
    data_2018_q2 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-04-01", "2018-06-30", inclusive="both")]
    data_2018_q3 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-07-01", "2018-09-30", inclusive="both")]
    data_2018_q4 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-10-01", "2018-12-31", inclusive="both")]

    data_2019_q1 = hist_data_daily.loc[hist_data_daily["Date"].between("2019-01-01", "2019-03-31", inclusive="both")]
    data_2019_q2 = hist_data_daily.loc[hist_data_daily["Date"].between("2019-04-01", "2019-06-30", inclusive="both")]
    data_2019_q3 = hist_data_daily.loc[hist_data_daily["Date"].between("2019-07-01", "2019-09-30", inclusive="both")]
    data_2019_q4 = hist_data_daily.loc[hist_data_daily["Date"].between("2019-10-01", "2019-12-31", inclusive="both")]

    data_2020_q1 = hist_data_daily.loc[hist_data_daily["Date"].between("2020-01-01", "2020-03-31", inclusive="both")]
    data_2020_q2 = hist_data_daily.loc[hist_data_daily["Date"].between("2020-04-01", "2020-06-30", inclusive="both")]
    data_2020_q3 = hist_data_daily.loc[hist_data_daily["Date"].between("2020-07-01", "2020-09-30", inclusive="both")]
    data_2020_q4 = hist_data_daily.loc[hist_data_daily["Date"].between("2020-10-01", "2020-12-31", inclusive="both")]

    data_2021_q1 = hist_data_daily.loc[hist_data_daily["Date"].between("2021-01-01", "2021-03-31", inclusive="both")]
    data_2021_q2 = hist_data_daily.loc[hist_data_daily["Date"].between("2021-04-01", "2021-06-30", inclusive="both")]
    data_2021_q3 = hist_data_daily.loc[hist_data_daily["Date"].between("2021-07-01", "2021-09-30", inclusive="both")]
    data_2021_q4 = hist_data_daily.loc[hist_data_daily["Date"].between("2021-10-01", "2021-12-31", inclusive="both")]

    data_2022_q1 = hist_data_daily.loc[hist_data_daily["Date"].between("2022-01-01", "2022-03-31", inclusive="both")]
    data_2022_q2 = hist_data_daily.loc[hist_data_daily["Date"].between("2022-04-01", "2022-06-30", inclusive="both")]
    data_2022_q3 = hist_data_daily.loc[hist_data_daily["Date"].between("2022-07-01", "2022-09-30", inclusive="both")]
    data_2022_q4 = hist_data_daily.loc[hist_data_daily["Date"].between("2022-10-01", "2022-12-31", inclusive="both")]
    #%%

    # create networks for each quarter. Note that this takes a while to run 

    net_2018_q1 = NetworkGraph(data_2018_q1)
    net_2018_q1.create_basic_network(corr_type="pearsonr")
    net_2018_q2 = NetworkGraph(data_2018_q2)
    net_2018_q2.create_basic_network(corr_type="pearsonr")
    net_2018_q3 = NetworkGraph(data_2018_q3)
    net_2018_q3.create_basic_network(corr_type="pearsonr")
    net_2018_q4 = NetworkGraph(data_2018_q4)
    net_2018_q4.create_basic_network(corr_type="pearsonr")

    net_2019_q1 = NetworkGraph(data_2019_q1)
    net_2019_q1.create_basic_network(corr_type="pearsonr")
    net_2019_q2 = NetworkGraph(data_2019_q2)
    net_2019_q2.create_basic_network(corr_type="pearsonr")
    net_2019_q3 = NetworkGraph(data_2019_q3)
    net_2019_q3.create_basic_network(corr_type="pearsonr")
    net_2019_q4 = NetworkGraph(data_2019_q4)
    net_2019_q4.create_basic_network(corr_type="pearsonr")

    net_2020_q1 = NetworkGraph(data_2020_q1)
    net_2020_q1.create_basic_network(corr_type="pearsonr")
    net_2020_q2 = NetworkGraph(data_2020_q2)
    net_2020_q2.create_basic_network(corr_type="pearsonr")
    net_2020_q3 = NetworkGraph(data_2020_q3)
    net_2020_q3.create_basic_network(corr_type="pearsonr")
    net_2020_q4 = NetworkGraph(data_2020_q4)
    net_2020_q4.create_basic_network(corr_type="pearsonr")

    net_2021_q1 = NetworkGraph(data_2021_q1)
    net_2021_q1.create_basic_network(corr_type="pearsonr")
    net_2021_q2 = NetworkGraph(data_2021_q2)
    net_2021_q2.create_basic_network(corr_type="pearsonr")
    net_2021_q3 = NetworkGraph(data_2021_q3)
    net_2021_q3.create_basic_network(corr_type="pearsonr")
    net_2021_q4 = NetworkGraph(data_2021_q4)
    net_2021_q4.create_basic_network(corr_type="pearsonr")

    net_2022_q1 = NetworkGraph(data_2022_q1)
    net_2022_q1.create_basic_network(corr_type="pearsonr")
    net_2022_q2 = NetworkGraph(data_2022_q2)
    net_2022_q2.create_basic_network(corr_type="pearsonr")
    net_2022_q3 = NetworkGraph(data_2022_q3)
    net_2022_q3.create_basic_network(corr_type="pearsonr")
    net_2022_q4 = NetworkGraph(data_2022_q4)
    net_2022_q4.create_basic_network(corr_type="pearsonr")
