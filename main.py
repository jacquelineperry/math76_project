#%%
from src.stocks_network.network_graph import NetworkGraph
from src.stocks_network.multilayer_graph import MultiLayerGraph
import pandas as pd
import networkx as nx
import yfinance as yf
import matplotlib.pyplot as plt
import sys
import numpy as np

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


#%%
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hist_data_weekly = pd.read_csv('data/historical_prices.csv')
    hist_data_daily = pd.read_csv('data/historical_prices_daily.csv')
    network = NetworkGraph(hist_data_weekly)
    # network.create_basic_network(corr_type="pearsonr")
    network.create_fisher_network(corr_type='pearsonr')

    # print(network.G.nodes.data())
    nx.write_gexf(network.G, 'weekly-data-3.gexf')


    #%%
    np.set_printoptions(threshold=sys.maxsize)
    print(network.adj_matrix)
    # nx.write_gexf(network.G, 'weekly-data-3.gexf')
    # pos = nx.spring_layout(network.G, 0.5)
    # nx.draw(network.G, pos)
    # plt.show()



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
    multilayer_network = MultiLayerGraph(20)

    # create layers for each quarter. Note that this takes a while to run 

    layer_2018_q1 = NetworkGraph(data_2018_q1)
    layer_2018_q1.create_basic_network(corr_type="pearsonr")

    # nx.write_gexf(layer_2018_q1.G, '2018-q1-graph.gexf')


    layer_2018_q2 = NetworkGraph(data_2018_q2)
    layer_2018_q2.create_basic_network(corr_type="pearsonr")
    layer_2018_q3 = NetworkGraph(data_2018_q3)
    layer_2018_q3.create_basic_network(corr_type="pearsonr")
    layer_2018_q4 = NetworkGraph(data_2018_q4)
    layer_2018_q4.create_basic_network(corr_type="pearsonr")

    layer_2019_q1 = NetworkGraph(data_2019_q1)
    layer_2019_q1.create_basic_network(corr_type="pearsonr")
    layer_2019_q2 = NetworkGraph(data_2019_q2)
    layer_2019_q2.create_basic_network(corr_type="pearsonr")
    layer_2019_q3 = NetworkGraph(data_2019_q3)
    layer_2019_q3.create_basic_network(corr_type="pearsonr")
    layer_2019_q4 = NetworkGraph(data_2019_q4)
    layer_2019_q4.create_basic_network(corr_type="pearsonr")

    layer_2020_q1 = NetworkGraph(data_2020_q1)
    layer_2020_q1.create_basic_network(corr_type="pearsonr")
    layer_2020_q2 = NetworkGraph(data_2020_q2)
    layer_2020_q2.create_basic_network(corr_type="pearsonr")
    layer_2020_q3 = NetworkGraph(data_2020_q3)
    layer_2020_q3.create_basic_network(corr_type="pearsonr")
    layer_2020_q4 = NetworkGraph(data_2020_q4)
    layer_2020_q4.create_basic_network(corr_type="pearsonr")

    layer_2021_q1 = NetworkGraph(data_2021_q1)
    layer_2021_q1.create_basic_network(corr_type="pearsonr")
    layer_2021_q2 = NetworkGraph(data_2021_q2)
    layer_2021_q2.create_basic_network(corr_type="pearsonr")
    layer_2021_q3 = NetworkGraph(data_2021_q3)
    layer_2021_q3.create_basic_network(corr_type="pearsonr")
    layer_2021_q4 = NetworkGraph(data_2021_q4)
    layer_2021_q4.create_basic_network(corr_type="pearsonr")

    layer_2022_q1 = NetworkGraph(data_2022_q1)
    layer_2022_q1.create_basic_network(corr_type="pearsonr")
    layer_2022_q2 = NetworkGraph(data_2022_q2)
    layer_2022_q2.create_basic_network(corr_type="pearsonr")
    layer_2022_q3 = NetworkGraph(data_2022_q3)
    layer_2022_q3.create_basic_network(corr_type="pearsonr")
    layer_2022_q4 = NetworkGraph(data_2022_q4)
    layer_2022_q4.create_basic_network(corr_type="pearsonr")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

    #%%
    # Temporal layers
    multilayer_network.add_layer('2018-q1', layer_2018_q1)
    multilayer_network.add_layer('2018-q2', layer_2018_q2)
    multilayer_network.add_layer('2018-q3', layer_2018_q3)
    multilayer_network.add_layer('2018-q4', layer_2018_q4)

    multilayer_network.add_layer('2019-q1', layer_2019_q1)
    multilayer_network.add_layer('2019-q2', layer_2019_q2)
    multilayer_network.add_layer('2019-q3', layer_2019_q3)
    multilayer_network.add_layer('2019-q4', layer_2019_q4)

    multilayer_network.add_layer('2020-q1', layer_2020_q1)
    multilayer_network.add_layer('2020-q2', layer_2020_q2)
    multilayer_network.add_layer('2020-q3', layer_2020_q3)
    multilayer_network.add_layer('2020-q4', layer_2020_q4)

    multilayer_network.add_layer('2021-q1', layer_2021_q1)
    multilayer_network.add_layer('2021-q2', layer_2021_q2)
    multilayer_network.add_layer('2021-q3', layer_2021_q3)
    multilayer_network.add_layer('2021-q4', layer_2021_q4)

    multilayer_network.add_layer('2022-q1', layer_2022_q1)
    multilayer_network.add_layer('2022-q2', layer_2022_q2)
    multilayer_network.add_layer('2022-q3', layer_2022_q3)
    multilayer_network.add_layer('2022-q4', layer_2022_q4)

    # %%
    print(nx.adjacency_matrix(multilayer_network.graph['2018-q1'].G))




# %%
