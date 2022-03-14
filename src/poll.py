# functions responsible for the extraction of data
# from an API, with various save methods (getter only)

#test push

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import alpha_vantage.techindicators as ti
import alpha_vantage.cryptocurrencies as cc
import alpha_vantage.fundamentaldata as fd
import collections
import csv
import os
import time
from datetime import datetime
from pathlib import Path
from datetime import datetime
# custom imports
import logger

logger = logger.Logging()

today = datetime.today().strftime('%Y-%m-%d')

#sp_names = pd.read_csv('constituents_csv.csv')
#sp_financials = pd.read_csv('constituents-financials_csv.csv')

abspath = os.path.abspath(os.getcwd())
finpath = Path(abspath).resolve().parent

api_path = str(finpath) + '/api_key.txt'
with open(api_path) as f:
    API_key = f.readlines()[0]
    API_key = API_key.strip('\n')
ts = TimeSeries(key=API_key, output_format='pandas')
indicators = ti.TechIndicators(key=API_key, output_format='pandas')
fundamentals = fd.FundamentalData(key=API_key, output_format='pandas')
crypto = cc.CryptoCurrencies(key=API_key, output_format='pandas')

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

#ticker_lst = ["AAPL", "MMM", "XRX", "ZION", "ZTS"]

def build_csv(ticker_lst, timeframe='daily', cols = ['open', 'high', 'low', 'close',
                                                     'adj_close', 'volume', 'dividend', 'split_coeff']):
    # do a check for which one to read in
    # add in some appropriate reasonable time stamp
    bad_tickers = []
    good_tickers = []
    features = ['SMA', 'EMA', 'WMA', 'MACD', 'STOCH', 'RSI', 'MOM', 'ROC', 'MFI', 'BBANDS', 'MIDPRICE']
    tech_indicators_dict = tech_indicators_dict_initialize(features, timeframe)
    count = 0
    start_t = time.time()
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

                
                data_file_loc = str(finpath) + "/storage/daily/tickers/" + ticker # writes full ticker file to storage
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
        count += 12
        if count > 63:
            end_t = time.time()
            time_diff = int(end_t - start_t)
            time.sleep(61 - time_diff)
            count = 0
            start_t = time.time()
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
        path = str(finpath) + '/storage/' + timeframe + '/features/' + feature
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

def get_coins():
    filepath = str(finpath) + '/digital_currency_list.csv'
    tables = pd.read_csv(filepath)
    currency_lst = tables["currency code"].to_list()
    return currency_lst

def build_crypto_csvs(currency_lst, timeframe='daily', cols = ['open', 'open 2', 'high', 'high 2', 'low', 'low 2',
                                            'close', 'close 2', 'volume', 'market cap']):
    parent_path = str(finpath)
    market = "USD"
    count = 0
    start_t = time.time()
    bad_currencies = []
    currency_lst = ['BTC']
    for currency in currency_lst:
        try:
            if timeframe == 'daily':
                data = crypto.get_digital_currency_daily(currency, market)[0]
                data.columns = cols
                data = data.drop(['open 2', 'high 2', 'low 2', 'close 2'], axis=1)
            filepath = parent_path + '/storage/' + timeframe + '/cryptocurrencies/' + currency
            data.to_csv(filepath)
            count += 1
        except:
            bad_currencies.append(currency)
        if count > 70:
            end_t = time.time()
            time_diff = int(end_t - start_t)
            time.sleep(61 - time_diff)
            count = 0
            start_t = time.time()
    print(bad_currencies)

def build_fundamental_data(ticker_lst):
    count = 0
    start_t = time.time()
    bad_tickers = []
    for ticker in ticker_lst:
        try:
            quarterly_income_statement = fundamentals.get_income_statement_quarterly(ticker)[0]
            annual_income_statement = fundamentals.get_income_statement_annual(ticker)[0]
            quarterly_balance_sheet = fundamentals.get_balance_sheet_quarterly(ticker)[0]
            annual_balance_sheet = fundamentals.get_balance_sheet_annual(ticker)[0]
            quarterly_cash_flow = fundamentals.get_cash_flow_quarterly(ticker)[0]
            annual_cash_flow = fundamentals.get_cash_flow_annual(ticker)[0]
            company_overview = fundamentals.get_company_overview(ticker)[0]
            quarterly_income_statement_file_loc = str(finpath) + "/storage/fundamental_data/annual/income_statement/" + ticker
            quarterly_income_statement.to_csv(quarterly_income_statement_file_loc, index='date')
            annual_income_statement_file_loc = str(finpath) + "/storage/fundamental_data/quarterly/income_statement/" + ticker
            annual_income_statement.to_csv(annual_income_statement_file_loc, index='date')
            quarterly_balance_sheet_file_loc = str(finpath) + "/storage/fundamental_data/annual/balance_sheet/" + ticker
            quarterly_balance_sheet.to_csv(quarterly_balance_sheet_file_loc, index='date')
            annual_balance_sheet_file_loc = str(finpath) + "/storage/fundamental_data/quarterly/balance_sheet/" + ticker
            annual_balance_sheet.to_csv(annual_balance_sheet_file_loc, index='date')
            quarterly_cash_flow_file_loc = str(finpath) + "/storage/fundamental_data/annual/cash_flow/" + ticker
            quarterly_cash_flow.to_csv(quarterly_cash_flow_file_loc, index='date')
            annual_cash_flow_file_loc = str(finpath) + "/storage/fundamental_data/quarterly/cash_flow/" + ticker
            annual_cash_flow.to_csv(annual_cash_flow_file_loc, index='date')
            company_overview_file_loc = str(finpath) + "/storage/fundamental_data/company_overview/" + ticker
            company_overview.to_csv(company_overview_file_loc, index='date')
        except Exception as e:
            print(e)
            bad_tickers.append(ticker)
        count += 7
        if count > 68:
            end_t = time.time()
            time_diff = int(end_t - start_t)
            time.sleep(61 - time_diff)
            count = 0
            start_t = time.time()
    print(bad_tickers)

if __name__ == "__main__":
    ticker_lst = get_sp500_tickers()
    print('ticker list read')
    currency_lst = get_coins()
    print('coin list read')
    build_csv(ticker_lst)
    print('ticker csvs built')
    build_fundamental_data(ticker_lst)
    print('fundamentals built')
    build_crypto_csvs(currency_lst)
    print('coins built')
    

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


