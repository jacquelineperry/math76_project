import pandas as pd
import numpy as np
from scipy.stats import pearsonr

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
    def __init__(self, historical_data):
        
        # 1. setting up data files
        self.historical_data =  historical_data
        self.company_list = list(self.historical_data['symbol'].unique())


    def ccf_values(self, series1, series2):
        """
        Computes the cross-correlation of two time series.
        
        Args:
            series1 (pd.Series): The first time series.
            series2 (pd.Series): The second time series.
            
        Returns:
            c (np.ndarray): The cross-correlation of the input time series.
        """
        
        p = series1
        q = series2

        p = (p - np.mean(p)) / (np.std(p, ddof=1) * len(p))
        q = (q - np.mean(q)) / (np.std(q, ddof=1))
        c = np.correlate(p, q, 'valid')

        return c
        
  
    def pivoted_cross_adjacency_matrix(self):
        """
        Computes the adjacency matrix for stock price cross-correlations.
        
        Args:
            self.historical_data (pd.DataFrame): The historical stock price data for each company.
            
        Returns:
            self.pivoted_cross_adj_matrix(np.ndarray): The adjacency matrix containing cross-correlation values
            for each pair of companies.
        """

        # Precompute a dictionary mapping company symbols to their closing stock price series --> pivoting here
        series_dict = {comp: self.historical_data.loc[self.historical_data['symbol'] == comp]['close'] for comp in self.company_list}
        pivoted_cross_adj_matrix = np.zeros((len(self.company_list), len(self.company_list))) # initialize to 2D array of zeroes

        # Iterate over each pair of companies
        for i in range(len(self.company_list)):
            for j in range(len(self.company_list)):
                if i == j:
                    # Set the diagonal to 1, as the correlation of a series with itself is 1
                    pivoted_cross_adj_matrix[i][j] = 1
                else:
                    series1 = series_dict[self.company_list[i]]
                    series2 = series_dict[self.company_list[j]]
                    ccf = self.ccf_values(series1, series2)
                    pivoted_cross_adj_matrix[i][j] = ccf[0]

        return pivoted_cross_adj_matrix

        
    def cross_adjacency_and_p_matrices(self): ## TODO: has some bags
        """
        Computes the adjacency matrix for stock price correlations and the corresponding p-value matrix.
        
        Args:
            self.historical_data (pd.DataFrame): The historical stock price data for each company.
            
        Returns:
            adj_matrix (np.ndarray): The adjacency matrix containing correlation values for each pair of companies.
            p_matrix (np.ndarray): The p-value matrix containing the p-values associated with each correlation value.
        """
        adj_matrix = np.zeros((len(self.company_list), len(self.company_list)))
        p_matrix = np.zeros((len(self.company_list), len(self.company_list)))

        # Precompute a dictionary mapping company symbols to their closing stock price series
        series_dict = {comp: self.historical_data.loc[self.historical_data['symbol'] == comp]['close'] for comp in self.company_list}

        for j in range(len(self.company_list)):
            for i in range(len(self.company_list)):
                comp1 = self.company_list[i]
                comp2 = self.company_list[j]
                series1 = np.nan_to_num(series_dict[comp1])
                series2 = np.nan_to_num(series_dict[comp2])
                
                correlation, p_value = pearsonr(series1, series2)

                if ~(i == j):
                    adj_matrix[i][j] += correlation
                    p_matrix[i][j] += p_value

        return adj_matrix, p_matrix


    #------------- pearsaon correlation ------------------------

    def pearson_corr_values(self,series1, series2):
        """
        Computes the Pearson correlation between two time series.

        Args:
            series1 (pd.Series): The first time series.
            series2 (pd.Series): The second time series.

        Returns:
            corr (float): The Pearson correlation between the input time series.
        """
        corr, _ = pearsonr(series1, series2)
        return corr
    


    def pearson_adjacency_matrix(self):
        """
        Computes the adjacency matrix for stock price correlations using Pearson correlation.

        Args:
            self.historical_data (pd.DataFrame): The historical stock price data for each company.

        Returns:
            adj_matrix (np.ndarray): The adjacency matrix containing Pearson correlation values
                                    for each pair of companies.
        """
        # Pivot the self.historical_data DataFrame to align the time series data for each company
        aligned_data = self.historical_data.pivot(index='date', columns='symbol', values='close')
        comps_list = aligned_data.columns

        pearson_adj_matrix = np.zeros((len(comps_list), len(comps_list)))

        # Precompute a dictionary mapping company symbols to their aligned closing stock price series
        series_dict = {comp: aligned_data[comp] for comp in comps_list}

        for j in range(len(comps_list)):
            for i in range(len(comps_list)):
                comp1 = comps_list[i]
                comp2 = comps_list[j]
                series1 = series_dict[comp1]
                series2 = series_dict[comp2]

                # Drop rows with NaN values in either series1 or series2
                aligned_series1, aligned_series2 = series1.align(series2, join='inner')
                aligned_series1 = aligned_series1.dropna()
                aligned_series2 = aligned_series2.dropna()

                # Align the two series again after removing NaN values
                aligned_series1, aligned_series2 = aligned_series1.align(aligned_series2, join='inner')

                corr = self.pearson_corr_values(aligned_series1, aligned_series2)

                if ~(i == j):
                    pearson_adj_matrix[i][j] += corr

            #print('j: ', j)
        return pearson_adj_matrix


    # ----------- multilayer correlations -----------------
    # TODO: here

