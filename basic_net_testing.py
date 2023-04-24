import pandas as pd

from src.stocks_network.network_graph import NetworkGraph
#from src.stocks_network.correlation import Correlation


if __name__ == '__main__':

    # 1. load the historical data into pd data frame
    hist_data = pd.read_csv('data/historical_data.csv')
     
    # testt 1 -->create network graph instance
    basic_network_graph = NetworkGraph(hist_data)
    basic_network_graph.create_basic_network()
    print("basic_network_graph: \n", basic_network_graph)
    print("\n")

    # test 2 -->  create network graph instance with custom correlation threshold

    # test 3 -->  create network graph instance with p_value stat

    # test 4 -->  create network graph with edges of multiple attributes

    # test 5 -->  create network graph with edges of multiple attributes

    