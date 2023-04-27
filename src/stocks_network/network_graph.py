import networkx as nx
from src.stocks_network.correlation import Correlation

# Description
# ----------
# The NetworkGraph class creates a network graph of stock correlations using historical stock price data.
# It provides methods for creating a basic network graph,adding node attributes, and evaluating network properties, such as
# average clustering coefficient, average shortest path length, and modularity.



class NetworkGraph():
    def __init__(self, historical_data):
        """Initializes the NetworkGraph object with historical stock price data, 
            p_value threshold, and correlation threshold. Also creates a list 
            of unique company symbols found in the data.
        """
  
        # 1. setting up data files
        self.historical_data =  self.historical_data = historical_data
        self.company_list = list(historical_data.columns)[1:]

        # init basic graph
        self.G = None

    def create_basic_network(self, corr_type):
        """
        Creates a basic network graph with nodes for each company and edges for each pair of companies with a correlation
        above the threshold.
        Inputs:
            self.historical_data (pd.DataFrame): The historical stock price data for each company.
            self.correlation_threshold (float): The threshold for the correlation between two companies.
        Returns:
            G (nx.Graph): The network graph.
        """


        corr= Correlation(self.historical_data) # 3.1  create correlation instance
        adj_matrix = corr.get_adj_matrix(corr_type) # 3.2 calculate correlation matrix
        print("Adjacency matrix: \n", adj_matrix)

        self.G = nx.from_numpy_matrix(adj_matrix)

        labels_mapping = dict(zip(list(range(0, len(self.company_list))), self.company_list))
        self.G = nx.relabel_nodes(self.G, labels_mapping)
    
        return self.G