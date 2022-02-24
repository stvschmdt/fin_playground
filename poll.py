# functions responsible for the extraction of data
# from an API, with various save methods (getter only)

#test push

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

today = datetime.today().strftime('%Y-%m-%d')

API_key = '599NW2X84IZN5W1U'

#sp_names = pd.read_csv('constituents_csv.csv')
#sp_financials = pd.read_csv('constituents-financials_csv.csv')

ts = TimeSeries(key=API_key, output_format='pandas')
indicators = ti.TechIndicators(key=API_key, output_format='pandas')

def get_tickers():
    sp_names = pd.read_csv('constituents_csv.csv')
    ticker_symbols = [ sym for sym in sp_names.Symbol ]
    return ticker_symbols

def industry_dict():
    sp_financials = pd.read_csv('constituents-financials_csv.csv')
    sector_dict = {}
    for i,j in zip(sp_financials.Symbol, sp_financials.Sector):
        sector_dict[i] = j
    return sector_dict

class tech_indicators:
    def init(self):
        pass

#loop through tickers
#add basic price data to SP 500 folder
#go through each tech indicator and get a column for that ticker
#add the column to SP 500 folder and the csv for that feature
#separate function for each timeframe?

def build_csv(ticker_lst, timeframe='daily', cols = ['open', 'high', 'low', 'close', 'volume']):
    # do a check for which one to read in
    # add in some appropriate reasonable time stamp
    bad_tickers = []
    good_tickers = []
    ticker_lst = ["AAPL", "MMM", "ZION", "ZTS", "XRX"]
    tech_indicators_dict = tech_indicators_dict_initialize(['SMA'], timeframe)
    for ticker in ticker_lst:
        try:
            if timeframe == 'daily':
                print('here')
                data, _ = ts.get_daily(ticker, outputsize='full')
                length = data.shape[0]
                # call function to add tech indicators to data file
                sma, _ = indicators.get_sma(ticker, timeframe)
                
        
                data['SMA'] = correct_length(length, sma['SMA'].to_list())
                
                tech_indicators_dict['SMA'].append(sma['SMA'].to_list())
                #data_file_loc = "storage/daily/tickers/" + ticker # writes full ticker file to storage
                #data.to_csv(data_file_loc)
            elif timeframe == "weekly":
                data, _ = ts.get_weekly(ticker, outputsize='full')
                data_file_loc = "SP500_weekly_data/" + ticker
            elif timeframe == "monthly":
                data, _ = ts.get_monthly(ticker, outputsize='full')
                data_file_loc = "SP500_monthly_data/" + ticker
            good_tickers.append(ticker)
        except:
            bad_tickers.append(ticker)
        #need a function that names the columns in the technical indicators dataframes we've constructed
        time.sleep(1)
    sma_df = fit_tech_to_df(tech_indicators_dict["SMA"], good_tickers)
    print(sma_df)
    print(len(tech_indicators_dict["SMA"]))
    print(bad_tickers)

    # bad_tickers = ['AGN', 'APC', 'BBT', 'BF.B', 'COG', 'CBS', 'CXO', 'LB', 'MYL', 'RHT', 'COL', 'SCG', 'TMK', 'VAR', 'WLTW']
    # need to add date_time functionality to write a timestamp of when the function was run to a file

def tech_indicators_dict_initialize(features_lst, timeframe):
    tech_indicators_dict = {}
    time_index = date_getter(timeframe)
    for feature in features_lst:
        tech_indicators_dict[feature] = [time_index]
    return tech_indicators_dict

def fit_tech_to_df(tech_data_lst, cols):
    tech_data_df = pd.DataFrame(tech_data_lst).transpose()
    tech_data_df.columns = ['date'] + cols
    tech_data_df = tech_data_df.set_index('date')
    return tech_data_df


def correct_length(length, tech_data):
    if length > len(tech_data):
        print(length)
        print(len(tech_data))
        a = length - len(tech_data)
        empty_lst = [np.nan]*a
        print('empty list', empty_lst)
        tot_lst = tech_data + empty_lst
        print('tot lst')
        print(tot_lst)
        return tot_lst
    elif length < len(tech_data):
        ind_lst = tech_data["SMA"].to_list()[:length]
    else:
        ind_lst = tech_data["SMA"].to_list()
    return ind_lst


def date_getter(timeframe):
    print(timeframe)
    if timeframe == 'daily':
        data, _ = ts.get_daily(symbol='MMM', outputsize='full')
    elif timeframe == 'weekly':
        data, _ = ts.get_weekly(symbol='MMM')
    elif timeframe == 'monthly':
        data, _ = ts.get_monthly(symbol='MMM')
    else:
        print('not a valid time step')
        return
    return np.array(data.index)

#print(date_getter('daily'))
#print(tech_indicators_dict_initialize(['SMA'], 'daily'))


#want a function that takes a ticker and returns a column of data for a specific feature


# scratchwork for technical indicators scraper function

if __name__ == "__main__":
   ticker_lst = get_tickers()
   build_csv(ticker_lst)

# thinking about dataloader
# separate file for last update either at dir level or file dict level
#sp500daily/aon.csv - some updated csv of olhcv

# most basic symbol level
# {sym : data}

# most basic at the dir level
# read_dir()
# master_data = {}
# master_data['symbol_prices'] = {}
# master_data['symbol_macd'] = {}
# master_data.items() -> ['symbol'], {}
# master_data['pe_ratio'] = {}
# master_data.items() -> ['symbol', 'pe_ratio'], {}
# master_data['symbol']['aon'] = dataframe
# master_data.items() -> ['symbol', 'pe_ratio'], {'aon'} : pd.DataFrame(all the historical data for aon)
# master_data['pe_ratio']['aon'] = dataframe has cols o,l,h,c,adj,v,macd,bb,sma,eda, ...

# for s in sp500dir:
# master_data['symbol'][s] = pd.read_csv()

# for s in sp500dir:
# master_data['pe_ratio'][s] = pd.read_csv()

# for s in sp500dir:
# master_data['earnings'][s] = pd.read_csv()


# { 'symbol' : {sym : data}}
# { 'sym' : col of data} or just a dataframe of cols are symbols, rows are feature


# sp500/amzn/daily, weekly, earnings, 
# sp500daily/amzn.csv
# sp500weekly/amzn.csv


# index, aon, mmm
# 1, 45, 57
# 2, 47, 55


