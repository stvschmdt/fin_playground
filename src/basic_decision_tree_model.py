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
from xgboost import XGBRegressor, XGBClassifier
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
        begin = pd.merge(begin, new_data, on='date', how='outer')
        print('ADDED', ticker)  
        
        count += 1
    print(begin[begin.isna().any(axis=1)])
    print(begin.shape)
    print(begin.dropna(axis=0).shape)
    return begin.dropna(axis=0)

def get_y(ticker_to_predict):
     path = parent_path + 'storage/daily/tickers/' + str(ticker_to_predict)
     df = pd.read_csv(path)
     df = df.dropna(axis = 0)
     y = df['close'].pct_change(-1)
     return y.shift(1).dropna()

def decision_tree_classifier(df, ticker_to_predict, pos_threshold, neg_threshold):
    df = df.iloc[1:, :]
    length = len(df)
    y = get_y(ticker_to_predict)
    y = y[:length]
    model = XGBClassifier(n_estimators = 250, learning_rate = 0.02, random_state=0)
    x_train, x_valid, y_train, y_valid = train_test_split(df, encode_y(y, pos_threshold, neg_threshold), train_size=0.8, test_size=0.2)
    model.fit(x_train, y_train)
    preds = model.predict(x_valid)
    print(preds)

def encode_y(y, pos_threshold, neg_threshold):
    encoded_y = [encode_method(pos_threshold, neg_threshold, i) for i in y]
    return encoded_y

def encode_method(pos_threshold, neg_threshold, x):
    if x >= pos_threshold:
        return 1
    if x <= neg_threshold:
        return -1
    return 0






ticker_dict = build_ticker_dicts(ticker_lst, 'daily')
df = get_appended_df(ticker_dict)
print(get_y('AAPL'))

#print(encode_y(get_y('AAPL'), 0.01, -0.01))

#print(df[df == np.inf].count())
#print(len(df))

decision_tree_classifier(df, 'AAPL', 0.01, -0.01)