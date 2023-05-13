#%%
import numpy as np
import random
import matplotlib.pyplot as plt
from correlation import Correlation
import pandas as pd


def simulate_sir(adjacency_matrix, infected_node, recovery_rate, num_iterations):
    num_nodes = adjacency_matrix.shape[0]
    
    # Initialize the state of each node (S: Susceptible, I: Infected, R: Recovered)
    states = np.zeros(num_nodes, dtype=int)
    states[infected_node] = 1  # Set the initially infected node
    
    infected_count = [1]  # Track the number of infected nodes in each iteration
    
    for _ in range(num_iterations):
        new_states = states.copy()
        
        # Iterate over each node
        for node in range(num_nodes):
            if states[node] == 1:  # If the node is infected
                neighbors = np.nonzero(adjacency_matrix[node])[0]  # Find neighboring nodes
                print(neighbors)
                # Iterate over each neighboring node
                for neighbor in neighbors:
                    if states[neighbor] == 0:  # If the neighbor is susceptible
                        # Calculate the probability of transmission based on correlation
                        transmission_prob = adjacency_matrix[node][neighbor]
                        
                        # Check if transmission occurs
                        if random.random() < transmission_prob:
                            new_states[neighbor] = 1  # Set the neighbor as infected
        
                # Check if recovery occurs
                if random.random() < recovery_rate:
                    new_states[node] = 2  # Set the node as recovered
        
        # Update the states after each iteration
        states = new_states.copy()
        infected_count.append(np.count_nonzero(states == 1))
    
    return infected_count

#%%

# Example usage
adjacency_matrix = np.array([[0, 0.7, 0.5, 0, 0],
                             [0.7, 0, 0.3, 0, 0.9],
                             [0.5, 0.3, 0, 0.8, 0],
                             [0, 0, 0.8, 0, 0.4],
                             [0, 0.9, 0, 0.4, 0]])

infected_node = 0  # Choose the starting infected node
recovery_rate = 0.1
num_iterations = 20

infected_count = simulate_sir(adjacency_matrix, infected_node, recovery_rate, num_iterations)

# Plotting the number of infected nodes over iterations
plt.plot(range(num_iterations + 1), infected_count)
plt.xlabel('Iterations')
plt.ylabel('Number of Infected Nodes')
plt.title('Agent-based SIR Model Simulation')
plt.show()


#%%
hist_data_weekly = pd.read_csv(r'C:\Users\coope\Documents\Math 76\math76_project\data\historical_prices.csv')
corr = Correlation(hist_data_weekly)
matrix = corr.get_corr_matrix("pearsonr")
print(matrix)
# %%

infected_node = 0  # Choose the starting infected node
recovery_rate = 0.1
num_iterations = 20
infected_count = simulate_sir(matrix, infected_node, recovery_rate, num_iterations)

plt.plot(range(num_iterations + 1), infected_count)
plt.xlabel('Iterations')
plt.ylabel('Number of Infected Nodes')
plt.title('Agent-based SIR Model Simulation')
plt.show()
# %%
