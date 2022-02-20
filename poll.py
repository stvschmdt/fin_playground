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

API_key = '7CKGY5COYII98PRI'

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

def build_csv(ticker_lst, timeframe='day', cols = ['open', 'high', 'low', 'close', 'volume']):
    # do a check for which one to read in
    # add in some appropriate reasonable time stamp
    for ticker in ticker_lst:
        # if full exists in dir
        daily, _ = ts.get_daily(ticker, outputsize='full')
        # else
        # daily, _ = ts.get_daily(ticker, outputsize='compact')
        # read in the full dataframe, merge the two
        weekly, _ = ts.get_weekly(ticker, outputsize='full')
        monthly, _ = ts.get_monthly(ticker, output_size='full')
        #cols = ['open', 'high', 'low', 'close', 'volume']
        daily_file_loc = "SP500_daily_data/" + ticker
        weekly_file_loc = "SP500_weekly_data" + ticker
        monthly_file_loc = "SP500_monthly_data" + ticker
        daily.to_csv(daily_file_loc)
        weekly.to_csv(weekly_file_loc)
        monthly.to_csv(monthly_file_loc)
        time.sleep(12)

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

