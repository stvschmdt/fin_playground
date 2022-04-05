#uses 1 row of data to predict next adjusted close
#uses data from all available tickers

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from datetime import datetime

from dataloader import *



#need to get data from all tickers next to each other in one df
#    #need to add in shifted adjusted close
#    #dictionary with required tickers is available
#    #need function that iterates through tickers and appends onto df
#    #need function
#train test split
#fit and predict


ticker_lst = ['AAPL', 'MMM']

ticker_dict = build_ticker_dicts(ticker_lst, 'daily')
#print(ticker_dict)

def get_appended_df(dictionary, ticker_to_predict):
    df = dictionary[ticker_to_predict]['daily']
    print(df)
    df['next_close'] = df['close'].shift(1)
    tickers = list(dictionary.keys())
    print(tickers)
    tickers.remove(ticker_to_predict)
    print(tickers)
    for ticker in tickers:
        new_data = dictionary[ticker]['daily']
        df = pd.merge(df, new_data, on='date', how='outer')
        print(df) 
        print(df.columns)   
    return df.dropna(axis=0)

print(get_appended_df(ticker_dict, 'AAPL'))
