import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
from yahooquery import Ticker

# Description

# The Correlation class is designed to calculate and analyze the correlations between stock prices
#  of different companies based on their historical data. The class provides methods for calculating
#   cross-correlation, Pearson correlation, and their respective adjacency matrices.

# Pearson correlation is a measure of the linear relationship between two variables and ranges from -1
# (perfect negative correlation) to 1 (perfect positive correlation), with 0 indicating no correlation.
# It is useful when the data is normally distributed and the relationship between the variables is linear. 
# Pearson correlation is also computationally efficient and easier to interpret than cross-correlation.

# On the other hand, cross-correlation is a measure of the similarity between two time series as a function of
# the time lag applied to one of them. It can detect non-linear relationships and identify the lag between
# two time series that maximizes their similarity. However, cross-correlation is more computationally expensive
# and requires additional parameters such as the maximum lag to search.

# In the context of our stock price analysis, both measures will be used and compared to gain insights into the 
# relationships between companies.


class Correlation():
    def __init__(self, historical_data, corr_threshold=0.8, sector_weight=0.25):
        # 1. setting up data files
        self.historical_data =  historical_data
        self.company_list = list(historical_data.columns)[1:]
        self.corr_threshold = corr_threshold
        self.sector_weight = sector_weight

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


    
    def get_adj_matrix(self, corr_type):
        """
        Computes the adjacency matrix for stock price correlations.
        
        Args:
            self.historical_data (pd.DataFrame): The historical stock price data for each company.
            corr_type (string): type of correlation (pearsonr, spearmanr, kendalltau)
            
        Returns:
            adjacency matrix based on significant correlations with appropriate p-value
        """

        adj_matrix = np.zeros((len(self.company_list), len(self.company_list))) # initialize to 2D array of zeroes

        # Iterate over each pair of companies
        for j in range(len(self.company_list)-1, -1, -1):
            for i in range(0, j+1):
                comp1 = self.company_list[i]
                comp2 = self.company_list[j]
                
                if (comp1 != comp2):
                    prices = self.historical_data[[comp1, comp2]].copy()
                    prices.dropna(inplace=True)
                    if prices.empty:
                        continue
                    
                    corr, p_val = 0, 0
                    if corr_type=="pearsonr": 
                        corr, p_val = pearsonr(prices[comp1], prices[comp2])
                    if corr_type=="spearmanr":
                        corr, p_val = spearmanr(prices[comp1], prices[comp2])
                    if corr_type=="kendalltau":
                        corr, p_val = kendalltau(prices[comp1], prices[comp2])

                    if abs(corr) >= self.corr_threshold and p_val <= 0.05:
                        adj_matrix[i][j] += 1

        adj_matrix = adj_matrix + adj_matrix.T - np.diag(np.diag(adj_matrix))

        return adj_matrix
    
    def get_weighted_adj_matrix(self, corr_type):
        """
        Computes the adjacency matrix for stock price correlations + industry correlations.
        
        Args:
            self.historical_data (pd.DataFrame): The historical stock price data for each company.
            corr_type (string): type of correlation (pearsonr, spearmanr, kendalltau)
            
        Returns:
            adjacency matrix based on significant correlations with appropriate p-value
        """

        adj_matrix = np.zeros((len(self.company_list), len(self.company_list))) # initialize to 2D array of zeroes

        # Iterate over each pair of companies
        for j in range(len(self.company_list)-1, -1, -1):
            for i in range(0, j+1):
                comp1 = self.company_list[i]
                comp2 = self.company_list[j]
                
                if (comp1 != comp2):
                    prices = self.historical_data[[comp1, comp2]].copy()
                    prices.dropna(inplace=True)
                    if prices.empty:
                        continue
                    
                    corr, p_val = 0, 0
                    if corr_type=="pearsonr": 
                        corr, p_val = pearsonr(prices[comp1], prices[comp2])
                    if corr_type=="spearmanr":
                        corr, p_val = spearmanr(prices[comp1], prices[comp2])
                    if corr_type=="kendalltau":
                        corr, p_val = kendalltau(prices[comp1], prices[comp2])

                    if abs(corr) >= self.corr_threshold and p_val <= 0.05:
                        adj_matrix[i][j] += abs(corr)
                        
                        if self.sector_list[i] == self.sector_list[j]:
                            adj_matrix[i][j] += self.sector_weight

        adj_matrix = adj_matrix + adj_matrix.T - np.diag(np.diag(adj_matrix))

        return adj_matrix
    # ----------- multilayer correlations -----------------
    # TODO: here