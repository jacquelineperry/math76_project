import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
import math as m
import scipy
import time

# function for calculating volatility
def ewma(df, weight):
    vols = []
    vols.append(0)
    keys = []
    
    for i in range(1, len(df)):
        ret = (df[i] - df[i-1])/df[i-1]
        var = (weight*(vols[i-1]**2)) + ((1-weight)*(ret**2))
        vol = m.sqrt(var)
        vols.append(vol)
        keys.append(-(len(df)+1-i))
    
    return list(np.array(vols[1:])*m.sqrt(252)*100)


# Description

# The Correlation class is designed to calculate and analyze the correlations between stock prices
#  of different companies based on their historical data. The class provides methods for calculating
#  Pearson's r correlation, spearman's rho, and kendall's tau and their respective adjacency matrices.

# Pearson correlation is a measure of the linear relationship between two variables and ranges from -1
# (perfect negative correlation) to 1 (perfect positive correlation), with 0 indicating no correlation.
# It is useful when the data is normally distributed and the relationship between the variables is linear. 
# Pearson correlation is also computationally efficient and easier to interpret than cross-correlation.

# Correlations are computed for the upper triangle of the matrix and then reflected. Diagonal is set as 0,
# so there are not self-edges.


class Correlation():
    def __init__(self, historical_data, corr_threshold=0.8):
        # 1. setting up data files
        self.historical_data =  historical_data
        self.company_list = list(historical_data.columns)[1:]
        self.corr_threshold = corr_threshold

    def get_adj_matrix(self, corr_type):
        """
        Computes the adjacency matrix for close price correlations.
        
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

        adj_matrix = adj_matrix + adj_matrix.T - np.diag(np.diag(adj_matrix))

        return adj_matrix

    def get_ret_matrix(self, corr_type):
        """
        Computes the adjacency matrix for log-returns of close price correlations.
        
        Args:
            self.historical_data (pd.DataFrame): The historical stock price data for each company.
            corr_type (string): type of correlation (pearsonr, spearmanr, kendalltau)
            
        Returns:
            adjacency matrix based on significant correlations with appropriate p-value
        """
                
        returns = pd.DataFrame()
        for comp in self.company_list:
            prices = self.historical_data[comp].copy()

            if prices.empty:
                continue

            ret = []
            for i in range(1, len(prices)):
                ret.append(m.log(prices[i]/prices[i-1]))
            returns[comp] = ret

        corr_matrix = np.zeros((len(self.company_list), len(self.company_list))) # initialize to 2D array of zeroes

        # Iterate over each pair of companies
        for j in range(len(self.company_list)-1, -1, -1):
            for i in range(0, j+1):
                comp1 = self.company_list[i]
                comp2 = self.company_list[j]
                
                if (comp1 != comp2):
                    rets = returns[[comp1, comp2]].copy()
                    rets.dropna(inplace=True)
                    if rets.empty:
                        continue

                    corr, p_val = 0, 0
                    if corr_type=="pearsonr": 
                        corr, p_val = pearsonr(rets[comp1], rets[comp2])
                    if corr_type=="spearmanr":
                        corr, p_val = spearmanr(rets[comp1], rets[comp2])
                    if corr_type=="kendalltau":
                        corr, p_val = kendalltau(rets[comp1], rets[comp2])

                    if abs(corr) >= self.corr_threshold and p_val <= 0.05:
                        corr_matrix[i][j] += abs(corr)

        corr_matrix = corr_matrix + corr_matrix.T - np.diag(np.diag(corr_matrix))
        return corr_matrix
    
    def get_vol_matrix(self, corr_type):
        """
        Computes the adjacency matrix for volatility of close price correlations.
        
        Args:
            self.historical_data (pd.DataFrame): The historical stock price data for each company.
            corr_type (string): type of correlation (pearsonr, spearmanr, kendalltau)
            
        Returns:
            adjacency matrix based on significant correlations with appropriate p-value
        """

        volatility = pd.DataFrame()
        for comp in self.company_list:
            prices = self.historical_data[comp].copy()

            if prices.empty:
                continue

            volatility[comp] = ewma(list(prices), 0.8)

        corr_matrix = np.zeros((len(self.company_list), len(self.company_list))) # initialize to 2D array of zeroes

        # Iterate over each pair of companies
        for j in range(len(self.company_list)-1, -1, -1):
            for i in range(0, j+1):
                comp1 = self.company_list[i]
                comp2 = self.company_list[j]
                
                if (comp1 != comp2):
                    vols = volatility[[comp1, comp2]].copy()
                    vols.dropna(inplace=True)
                    if vols.empty:
                        continue

                    corr, p_val = 0, 0
                    if corr_type=="pearsonr": 
                        corr, p_val = pearsonr(vols[comp1], vols[comp2])
                    if corr_type=="spearmanr":
                        corr, p_val = spearmanr(vols[comp1], vols[comp2])
                    if corr_type=="kendalltau":
                        corr, p_val = kendalltau(vols[comp1], vols[comp2])

                    if abs(corr) >= self.corr_threshold and p_val <= 0.05:
                        corr_matrix[i][j] += abs(corr)

        corr_matrix = corr_matrix + corr_matrix.T - np.diag(np.diag(corr_matrix))
        return corr_matrix
