#%%
from industry import Industry
from network_graph import NetworkGraph
from correlation import Correlation
import pandas as pd



# #%%
# test_list = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC']
# test1 = Industry(test_list)

# print(test1.industry_list)
# print(test1.sector_list)
# # %%
# print('Adj Matrix Sector \n',test1.get_adj_matrices()[0])
# print('Adj Matrix Industry \n',test1.get_adj_matrices()[1])

# %%
hist_data_weekly = pd.read_csv(r'C:\Users\coope\Documents\Math 76\math76_project\data\historical_prices.csv')
test = NetworkGraph(hist_data_weekly)
graph0 = test.create_basic_network("pearsonr")
#graph = test.create_sector_network()
#graph2 = test.create_industry_network()

#test_list = test.company_list
#print(test_list)
#test_list.to_csv(r'test_list.csv')
#test.create_sector_network()
#print(test.G)
# %%
hist_data_weekly = pd.read_csv(r'C:\Users\coope\Documents\Math 76\math76_project\data\historical_prices.csv')
corr = Correlation(hist_data_weekly)
matrix = corr.get_adj_matrix
print(matrix)