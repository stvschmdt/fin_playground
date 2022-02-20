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

def build_csv_dict(ticker_lst):
    master_dict = {}
    for ticker in ticker_lst:
        test, _ = ts.get_daily(ticker, outputsize='full')
        cols = ['open', 'high', 'low', 'close', 'volume']
        file_loc = "SP500_daily_data/" + ticker
        test.to_csv(file_loc)
        time.sleep(12)

if __name__ == "__main__":
   ticker_lst = get_tickers()
   build_csv_dict(ticker_lst)


