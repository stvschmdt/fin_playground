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

def build_csv(ticker_lst, timeframe='day', cols = ['open', 'high', 'low', 'close', 'volume']):
    # do a check for which one to read in
    # add in some appropriate reasonable time stamp
    bad_tickers = []
    for ticker in ticker_lst:
        try:
            if timeframe == 'day':
                data, _ = ts.get_daily(ticker, outputsize='full')
                data_file_loc = "SP500_daily_data/" + ticker
            elif timeframe == "week":
                data, _ = ts.get_weekly(ticker, outputsize='full')
                data_file_loc = "SP500_weekly_data/" + ticker
            elif timeframe == "month":
                data, _ = ts.get_monthly(ticker, outputsize='full')
                data_file_loc = "SP500_monthly_data/" + ticker
            data.to_csv(data_file_loc)
        except:
            bad_tickers.append(ticker)
        time.sleep(1)
    print(bad_tickers)

    # bad_tickers = ['AGN', 'APC', 'BBT', 'BF.B', 'COG', 'CBS', 'CXO', 'LB', 'MYL', 'RHT', 'COL', 'SCG', 'TMK', 'VAR', 'WLTW']
    # need to add date_time functionality to write a timestamp of when the function was run to a file

def build_monthly(ticker_list):
    sp_path = 'storage/monthly/SP500/'
    for ticker in ticker_list:
        basic_data, _ = ts.get_monthly(ticker, outputsize='full')
        #function that loops through the tech indicators
        #and then we add the columns, both to basic_data and the feature specific df
        basic_data.to_csv(sp_path + ticker)




#want a function that takes a ticker and returns a column of data for a specific feature

def add_tech_indicators(ticker_list):
    
    for split in ['daily', 'weekly', 'monthly']:
        daily = pd.DataFrame()
        weekly = pd.DataFrame()
        monthly = pd.DataFrame()
        for ticker in ticker_list:
            data, _ = indicators.get_sma(ticker, interval=split)
            daily = pd.merge(left=daily, right=data, on='date')
            


test_ticker_list = ['aon', 'mmm', 'aapl', 'msft', 'goog']

sma_aapl, _ = indicators.get_sma('aapl', interval='daily')

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

