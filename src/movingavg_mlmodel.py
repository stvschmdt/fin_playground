import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from datetime import datetime
import math
import pandas as pd
import numpy as np
from setuptools import SetuptoolsDeprecationWarning
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor, XGBClassifier
from sklearn.model_selection import train_test_split

from dataloader import *

#this code implements a moving average based decision tree
#the method is from this paper: https://www.sciencedirect.com/science/article/pii/S1877050920307924



ticker_dict = build_ticker_dicts(['AAPL'], 'daily')
ticker_df = ticker_dict['AAPL']['daily']
ticker_df = ticker_df.iloc[::-1]
ticker_df = ticker_df[['open', 'high', 'low', 'close']]
print(ticker_df)

def generate_x_df(ticker_df):
    x_df = ticker_df.copy()
    x_df['h-l'] = x_df['high'] - x_df['low']
    x_df['o-c'] = x_df['open'] - x_df['close']
    x_df['ma_7'] = x_df['close'].rolling(7).mean()
    x_df['ma_14'] = x_df['close'].rolling(14).mean()
    x_df['ma_21'] = x_df['close'].rolling(21).mean()
    x_df['std_7'] = x_df['close'].rolling(7).std()
    x_df = x_df.dropna(axis=0)
    return x_df[['h-l', 'o-c', 'ma_7', 'ma_14', 'ma_21', 'std_7']][:-1]

def generate_y(ticker_df):
    return ticker_df['close'].shift(-1)[20:].dropna()


def decision_tree_regressor(ticker_df):
    x = generate_x_df(ticker_df)
    y = generate_y(ticker_df)
    y_acc_valid = np.where(y >= y.shift(1), 1, -1)
    split = int(math.floor(0.8*len(x)))
    x_train, x_test, y_train, y_test = x[:split], x[split:], y[:split], y[split:]
    model = XGBRegressor(n_estimators=500, learning_rate=0.02, random_state=0)
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    y_acc_valid = np.where(y_test >= y_test.shift(1), 1, -1)
    bin_preds = np.where(preds >= y_test.shift(1), 1, -1)
    #print(y_acc_valid, bin_preds)
    binacc_valid = np.where(y_acc_valid==bin_preds, 1, 0)
    print(sum(binacc_valid)/len(binacc_valid))

    #print(preds)
    #print(preds[-20:], y_test[-20:])
    #print(np.percentile(preds - y_test, 60))
    #mse = (np.square(preds - y_test)).mean()
    #print(mse)


decision_tree_regressor(ticker_df)


