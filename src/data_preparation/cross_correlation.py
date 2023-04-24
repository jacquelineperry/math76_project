import pandas as pd
import numpy as np

def ccf_values(series1, series2):
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

def compute_cadjacency_matrix(hist_data):
    """
    Computes the adjacency matrix for stock price cross-correlations.
    
    Args:
        hist_data (pd.DataFrame): The historical stock price data for each company.
        
    Returns:
        adj_matrix (np.ndarray): The adjacency matrix containing cross-correlation values
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
            
            ccf = ccf_values(series1, series2)

            if ~(i == j):
                adj_matrix[i][j] += ccf[0]

        print('j: ', j)

    return adj_matrix
