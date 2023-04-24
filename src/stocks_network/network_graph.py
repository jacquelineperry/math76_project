import networkx as nx
from src.stocks_network.correlation import Correlation

# Description
# The NetworkGraph class creates a network graph of stock correlations using historical stock price data.
# It provides methods for creating a basic network graph,adding node attributes, and evaluating network properties, such as
# average clustering coefficient, average shortest path length, and modularity.

# default constants
DEFAULT_P_VALUE = 0.05 
DEFAULT_CORRELATION_THRESHOLD = 0.85 # threshold when not using p_value stat

class NetworkGraph():
    def __init__(self, historical_data, p_value=DEFAULT_P_VALUE, correlation_threshold=DEFAULT_CORRELATION_THRESHOLD):
        """Initializes the NetworkGraph object with historical stock price data, p_value threshold, and correlation threshold.
            Also creates a list of unique company symbols found in the data.
        """
  
        # 1. setting up data files
        self.historical_data =  self.historical_data = historical_data
        self.company_list = list(self.historical_data['symbol'].unique())

        # 2. variables
        self.p_value = p_value
        self.correlation_threshold = correlation_threshold

        # init basic graph
        self.G = None

        

    def create_basic_network(self):
        """
        Creates a basic network graph with nodes for each company and edges for each pair of companies with a correlation
        above the threshold.
        Inputs:
            self.historical_data (pd.DataFrame): The historical stock price data for each company.
            self.correlation_threshold (float): The threshold for the correlation between two companies.
        Returns:
            G (nx.Graph): The network graph.
        """

        # 1. Create a basic network graph
        self.G = nx.Graph()

        #2. Add nodes to the graph
        self.G.add_nodes_from(self.company_list)

        # 3. calculate correlations between stock price movements using correlation method of choice
        corr= Correlation(self.historical_data) # 3.1  create correlation instance
        correlation_matrix = corr.pivoted_cross_adjacency_matrix() # 3.2 calculate correlation matrix
        print("Using correlationmatrix: \n", correlation_matrix)
            
        # 4. Iterate through the correlation matrix and add edges for pairs with correlations above the threshold
        # 11. Iterate through the correlation matrix and add edges for pairs with correlations above the threshold
        stocks =0
        edges = 0
        for i in range(correlation_matrix.shape[0]):
            for j in range(i + 1, correlation_matrix.shape[1]):
                if abs(correlation_matrix[i, j]) > self.correlation_threshold:
                    self.G.add_edge(self.company_list[i], self.company_list[j], weight=correlation_matrix[i, j])
                    edges+=1
            stocks+=1

        print("(Number of stocks, significant edgea: \n", (stocks,edges))
        return self.G





    def add_node_attributes(self, attributes_data):
        """
        Adds attributes to the nodes in the network graph.
        Inputs:
            attribute_data (pd.DataFrame): A DataFrame containing the company symbols and their corresponding attribute. E.g. companies.csv
        """
        # TODO: here
        pass




    def evaluate_network_properties(self):
        """
        Evaluates the properties of the network graph, including average clustering coefficient, average shortest
        path length, and modularity.

        Returns:
            avg_clustering_coeff (float): The average clustering coefficient of the network.
            avg_path_length (float): The average shortest path length of the network (None if the network is not connected).
            modularity (float): The modularity of the network (None if python-louvain package is not installed).
        """

        """The outputs of the function can provide some insight into the properties of the network,
            but it ultimately depends on what specific properties you are interested in and the context of your analysis.

            * Average clustering coefficient measures the degree to which nodes in the graph tend to cluster together.
            A high clustering coefficient indicates that the network has many tightly-knit clusters, while a low clustering
            coefficient indicates that the network is more spread out.
            * Average shortest path length measures the average number of steps it takes to travel from one node to another.
            A smaller average path length indicates that the network is more connected, while a larger average path length
            indicates that the network is more spread out.
            * Modularity measures the degree to which the network can be divided into communities or clusters. 
            A high modularity indicates that the network has distinct communities with few connections between them,
            while a low modularity indicates that the network is more interconnected.

            In general, a "good" graph will depends on the specific goals of user's analysis. For example, if user is interested 
            in identifying clusters of related companies, a high modularity value could indicate a good graph.
            Alternatively, if user is  interested in the overall connectedness of the network, a low average path length could
            indicate a good graph.
        """

        avg_clustering_coeff = nx.average_clustering(self.G)
        
        if nx.is_connected(self.G):
            avg_path_length = nx.average_shortest_path_length(self.G)
        else:
            avg_path_length = None  # or another value to represent disconnected graphs
        
        try:
            import community as community_louvain  # you'll need to install python-louvain package
            partition = community_louvain.best_partition(self.G)
            modularity = community_louvain.modularity(partition,self. G)
        except ImportError:
            modularity = None
        
        return avg_clustering_coeff, avg_path_length, modularity

    
            