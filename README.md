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
│   └── ... #etc
│
├── src/ # Source code directory
│   ├── stocks_network/ 
│   │   ├── __init__.py  # Package initialization
│   │   └── correlation.py # Data preparation functions
│   │   └── network_graph.py # Data preparation functions
│  
│
└── main.py
└── basic_net_testing.py
└── corr_testing.py
```


### data/

This directory contains data files like historical stock data and information about S&P 500 companies. You can add more data files here as needed.

### src/

This directory contains the source code organized into separate subdirectories for each module.

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
