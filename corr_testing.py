import pandas as pd
import numpy as np

from src.stocks_network.correlation import Correlation


if __name__ == '__main__':

    # 1. load the historical data into pd data frame
    hist_data = pd.read_csv('data/historical_data.csv')
     

    # test 1 -->  pearson correlation
    pearson = Correlation(hist_data)
    pearson_adj_matrix = pearson.pearson_adjacency_matrix()
    print("pearson_adj_matrix: \n", pearson_adj_matrix)
    print("\n")

    # test 2 -->  crosscorrelation no p_value
    basic_cross = Correlation(hist_data)
    pivoted_cross_adj_matrix = basic_cross.pivoted_cross_adjacency_matrix()
    print("pivoted_cross_adj_matrix: \n", pivoted_cross_adj_matrix)
    print("\n")
    
    '''
    # TODO: has bugs
    # test 3 -->  crosscorrelation with p_value
    cross = Correlation(hist_data)
    cross_adj_matrix,p_matrix = cross.cross_adjacency_and_p_matrices()
    print("cross_adj_matrix: ", cross_adj_matrix)
    print("\n")
    print("p_matrix: ", p_matrix)
     print("\n")

    # test 4 -->  spearman correlation
    spearman = Correlation(hist_data)
    spearman_adj_matrix = spearman.spearman_adjacency_matrix()
    print("spearman_adj_matrix: ", spearman_adj_matrix)
    print("\n")

    # test 5 -->  kendall correlation
    kendall = Correlation(hist_data)
    kendall_adj_matrix = kendall.kendall_adjacency_matrix()
    print("kendall_adj_matrix: ", kendall_adj_matrix)
    print("\n")
    '''
