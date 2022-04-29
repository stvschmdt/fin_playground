#uses 1 row of data to predict next adjusted close
#uses data from all available tickers

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

from dataloader import *


pd.options.mode.chained_assignment = None


abspath = os.path.abspath(os.getcwd())
finpath = Path(abspath).resolve().parent
parent_path = str(finpath) + '/'


ticker_lst = ['AAPL', 'MMM', 'ZION']


#print(ticker_dict)


def add_pct_changes(df):
    columns = df.columns
    for column in columns:
        column_name = column + '_pct_change'
        df[column_name] = df[column].pct_change(-1)
        #print(df[column_name])
    return df

def shift_columns(df, n=0):
    columns = df.columns
    for column in columns:
        for i in range(1, n+1):
           column_name = column + '_shift_' + str(i)
           df[column_name] = df[column].shift(-i)
    return df


def get_appended_df(dictionary, add_pcts = True, shift = True, shift_n = 3):
    count = 1
    tickers = list(dictionary.keys())
    print(tickers)
    for ticker in tickers:
        new_data = dictionary[ticker]['daily']
        if add_pcts:
            new_data = add_pct_changes(new_data)
        if shift:
            new_data = shift_columns(new_data, shift_n)
        if count == 1:
            begin = new_data
            print('ADDED', ticker)  
            print(begin)
            count += 1
            continue
        #print(new_data)    
        begin = pd.merge(begin, new_data, on='date', how='outer')
        print('ADDED', ticker)  
        print(begin)
        count += 1
    return begin.dropna(axis=0)

def get_y(ticker_to_predict):
     path = parent_path + 'storage/daily/tickers/' + str(ticker_to_predict)
     df = pd.read_csv(path)
     y = df['close'].pct_change(-1)
     return y.shift(1)

def decision_tree_regressor(df, ticker_to_predict):
    df = df.iloc[1:, :]
    length = len(df)
    y = get_y(ticker_to_predict)
    y = y[:len]
    model = XGBRegressor(n_estimators = 250, learning_rate = 0.02, random_state=0)
    X_train, X_valid, y_train, y_valid = train_test_split(df, y, train_size=0.8, test_size=0.2)



ticker_dict = build_ticker_dicts(ticker_lst, 'daily')
#print(get_appended_df(ticker_dict))
print(get_y('AAPL'))
