import pandas as pd
import numpy as np
from src.data_preparation.cross_correlation import compute_cadjacency_matrix
from src.data_preparation.pearson_correlation import compute_padjacency_matrix


if __name__ == '__main__':

    # 1. load the historical data into pd data frame
    hist_data = pd.read_csv('data/historical_data.csv')

    # 2. compute the adjacency matrix using cross-correlation
    cadj_matrix = compute_cadjacency_matrix(hist_data)

    # 3. compute the adjacency matrix using pearson correlation
    padj_matrix = compute_padjacency_matrix(hist_data)

