import pandas as pd
import numpy as np
from scipy.stats import pearsonr

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

def pearson_corr_values(series1, series2):
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

def compute_padjacency_matrix(hist_data):
    """
    Computes the adjacency matrix for stock price correlations using Pearson correlation.

    Args:
        hist_data (pd.DataFrame): The historical stock price data for each company.

    Returns:
        adj_matrix (np.ndarray): The adjacency matrix containing Pearson correlation values
                                 for each pair of companies.
    """
    comps_list = list(hist_data['symbol'].unique())
    adj_matrix = np.zeros((len(comps_list), len(comps_list)))

    # Precompute a dictionary mapping company symbols to their closing stock price series
    series_dict = {comp: hist_data.loc[hist_data['symbol'] == comp]['close'] for comp in comps_list}

    for j in range(len(comps_list)):
        for i in range(len(comps_list)):
            comp1 = comps_list[i]
            comp2 = comps_list[j]
            series1 = series_dict[comp1]
            series2 = series_dict[comp2]

            corr = pearson_corr_values(series1, series2)

            if ~(i == j):
                adj_matrix[i][j] += corr

        print('j: ', j)

    return adj_matrix
