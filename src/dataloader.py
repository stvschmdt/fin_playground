# functions for reading in data from store
# minimal parameterized cleansing, verification
# output to parameterized dataframes (filters, slices)
# output dataframes in dictionary format (asset : payload)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import alpha_vantage.techindicators as ti
import alpha_vantage.cryptocurrencies as cc
import collections
import csv
import os
import time
from datetime import datetime

def build_dicts(ticker_lst, feature_lst, timeframe, start_date, end_date):
    path = 'storage/' + timeframe
    dictionary = {'tickers' : {}, 'features' : {}}
    for ticker in ticker_lst:
        path1 = path + '/tickers/' + ticker
        data = pd.read_csv(path1)
        data = data.set_index('date')
        if start_date in data.index:
            data = data.loc[end_date:start_date]
            old_shape = data.shape
            new_df = data.dropna()
            if new_df.shape == old_shape:
                dictionary['tickers'][ticker] = new_df
    for feature in feature_lst:
        path2 = path + '/features/' + feature
        data = pd.read_csv(path2)
        data = data.set_index('date')
        data = data.loc[end_date:start_date]
        data = data.dropna('columns')
        dictionary['features'][feature] = data
    print(dictionary['tickers'].keys())
    print(dictionary['features'].keys())

# write functionality to check if the date entered for start or end date was a weekend

if __name__ == "__main__":
    build_dicts(["AAPL", "MMM", "ZION", "ZTS", "XRX", "TSLA"], ['SMA', 'EMA', 'WMA', 'MACD', 'STOCH', 'RSI', 'MOM', 'ROC', 'MFI', 'BBANDS', 'MIDPRICE'], "daily", "2004-11-05", "2020-12-12")
