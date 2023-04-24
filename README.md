# Multilayer Network Graph for Stock Price Analysis

This project aims to build a multilayer network graph from scratch to analyze stock price movements of `S&P 500` companies using various factors like `location`, `industry`, `market cap`, `news sentiment`, `trading volume`, and `social media sentiment`.

## Directory Structure

The project is organized into the following directories and files:

```python 
project_directory/
│
├── data/ # Data files directory
│   ├── historical_data.csv # Historical stock data
│   ├── companies.csv # S&P 500 companies information
│   └── ...
│
├── src/ # Source code directory
│   ├── data_preparation/ # Data preparation module
│   │   ├── __init__.py  # Package initialization
│   │   └── data_preparation.py # Data preparation functions
│   │
│   ├── network_construction/
│   │   ├── __init__.py
│   │   └── network_construction.py
│   │
│   ├── network_analysis/
│   │   ├── __init__.py
│   │   └── network_analysis.py
│   │
│   └── visualization/
│       ├── __init__.py
│       └── visualization.py
│
└── main.py
```


### data/

This directory contains data files like historical stock data and information about S&P 500 companies. You can add more data files here as needed.

### src/

This directory contains the source code organized into separate subdirectories for each module.

#### src/data_preparation/

This module contains functions for preparing and processing the data, including downloading historical stock data, calculating correlations, and extracting features like location, industry, and market cap.

#### src/network_construction/

This module contains functions for building the network graph, including creating single-layer and multilayer graphs, and adding nodes and edges based on different attributes.

#### src/network_analysis/

This module contains functions for analyzing the network graph, including calculating network properties like clustering coefficients, path lengths, and modularity, as well as functions for estimating optimal thresholds.

#### src/visualization/

This module contains functions for visualizing the network graph and its properties, including plotting the network, displaying node and edge attributes, and creating visualizations of network properties for different thresholds.

### main.py

This is the main script that coordinates the entire process of building and analyzing the network graph. It imports the necessary functions from the modules and uses them to execute the different steps of the project.

## Usage

To run the project, execute the `main.py` script:

```bash
python main.py
```

This will start the process of data preparation, network construction, analysis, and visualization, outputting the results to the console and generating visualizations as specified in the code.

Make sure you have all the necessary dependencies installed before running the project. You can install them using pip:

```bash 
pip install -r requirements.txt
```

## Contributing

If you want to contribute to this project, please follow the directory structure and add your code to the appropriate module. Update this README if necessary to document any new additions or changes to the project structure.
