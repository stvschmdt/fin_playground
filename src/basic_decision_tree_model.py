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


ticker_lst = ['AAPL', 'MMM', 'ZION']

ticker_dict = build_ticker_dicts(ticker_lst, 'daily')
#print(ticker_dict)


def add_pct_changes(df):
    columns = df.columns
    for column in columns:
        column_name = column + '_pct_change'
        df[column_name] = df[column].pct_change()
    return df

def shift_columns(df, n=0):
    columns = df.columns
    for column in columns:
        for i in range(1, n+1):
           column_name = column + '_shift_' + str(i)
           df[column_name] = df[column].shift(-i)
    return df


def get_appended_df(dictionary, ticker_to_predict, add_pcts = True, shift = True, shift_n = 3):
    count = 1
    #df = dictionary[ticker_to_predict]['daily']
    #print(df.columns)
    #begin = df.index
    #df['pct_change'] = df['close'].pct_change(1)
    tickers = list(dictionary.keys())
    print(tickers)
    #tickers.remove(ticker_to_predict)
    for ticker in tickers:
        new_data = dictionary[ticker]['daily']
        if add_pcts:
            new_data = add_pct_changes(new_data)
        if shift:
            new_data = shift_columns(new_data, shift_n)
        if count == 1:
            begin = new_data
            print('ADDED', ticker)  
            print(begin)
            count += 1
            continue    
        begin = pd.merge(begin, new_data, on='date', how='outer')
        print('ADDED', ticker)  
        print(begin)
        count += 1
    return begin.dropna(axis=0)

print(get_appended_df(ticker_dict, 'AAPL'))
