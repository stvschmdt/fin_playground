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
# custom imports
import logger

logger = logger.Logging()

today = datetime.today().strftime('%Y-%m-%d')

API_key = ''

#sp_names = pd.read_csv('constituents_csv.csv')
#sp_financials = pd.read_csv('constituents-financials_csv.csv')

ts = TimeSeries(key=API_key, output_format='pandas')
indicators = ti.TechIndicators(key=API_key, output_format='pandas')



# ---- econ indicators
#directory is storage/econ_indicators/econ_indicator
#then annual, daily, monthly, weekly, daily within it
#figure out the timeframes for econ data and begin pulling it



# ---- fundamental data
#most are annual and quarterly, but some are not
#could do storage/fundamental/annual/feature, or could do same structure as econ indicators
#I'm inclined towards the second
#storage/fundamental/annual/feature leads to a csv where tickers are columns and rows are the feature



#loop through tickers
#add basic price data to SP 500 folder
#go through each tech indicator and get a column for that ticker
#add the column to SP 500 folder and the csv for that feature
#separate function for each timeframe?

#technicals: SMA, EMA, WMA, MACD, STOCH, RSI, MOM, ROC, MFI, BANDS, MIDPRICE

features = ['SMA', 'EMA', 'WMA', 'MACD', 'STOCH', 'RSI', 'MOM', 'ROC', 'MFI', 'BBANDS', 'MIDPRICE']

def build_csv(ticker_lst, timeframe='daily', cols = ['open', 'high', 'low', 'close',
                                                     'adj_close', 'volume', 'dividend', 'split_coeff']):
    # do a check for which one to read in
    # add in some appropriate reasonable time stamp
    bad_tickers = []
    good_tickers = []
    features = ['SMA', 'EMA', 'WMA', 'MACD', 'STOCH', 'RSI', 'MOM', 'ROC', 'MFI', 'BBANDS', 'MIDPRICE']
    tech_indicators_dict = tech_indicators_dict_initialize(features, timeframe)
    for ticker in ticker_lst:
        try:
            if timeframe == 'daily':
                data, _ = ts.get_daily_adjusted(ticker, outputsize='full')
                data.columns = cols
                length = data.shape[0]
                
                #begin adding tech indicators here
                
                sma, _ = indicators.get_sma(ticker, timeframe)
                data['SMA'] = correct_length(length, sma['SMA'].to_list())
                tech_indicators_dict['SMA'].append(sma['SMA'].to_list())
                print('made sma', ticker)

                ema, _ = indicators.get_ema(ticker, timeframe)
                data['EMA'] = correct_length(length, ema['EMA'].to_list())
                tech_indicators_dict['EMA'].append(ema['EMA'].to_list())
                print('made ema', ticker)

                wma, _ = indicators.get_wma(ticker, timeframe)
                data['WMA'] = correct_length(length, wma['WMA'].to_list())
                tech_indicators_dict['WMA'].append(wma['WMA'].to_list())
                print('made wma', ticker)

                macd, _ = indicators.get_macd(ticker, timeframe)
                data['MACD'] = correct_length(length, macd['MACD'].to_list())
                tech_indicators_dict['MACD'].append(macd['MACD'].to_list())
                print('made macd', ticker)
                
                stoch, _ = indicators.get_stoch(ticker, timeframe)
                data['SLOWD'] = correct_length(length, stoch['SlowD'].to_list())
                data['SLOWK'] = correct_length(length, stoch['SlowK'].to_list())
                print(stoch)
                tech_indicators_dict['STOCH'].append(stoch.values)
                #values are appended in as a list of lists, where the first term
                #is SlowD and the second term is SlowK: (SlowD, SlowK)
                print('made stoch', ticker)

                rsi, _ = indicators.get_rsi(ticker, timeframe)
                data['RSI'] = correct_length(length, rsi['RSI'].to_list())
                tech_indicators_dict['RSI'].append(rsi['RSI'].to_list())
                print('made rsi', ticker)

                mom, _ = indicators.get_mom(ticker, timeframe)
                data['MOM'] = correct_length(length, mom['MOM'].to_list())
                tech_indicators_dict['MOM'].append(mom['MOM'].to_list())
                print('made mom', ticker)

                roc, _ = indicators.get_roc(ticker, timeframe)
                data['ROC'] = correct_length(length, roc['ROC'].to_list())
                tech_indicators_dict['ROC'].append(roc['ROC'].to_list())
                print('made roc', ticker)

                mfi, _ = indicators.get_mfi(ticker, timeframe)
                data['MFI'] = correct_length(length, mfi['MFI'].to_list())
                tech_indicators_dict['MFI'].append(mfi['MFI'].to_list())
                print('made mfi', ticker)

                bbands, _ = indicators.get_bbands(ticker, timeframe)
                print(bbands)
                data['LBAND'] = correct_length(length, bbands['Real Lower Band'].to_list())
                data['UBAND'] = correct_length(length, bbands['Real Upper Band'].to_list())
                data['MBAND'] = correct_length(length, bbands['Real Middle Band'].to_list())
                tech_indicators_dict['BBANDS'].append(bbands.values)
                # First term in list of values is LBand, then UBand, then MBand: (LBand, UBand, MBand)
                print('made bbands', ticker)

                midprice, _ = indicators.get_midprice(ticker, timeframe)
                print(midprice)
                data['MIDPRICE'] = correct_length(length, midprice['MIDPRICE'].to_list())
                tech_indicators_dict['MIDPRICE'].append(midprice['MIDPRICE'].to_list())
                print('made midprice', ticker)

                print('made feature dict')

                
                data_file_loc = "storage/daily/tickers/" + ticker # writes full ticker file to storage
                data.to_csv(data_file_loc, index='date')
            elif timeframe == "weekly":
                data, _ = ts.get_weekly(ticker, outputsize='full')
                data_file_loc = "SP500_weekly_data/" + ticker
            elif timeframe == "monthly":
                data, _ = ts.get_monthly(ticker, outputsize='full')
                data_file_loc = "SP500_monthly_data/" + ticker
            good_tickers.append(ticker)
        except:
            bad_tickers.append(ticker)
            return -1
        #need a function that names the columns in the technical indicators dataframes we've constructed
        time.sleep(1)
    print('begin writing')
    write_all_features(tech_indicators_dict, features, good_tickers, timeframe)
    print('finish writing')
    print(len(tech_indicators_dict["SMA"]))
    print(bad_tickers)
    return 0

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

def write_all_features(tech_indicators_dict, features, good_tickers, timeframe):
    for feature in features:
        path = 'storage/' + timeframe + '/features/' + feature
        print(path)
        feature_df = fit_tech_to_df(tech_indicators_dict[feature], cols=good_tickers)
        feature_df.to_csv(path)

def correct_length(length, tech_data):
    if length > len(tech_data):
        a = length - len(tech_data)
        empty_lst = [np.nan]*a
        tot_lst = tech_data + empty_lst
        return tot_lst
    elif length < len(tech_data):
        ind_lst = tech_data["SMA"].to_list()[:length]
    else:
        ind_lst = tech_data["SMA"].to_list()
    return ind_lst


def date_getter(timeframe):
    print(timeframe)
    if timeframe == 'daily':
        data, _ = ts.get_daily_adjusted(symbol='MMM', outputsize='full')
    elif timeframe == 'weekly':
        data, _ = ts.get_weekly(symbol='MMM')
    elif timeframe == 'monthly':
        data, _ = ts.get_monthly(symbol='MMM')
    else:
        print('not a valid time step')
        return
    return np.array(data.index)

def get_sp500_tickers():
    tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp500 = tables[0]
    print(sp500['Symbol'].to_list())
    return sp500['Symbol'].to_list()

print(build_csv(ticker_lst=["AAPL", "MMM", "XRX", "ZION", "ZTS", "TSLA"]))

if __name__ == "__main__":
    
    print('hi')
    #tickers = get_sp500_tickers()
    #ticker_lst = get_tickers()
    #build_csv(ticker_lst)
    

#print(date_getter('daily'))
#print(tech_indicators_dict_initialize(['SMA'], 'daily'))


#want a function that takes a ticker and returns a column of data for a specific feature


# scratchwork for technical indicators scraper function


   


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


