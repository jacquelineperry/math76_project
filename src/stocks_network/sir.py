#%%
# importing necessary libraries
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from network_graph import NetworkGraph
import pandas as pd
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
import matplotlib.pyplot as plt
from ndlib.viz.bokeh.MultiPlot import MultiPlot
import numpy as np

#%%
# Network topology
hist_data_weekly = pd.read_csv(r'C:\Users\coope\Documents\Math 76\math76_project\data\historical_prices.csv')
graph = NetworkGraph(hist_data_weekly)

#%%
# importing daily data for quarterly example
hist_data_daily = pd.read_csv(r'C:\Users\coope\Documents\Math 76\math76_project\data\historical_prices_daily.csv')

data_2018_q1 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-01-01", "2018-03-31", inclusive="both")]
data_2018_q2 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-04-01", "2018-06-30", inclusive="both")]
data_2018_q3 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-07-01", "2018-09-30", inclusive="both")]
data_2018_q4 = hist_data_daily.loc[hist_data_daily["Date"].between("2018-10-01", "2018-12-31", inclusive="both")]

# creating a graph for each quarter in 2018
graph1 = NetworkGraph(data_2018_q1).create_basic_network("pearsonr")
graph2 = NetworkGraph(data_2018_q2).create_basic_network("pearsonr")
graph3 = NetworkGraph(data_2018_q3).create_basic_network("pearsonr")
graph4 = NetworkGraph(data_2018_q4).create_basic_network("pearsonr")

graphs_2018 = [graph1, graph2, graph3, graph4]

#%%
# creating graph, runtime is high here so in isolated cell
g = graph.create_basic_network("pearsonr")

#%%
""" 
This runs SIR analysis and outputs diffusion trend and prevalence plots
"""
# Model selection
model = ep.SIRModel(g)

# Model Configuration
cfg = mc.Configuration()
# setting infection probability
cfg.add_model_parameter('beta', 0.01)
# setting removal probability
cfg.add_model_parameter('gamma', 0.005)
# setting inital infection. Can either selection fraction or specific nodes

# fraction- uncomment first line if not setting specific intially infected nodes
cfg.add_model_parameter("fraction_infected", 0.05)
#cfg.add_model_parameter("fraction_infected", 0.0)

# specific nodes
#cfg.add_model_initial_configuration("Infected",['A'])

model.set_initial_status(cfg)

# Simulation execution
iterations = model.iteration_bunch(100)
trends = model.build_trends(iterations)

# visualize the simulaton
viz = DiffusionTrend(model, trends)
p = viz.plot(width=400, height=400)
viz2 = DiffusionPrevalence(model, trends)
p2 = viz2.plot(width=400, height=400)

vm = MultiPlot()
vm.add_plot(p)
vm.add_plot(p2)
m = vm.plot()
show(m)

# %%
""" 
This cell outputs a string with the nodes infected after each iteration in the SIR analysis
"""
# Create lists to store the infected and recovered nodes after each iteration
infected_nodes_list = []
recovered_nodes_list = []
node_counts = []

# Iterate over the iterations
for iteration in iterations:
    # Get the status of each node in the iteration
    status = iteration['status']
    
    # Filter the infected and recovered nodes
    infected_nodes = [node for node, node_status in status.items() if node_status == 1]
    recovered_nodes = [node for node, node_status in status.items() if node_status == 2]
    
    # Add the infected and recovered nodes to their respective lists
    infected_nodes_list.append(infected_nodes)
    recovered_nodes_list.append(recovered_nodes)

    # Count the number of infected nodes
    node_counts.append(len(infected_nodes))

# Print the list of infected and recovered nodes after each iteration
for i in range(len(iterations)):
    print(f"Iteration {i + 1}: Infected nodes: {infected_nodes_list[i]}, Recovered nodes: {recovered_nodes_list[i]}")

#%%
""" 
This cell runs multiple SIR for different beta values and then outputs the result in a figure
"""
# Define a range of beta values
beta_values = [0.001, 0.01, 0.1]
gamma = 0.005
initial_fraction_infected = 0.05

# Initialize the SIR model for each beta value
models = []
for beta in beta_values:
    model = ep.SIRModel(g)
    config = mc.Configuration()
    config.add_model_parameter('beta', beta)
    config.add_model_parameter('gamma', gamma)
    cfg.add_model_parameter("fraction_infected", initial_fraction_infected)
    model.set_initial_status(config)
    models.append(model)

# Run the SIR model for each beta value
iterations = 30
results = []
for model in models:
    result = model.iteration_bunch(iterations)
    infected_counts = [len([node for node, status in iteration['status'].items() if status == 1]) for iteration in result]
    results.append(infected_counts)

# Plot the infected curve for each beta value
plt.figure(figsize=(8, 6))
colors = plt.cm.Blues(np.linspace(0.3, 1, len(beta_values)))
for i in range(len(beta_values)):
    plt.plot(range(iterations), results[i], label=f'beta={beta_values[i]}', linewidth=2, color=colors[i])


plt.xlabel('Time Step')
plt.ylabel('Number of Infected Nodes')
plt.title(f'Infected Curve for Different Beta Values\nGamma={gamma}, Initial Infected Fraction={initial_fraction_infected}')
plt.legend()
plt.legend()
plt.show()

# %%
""" 
This cell runs multiple SIR for different gamma values and then outputs the result in a figure
"""
# Define a range of gamma values
beta = 0.01
gamma_values = [0.005, 0.05, 0.5]
initial_fraction_infected = 0.05

# Initialize the SIR model for each beta value
models = []
for gamma in gamma_values:
    model = ep.SIRModel(g)
    config = mc.Configuration()
    config.add_model_parameter('beta', beta)
    config.add_model_parameter('gamma', gamma)
    cfg.add_model_parameter("fraction_infected", initial_fraction_infected)
    model.set_initial_status(config)
    models.append(model)

# Run the SIR model for each gamma value
iterations = 30
results = []
for model in models:
    result = model.iteration_bunch(iterations)
    infected_counts = [len([node for node, status in iteration['status'].items() if status == 1]) for iteration in result]
    results.append(infected_counts)

# Plot the infected curve for each gamma value
plt.figure(figsize=(8, 6))
colors = plt.cm.Blues(np.linspace(0.3, 1, len(gamma_values)))
for i in range(len(gamma_values)):
    plt.plot(range(iterations), results[i], label=f'gamma={gamma_values[i]}', linewidth=2, color=colors[i])


plt.xlabel('Time Step')
plt.ylabel('Number of Infected Nodes')
plt.title(f'Infected Curve for Different Gamma Values\nBeta={beta}, Initial Infected Fraction={initial_fraction_infected}')
plt.legend()
plt.legend()
plt.show()

# %%
""" 
This cell computes SIR with Amazon as initially infected node for the 4 quarters in 2018
It outputs a figure with all four infected curves graphed
"""

results = []
iterations = 40
for graph in graphs_2018:
    
    # Model selection
    model = ep.SIRModel(graph)

    # Model Configuration
    cfg = mc.Configuration()
    # setting infection probability
    cfg.add_model_parameter('beta', 0.01)
    # setting removal probability
    cfg.add_model_parameter('gamma', 0.005)
    # setting inital infection. Can either selection fraction or specific nodes

    # fraction- uncomment first line if not setting specific intially infected nodes
    #cfg.add_model_parameter("fraction_infected", 0.05)
    #cfg.add_model_parameter("fraction_infected", 0.0)

    # specific nodes
    cfg.add_model_initial_configuration("Infected",['AMZN'])

    model.set_initial_status(cfg)

    # Simulation execution
    result = model.iteration_bunch(iterations)
    trends = model.build_trends(result)

    infected_counts = [len([node for node, status in iteration['status'].items() if status == 1]) for iteration in result]
    results.append(infected_counts)

# Plot the results
labels = ["2018 Q1", "2018 Q2", "2018 Q3", "2018 Q4"]
plt.figure(figsize=(8, 6))
colors = plt.cm.Blues(np.linspace(0.3, 1, len(graphs_2018)))
                      
for i in range(len(graphs_2018)):
    plt.plot(range(iterations), results[i], label=labels[i], linewidth=2, color=colors[i])

plt.xlabel('Time Step')
plt.ylabel('Number of Infected Nodes')
plt.title(f'Infected Curve for AMZN Using Different Quarters in 2018 \nBeta=0.01, Gamma=0.005')
plt.legend()
plt.legend()
plt.show()
