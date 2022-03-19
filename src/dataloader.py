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
from pathlib import Path
from datetime import datetime

abspath = os.path.abspath(os.getcwd())
finpath = Path(abspath).resolve().parent
parent_path = str(finpath) + '/'

#function takes a ticker and returns a dictionary with the data for that ticker
def build_ticker_dict(ticker, timeframe, start_date = '1999-12-17', end_date='2022-02-25', match_dates = True):
    if not check_dates(start_date, end_date, timeframe):
        return 0
    path = parent_path + 'storage/' + timeframe
    dictionary = {'daily' : pd.DataFrame(), 'fundamental': pd.DataFrame()}
    path1 = path + '/tickers/' + ticker
    data = pd.read_csv(path1)
    data = data.set_index('date')
    if not match_dates:
        new_df = data.dropna()
        dictionary['daily'] = new_df
    if start_date in data.index:
        data = data.loc[end_date:start_date]
        old_shape = data.shape
        new_df = data.dropna()
        if new_df.shape == old_shape:
            dictionary['daily'] = new_df
        else:
            print('contains NA within date range:', ticker)
            return ticker
    else:
        print('does not contain start date:', ticker)
        return ticker

    fundamentals = pd.read_csv(parent_path + 'storage/fundamental_data/quarterly/income_statement/' + ticker)
    dictionary['fundamental'] = fundamentals

    return dictionary

def build_ticker_dicts(ticker_lst, timeframe, start_date = '1999-12-17', end_date='2022-02-25', match_dates = True):
    dictionary = {}
    for ticker in ticker_lst:
        dictionary['ticker'] = build_ticker_dict(ticker, timeframe, start_date, end_date, match_dates)
    return dictionary



def build_feature_dicts(feature_lst, timeframe, start_date, end_date):
    valid_dates = get_valid_dates(timeframe)
    dictionary = {'features' : {}}
    if start_date not in valid_dates:
        print('start date not valid')
        return 0
    if end_date not in valid_dates:
        print('end dates not valid')
        return 0
    path = parent_path + 'storage/' + timeframe
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
    path = parent_path + 'storage/daily/tickers/AAPL'
    data = pd.read_csv(path)
    return data['date'].to_list()

def check_dates(start_date, end_date, timeframe):
    valid_dates = get_valid_dates(timeframe)
    if start_date not in valid_dates:
        print('start date not valid')
        return 0
    if end_date not in valid_dates:
        print('end dates not valid')
        return 0
    return 1


# write functionality to check if the date entered for start or end date was a weekend

if __name__ == "__main__":
    #build_dicts(["AAPL", "MMM", "ZION", "ZTS", "XRX", "TSLA"], ['SMA', 'EMA', 'WMA', 'MACD', 'STOCH', 'RSI', 'MOM', 'ROC', 'MFI', 'BBANDS', 'MIDPRICE'], "daily", "2004-11-05", "2020-12-14")
    print('main')
    print(parent_path)
    print(build_ticker_dict('AAPL', 'daily'))