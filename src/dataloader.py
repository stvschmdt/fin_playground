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


#this function allows you to select data from cold storage
def build_ticker_dicts(ticker_lst, timeframe, start_date, end_date):
    valid_dates = get_valid_dates(timeframe)
    if start_date not in valid_dates:
        print('start date not valid')
        return 0
    if end_date not in valid_dates:
        print('end dates not valid')
        return 0
    path = 'storage/' + timeframe
    dictionary = {'tickers' : {}}
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

def build_feature_dicts(feature_lst, timeframe, start_date, end_date):
    valid_dates = get_valid_dates(timeframe)
    dictionary = {'features' : {}}
    if start_date not in valid_dates:
        print('start date not valid')
        return 0
    if end_date not in valid_dates:
        print('end dates not valid')
        return 0
    path = 'storage/' + timeframe
    for feature in feature_lst:
        path2 = path + '/features/' + feature
        data = pd.read_csv(path2)
        data = data.set_index('date')
        data = data.loc[end_date:start_date]
        data = data.dropna('columns')
        dictionary['features'][feature] = data
    return dictionary

#function returns a list of valid dates
def get_valid_dates(timeframe):
    path = 'storage/' + timeframe + '/tickers/AAPL'
    data = pd.read_csv(path)
    return data['date'].to_list()


# write functionality to check if the date entered for start or end date was a weekend

if __name__ == "__main__":
    build_dicts(["AAPL", "MMM", "ZION", "ZTS", "XRX", "TSLA"], ['SMA', 'EMA', 'WMA', 'MACD', 'STOCH', 'RSI', 'MOM', 'ROC', 'MFI', 'BBANDS', 'MIDPRICE'], "daily", "2004-11-05", "2020-12-14")
