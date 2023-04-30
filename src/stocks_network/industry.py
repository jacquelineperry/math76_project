#%%
import pandas as pd
import numpy as np
from yahooquery import Ticker

class Industry():
    def __init__(self, company_list):
        self.company_list = self.company_list = company_list

        # below code looks up sector and industry from company list
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

    def get_adj_matrices(self,type):
        """
        Computes the adjacency matrixes for industry and sector.
        
        Args: industry_sector_list: panda data frame with symbol, industry, sector

            
        Returns: two adjancency matrices,[0] is sector and [1] is industry
            
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
        
        if type =="sector":
            return adj_matrix_sector
        if type =="industry":
            return adj_matrix_industry

