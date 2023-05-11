#%%
import networkx as nx
from src.stocks_network.correlation import Correlation
import yfinance as yf
from yahooquery import Ticker
import pandas as pd

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
        self.adj_matrix = None

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

        self.adj_matrix = adj_matrix
        self.G = nx.from_numpy_matrix(adj_matrix)
 
        labels_mapping = dict(zip(list(range(0, len(self.company_list))), self.company_list))
        self.G = nx.relabel_nodes(self.G, labels_mapping)

        attribute_dict = {}

        tickers = Ticker(self.company_list, asynchronous=True)

        datasi = tickers.get_modules("summaryProfile quoteType")
        dfsi = pd.DataFrame.from_dict(datasi).T
        dataframes = [pd.json_normalize([x for x in dfsi[module] if isinstance(x, dict)]) for
        module in ['summaryProfile', 'quoteType']]

        dfsi = pd.concat(dataframes, axis=1)

        dfsi = dfsi.set_index('symbol')
        dfsi = dfsi.loc[self.company_list]
  
        # 1. setting up data files
        self.industry_list =  list(dfsi['industry'])
        self.sector_list   =  list(dfsi['sector'])

        # print('node 0: ', self.G.nodes[0])

        for i in range(0, len(self.company_list)):
            # print(company_list[i])
            # tick = yf.Ticker(comp)
            comp = self.company_list[i]
            attribute_dict[comp] = self.sector_list[i]
            # self.G.nodes[i]['sector'] = self.industry_list[i]

        nx.set_node_attributes(self.G, attribute_dict, "sector")
    
        return self.G
    
    def create_fisher_network(self, corr_type):
        corr= Correlation(self.historical_data) # 3.1  create correlation instance
        corr_matrix = corr.get_fisher_matrix(corr_type) # 3.2 calculate correlation matrix

        self.adj_matrix = corr_matrix
        # self.G = nx.from_numpy_matrix(adj_matrix)
 
        # labels_mapping = dict(zip(list(range(0, len(self.company_list))), self.company_list))
        # self.G = nx.relabel_nodes(self.G, labels_mapping)
        self.G = nx.Graph()

        attribute_dict = {}

        tickers = Ticker(self.company_list, asynchronous=True)

        datasi = tickers.get_modules("summaryProfile quoteType")
        dfsi = pd.DataFrame.from_dict(datasi).T
        dataframes = [pd.json_normalize([x for x in dfsi[module] if isinstance(x, dict)]) for
        module in ['summaryProfile', 'quoteType']]

        dfsi = pd.concat(dataframes, axis=1)

        dfsi = dfsi.set_index('symbol')
        dfsi = dfsi.loc[self.company_list]
  
        # 1. setting up data files
        self.industry_list =  list(dfsi['industry'])
        self.sector_list   =  list(dfsi['sector'])

        # print('node 0: ', self.G.nodes[0])

        for j in range(len(self.company_list)-1, -1, -1):
            for i in range(0, j+1):
                comp1 = self.company_list[i]
                comp2 = self.company_list[j]

                self.G.add_edge(comp1, comp2, weight=self.adj_matrix[i][j])

        for i in range(0, len(self.company_list)):
            # print(company_list[i])
            # tick = yf.Ticker(comp)
            comp = self.company_list[i]
            attribute_dict[comp] = self.sector_list[i]
            # self.G.nodes[i]['sector'] = self.industry_list[i]

        nx.set_node_attributes(self.G, attribute_dict, "sector")
    
        return self.G