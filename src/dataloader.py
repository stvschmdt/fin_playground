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
from datetime import timedelta

pd.options.mode.chained_assignment = None


abspath = os.path.abspath(os.getcwd())
finpath = Path(abspath).resolve().parent
parent_path = str(finpath) + '/'


#function takes a ticker and returns a dictionary with the data for that ticker
def build_ticker_dict(ticker, timeframe, start_date = '2004-09-30', end_date='2022-02-25', match_dates = True):
    if not check_dates(start_date, end_date, timeframe):
        return 0
    path = parent_path + 'storage/' + timeframe
    dictionary = {'daily' : pd.DataFrame(), 'fundamental': pd.DataFrame()}
    path1 = path + '/tickers/' + ticker
    data = pd.read_csv(path1)
    data = data.set_index('date')

    fundamental_income = pd.read_csv(parent_path + 'storage/fundamental_data/quarterly/income_statement/' + ticker)
    fundamental_balance_sheet = pd.read_csv(parent_path + 'storage/fundamental_data/quarterly/balance_sheet/' + ticker)
    fundamental_cash_flow = pd.read_csv(parent_path + 'storage/fundamental_data/quarterly/cash_flow/' + ticker)
    fundamental_company_overview = pd.read_csv(parent_path + 'storage/fundamental_data/company_overview/' + ticker)
    dictionary['fundamental'] = {"income statement" : fundamental_income, "balance sheet" : fundamental_balance_sheet,
                                 "cash flow" : fundamental_cash_flow, "company overview" : fundamental_company_overview}

    if not match_dates:
        new_df = data.dropna()
        dictionary['daily'] = new_df
        return dictionary
    if start_date in data.index:
        data = data.loc[end_date:start_date]
        old_shape = data.shape
        new_df = data.dropna()
        if new_df.shape == old_shape:
            dictionary['daily'] = new_df
            return dictionary
        else:
            print('contains NA within date range:', ticker)
            return ticker
    else:
        print('does not contain start date:', ticker)
        return ticker


def build_ticker_dicts(ticker_lst, timeframe, start_date = '2004-09-30', end_date='2022-02-25', match_dates = True):
    dictionary = {}
    bad_tickers = []
    for ticker in ticker_lst:
        data = build_ticker_dict(ticker, timeframe, start_date, end_date, match_dates)
        if data == ticker:
            bad_tickers.append(ticker)
            continue
        dictionary[ticker] = data
    print('bad tickers:', bad_tickers)
    return dictionary




#functions that get data for a certain technical indicator
def build_feature_df(feature, timeframe, ticker_lst=[], start_date='1999-12-17', end_date='2022-02-25', match_dates=True, all_cols=True):
    if not check_dates(start_date, end_date, timeframe):
        return 0
    path = parent_path + 'storage/' + timeframe
    path2 = path + '/features/' + feature
    data = pd.read_csv(path2)
    data = data.set_index('date')
    data = data.loc[end_date:start_date]
    
    if not all_cols:
        data = data[ticker_lst]

    if match_dates:
        data = data.dropna('columns')
    
    return data


def build_feature_dicts(features, timeframe, ticker_lst=[], start_date='1999-12-17', end_date='2022-02-25', match_dates=True, all_cols=True):
    dictionary = {}
    for feature in features:
        data = build_feature_df(feature, timeframe, ticker_lst, start_date, end_date, match_dates, all_cols)
        dictionary[feature] = data
    return dictionary



def build_crypto_df(coin, timeframe, start_date='2019-06-24', end_date='2022-03-19', match_dates=True):
    path = parent_path + 'storage/' + timeframe
    path3 = path + '/cryptocurrencies/' + coin

    data = pd.read_csv(path3)
    data = data.set_index('date')
    
    if not match_dates:
        return data

    if start_date in data.index:
        data = data.loc[end_date:start_date]
        old_shape = data.shape
        new_df = data.dropna()
        if new_df.shape == old_shape:
            return new_df
        else:
            print('contains NA within date range:', coin)
            return coin
    else:
        print('does not contain start date:', coin)
        return coin

def build_cryto_dict(coins, timeframe, start_date='2019-06-24', end_date='2022-03-19', match_dates=True):
    dictionary = {}
    bad_coins = []
    for coin in coins:
        data = build_crypto_df(coin, timeframe, start_date, end_date, match_dates)
        if data == coin:
            bad_coins.append(coin)
            continue
        dictionary[coin] = data
    print('bad coins:', bad_coins)
    return dictionary

#builds a rolling average of columns
# Note: we remove a number of columns from the dataframe equal to our rolling_interval value,
# because we have NaN values for these rolling_intervals as we do not have enough 
# previous observations to compute the rolling averages for these days   
def build_rolling_average(dictionary, feature, rolling_interval, timeframe='daily'):
    master_lst = list(dictionary.keys())
    new_col = str(rolling_interval) + " day rolling " + feature
    for item in master_lst:
        df = dictionary[item][timeframe]
        df = df[::-1]
        df[new_col] = df[feature].rolling(rolling_interval).mean()       
        df = df[::-1]
        df = df.dropna()
        dictionary[item][timeframe] = df
    return dictionary


#list of dates where we have market data for cryptocurrencies
def get_valid_crypto_dates():
    path = parent_path + 'storage/daily/cryptocurrenices/BTC'
    data = pd.read_csv(path)
    return data['date'].to_list()

def check_valid_crypto_dates(start_date, end_date, valid_dates):
    if start_date not in valid_dates:
        print('start date not valid')
        return 0
    if end_date not in valid_dates:
        print('end date not valid')
        return 0
    return 1


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

def build_sector_dict(ticker_dict):
    sector_dict = {}
    ticker_lst = list(ticker_dict.keys())
    for ticker in ticker_lst:
        sector = ticker_dict[ticker]['fundamental']['company overview']["Sector"][0]
        industry = ticker_dict[ticker]['fundamental']['company overview']["Industry"][0]
        if sector not in sector_dict.keys():
            sector_dict[sector] = {}
        if industry not in sector_dict[sector]:
            sector_dict[sector][industry] = [ticker]
        else:
            sector_dict[sector][industry].append(ticker)
    return sector_dict

#1. this can likely be easily generalized to accept arguments for cryptocurrencies as well
#2. function also assumes that the dimensions of your dataframes are all the same and do not have NaN values
#3. possible extension of this function could potentially normalize the shape of the selected ticker dataframes
#   before summing the values in the dataframe to build an index
def build_index(tickers, ticker_dict):
    df_lst = []
    for ticker in tickers:
        df_lst.append(ticker_dict[ticker]['daily'])
    index_df = sum(df_lst)
    index_df = index_df[["open", "high", "low", "close", "adj_close", "volume"]]
    return index_df

if __name__ == "__main__":
    print('main')
    ticker_dict = build_ticker_dicts(['AAPL', 'MMM', 'XRX', 'ZION'], 'daily')
    #build_rolling_average(ticker_dict, 'volume', 100)
    #build_sector_dict(ticker_dict)
    #build_index(['AAPL', 'MMM', 'XRX', 'ZION'], ticker_dict)
    print(ticker_dict['AAPL']['daily'])