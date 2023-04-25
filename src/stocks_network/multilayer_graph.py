import networkx as nx
from community import community_louvain

# Description

# The MultiLayerGraph class is designed to represent and manipulate multilayer networks,
# also known as multiplex networks. These networks consist of multiple layers, each 
# containing a single-layer network (graph), with nodes potentially connected across
# different layers. The class provides functionalities to create and modify multilayer
# graphs, add nodes and edges (both intra-layer and inter-layer), and compute various
# network metrics such as degree sequence, total degree sequence, modularity, and density.

class MultiLayerGraph:
    def __init__(self, num_layers):
        """
        Initialize a new instance of the MultiLayerGraph class.

        :param num_layers: The number of layers in the multilayer graph.
        """
        self.num_layers = num_layers
        self.graph = {layer: {} for layer in range(num_layers)}


    def add_node(self, layer, node):
        """
        Add a node to the specified layer in the multilayer graph.

        :param layer: The layer to which the node should be added.
        :param node: The node to be added.
        """
        if layer in self.graph:
            self.graph[layer][node] = []
        else:
            raise ValueError(f"Invalid layer: {layer}")

    def add_edge(self, layer1, node1, layer2, node2):
        """
        Add an edge between two nodes in the multilayer graph.

        :param layer1: The layer of the first node.
        :param node1: The first node.
        :param layer2: The layer of the second node.
        :param node2: The second node.
        """
        if layer1 in self.graph and layer2 in self.graph:
            if node1 in self.graph[layer1] and node2 in self.graph[layer2]:
                self.graph[layer1][node1].append((layer2, node2))
                self.graph[layer2][node2].append((layer1, node1))
            else:
                raise ValueError(f"Invalid nodes: {node1} or {node2}")
        else:
            raise ValueError(f"Invalid layers: {layer1} or {layer2}")

    def add_single_layer_graph(self, layer, single_layer_graph):
        """
        Add a single-layer graph to the specified layer in the multilayer graph.

        :param layer: The layer to which the single-layer graph should be added.
        :param single_layer_graph: The single-layer graph (adjacency list) to be added.
        """
        for node, edges in single_layer_graph.items():
            self.add_node(layer, node)
            for connected_node in edges:
                self.add_edge(layer, node, layer, connected_node)

    def degree_sequence(self, layer):
        """
        Compute the degree sequence for the specified layer in the multilayer graph.

        :param layer: The layer for which to compute the degree sequence.
        :return: A list of node degrees sorted in descending order.
        """
        layer_graph = self._create_networkx_graph(layer)
        return sorted([d for n, d in layer_graph.degree()], reverse=True)

    def total_degree_sequence(self):
        """
        Compute the total degree sequence for the multilayer graph.

        :return: A list of node degrees sorted in descending order.
        """
        degree_seq = []
        for layer in range(self.num_layers):
            degree_seq += self.degree_sequence(layer)
        return sorted(degree_seq, reverse=True)

    def modularity(self):
        """
        Compute the modularity for each layer in the multilayer graph using the Louvain method.

        Note: This method calculates modularity only for single-layer graphs.

        :return: A list of modularity values for each layer.
        """
        modularity_layers = []
        for layer in range(self.num_layers):
            layer_graph = self._create_networkx_graph(layer)
            partition = community_louvain.best_partition(layer_graph)
            modularity_layers.append(community_louvain.modularity(partition, layer_graph))
        return modularity_layers
    
    def convert_to_multilayer(self, single_layer_graph, num_layers):
        """
        Convert a single-layer graph to a multilayer graph with the specified number of layers.
        The single-layer graph will be added to the first layer of the multilayer graph.

        :param single_layer_graph: The single-layer graph to be converted (adjacency list).
        :param num_layers: The number of layers in the multilayer graph.
        :return: A MultiLayerGraph instance containing the converted multilayer graph.
        """
        multilayer_graph = MultiLayerGraph(num_layers)
        multilayer_graph.add_single_layer_graph(0, single_layer_graph)
        return multilayer_graph

def display(self):
    """
    Display the multilayer graph's structure by printing nodes and their connected edges in each layer.
    """
    for layer, nodes in self.graph.items():
        print(f"Layer {layer}:")
        for node, edges in nodes.items():
            print(f"  Node {node}: {edges}")

