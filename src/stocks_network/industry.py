import pandas as pd
import numpy as np

class Industry():
    def __init__(self, company_list):
        # 1. setting up data files
        self.company_list =  company_list
        #self.company_list = list(historical_data.columns)[1:]
        #self.corr_threshold = corr_threshold