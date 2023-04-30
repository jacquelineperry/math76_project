#%%
import pandas as pd
import numpy as np

class Industry():
    def __init__(self, industry_sector_list):
        # 1. setting up data files
        self.industry_list =  list(industry_sector_list['industry'])
        self.sector_list   =  list(industry_sector_list['sector'])
        self.company_list  =  list(industry_sector_list['symbol'])

    def get_adj_matrixes(self):
        """
        Computes the adjacency matrixes for industry and sector.
        
        Args:

            
        Returns:
            
        """

        adj_matrix_sector = np.zeros((len(self.company_list), len(self.company_list))) # initialize to 2D array of zeroes
        adj_matrix_industry = np.zeros((len(self.company_list), len(self.company_list))) # initialize to 2D array of zeroes

        # Iterate over each pair of companies
        for j in range(len(self.company_list)-1, -1, -1):
            for i in range(0, j+1):
                comp1 = self.company_list[i]
                comp2 = self.company_list[j]
                
                if (comp1 != comp2):
                    if self.sector_list[i] == self.sector_list[j]:
                        adj_matrix_sector[i][j] += 1
                    if self.industry_list[i] == self.industry_list[j]:
                        adj_matrix_industry[i][j] += 1

        adj_matrix_sector = adj_matrix_sector + adj_matrix_sector.T - np.diag(np.diag(adj_matrix_sector))
        adj_matrix_industry = adj_matrix_industry + adj_matrix_industry.T - np.diag(np.diag(adj_matrix_industry))
        
        return adj_matrix_sector, adj_matrix_industry


#%%
industry_sector = pd.read_csv(r"C:\Users\coope\Documents\Math 76\math76_project\data\industry_sector.csv")
test1 = Industry(industry_sector)
#print(industry_sector)

print(test1.industry_list)
print(test1.sector_list)
# %%
print(industry_sector)
test1.get_adj_matrixes()[1]
# %%
