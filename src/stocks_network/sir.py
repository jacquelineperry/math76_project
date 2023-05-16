#%%
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from network_graph import NetworkGraph
import pandas as pd
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend

#%%
# Network topology
hist_data_weekly = pd.read_csv(r'C:\Users\coope\Documents\Math 76\math76_project\data\historical_prices.csv')
g = NetworkGraph(hist_data_weekly).create_basic_network("pearsonr")

#%%

# Model selection
model = ep.SIRModel(g)

# Model Configuration
cfg = mc.Configuration()
# setting infection probability
cfg.add_model_parameter('beta', 0.01)
# setting removal probability
cfg.add_model_parameter('gamma', 0.005)
cfg.add_model_parameter("fraction_infected", 0.05)
model.set_initial_status(cfg)

# Simulation execution
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)

# %%

# visualize the simulaton
viz = DiffusionTrend(model, trends)
p = viz.plot(width=400, height=400)
show(p)

