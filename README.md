# math76_project

## data:
- contains list of S&P 500 companies with some info about each company, downloaded from Wikipedia
- also contains historical data of S&P 500 companies on a weekly and daily basis from beginning of 2018 through end of 2022.

## data_extraction.py
- use to get historical data as CSV

## partition.py
- creates network from weekly historical data and partitions using leiden algorithm
- also creates quarterly networks

## src/stocks_network
### correlation.py:
- calculates various matrices based on correlation types and ways of valuing stock
### network_graph.py
- creates actual network instances
### sir.py
- all SIR analysis in this file
- contains multiple cells that compute SIR for different example use cases

## company_list.csv
- simply a list of all the companies
## company_list_aft2018.csv
- list of companies founded before 2018

## Quarters_Adj_Matrices/
- contains the adjusted matrices for each quarter. These are CSV files that represent the binary correlation matrix of stock different quarters.

## Heatmaps/
- contents in the "Heatmaps" folder are:

  1. **Correlation Movie Window for 20 Quarters.gif**: This is an animated GIF file that cycles through heatmaps of the correlation matrices for each of the 20 quarters. Each heatmap visually represents the correlations between each pair of stocks in the S&P 500 index for that quarter. The color scale on the heatmap indicates the strength and direction of the correlation, with warm colors of thew rainbow colors representing strong positive correlation, and cooler ones like blue  representing strong negative correlation, and colors in between representing correlations closer to zero.

  2. **Correlation Movie Windowe for 20 Quarters.pptx**: This is a PowerPoint presentation that also contains the same sequence of correlation heatmaps as the animated GIF. Each slide in the presentation represents a different quarter, and the heatmap on that slide shows the correlations between each pair of stocks for that quarter.

  3. **Partial Correlations Heatmap for Q20.png**: This is a PNG image file of the heatmap for the partial correlations of the stocks in the S&P 500 index for the 20th quarter. Unlike the regular correlation, which measures the degree of association between two variables, the partial correlation measures the degree of association between two variables while controlling for the effect of one or more additional variables. In this case, the partial correlation heatmap shows how each pair of stocks is correlated when the effects of all other stocks are accounted for. 

## sp_network_graphs.ipynb
- visualizes and analyze the relationships between different stocks over different quarters.
-  Here's a high-level overview of what the code does:
    1. **Subgraphs and Disconnected Components**
    2. **Industry Classification**
    3. **Network Analysis**: The code computes various network measures for the graph such as degree centrality, closeness centrality, betweenness centrality, eigenvector centrality, and clustering coefficients. It also finds the central and peripheral nodes, and the shortest path between nodes.
    4. **Industry-Specific Network Analysis**: The graph is visualized again, this time with nodes colored according to their sector. The same is done for the disconnected components of the network.

## tickers_correlations.ipynb
- consists of a comprehensive network study of the S&P 500 stock market index. The primary goal is to examine the correlation structure among different stocks and understand their behavior over time.
  1. **Correlation Analysis:** For each quarter, a correlation matrix is computed, comparing the log returns of every pair of stocks. This analysis helps to understand the degree of relation between different stocks and how they move in relation to each other.

  3. **Network Construction:** For each quarter, an adjacency matrix is created based on a certain correlation threshold. In this network, each stock is a node, and an edge exists between two nodes if their correlation is above the threshold.

  4. **Edge Density and Correlation Coefficient Analysis:** A plot of edge density (the proportion of actual connections to potential connections) against correlation threshold is created, along with a distribution plot of correlation coefficients. This helps to understand how the network's density changes with the correlation threshold and to see the overall spread of correlation values.

  5. **Degree Distribution Analysis:** The degree distributions of stock correlations are plotted for different correlation thresholds. This analysis aids in identifying if the network follows a scale-free distribution, which is common in many natural and social networks.

  6. **Hierarchical Clustering:** Using the correlation matrices, hierarchical clustering is performed for each quarter to group together stocks that show similar trends over time. The output is visualized using a dendrogram. 
