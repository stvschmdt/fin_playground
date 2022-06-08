import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
from setuptools import SetuptoolsDeprecationWarning
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor, XGBClassifier
from sklearn.model_selection import train_test_split

from dataloader import *


def rsi_method(ticker):
    ticker_dict = build_ticker_dicts([ticker], 'daily')
    ticker_df = ticker_dict[ticker]['daily']
    rsi_df = ticker_df[['close', 'RSI']]
    rsi_df['signal'] = encode_rsi(rsi_df['RSI'])
    rsi_df['pct_change'] = rsi_df['close'].pct_change(-1).shift(1)
    rsi_df['pct_change_in_portfolio'] = 1 + rsi_df['pct_change'] * rsi_df['signal']
    rsi_df['portfolio_value'] = rsi_df['pct_change_in_portfolio'][::-1].cumprod()
    print(rsi_df['portfolio_value'][1])
    print((rsi_df['close'][0] - rsi_df['close'][-1]) / rsi_df['close'][-1])
    return rsi_df['portfolio_value'][1]

def encode_rsi(lst):
    return [encode_method(i) for i in lst]

def encode_method(x):
    if x > 70:
        return 1
    elif x < 30:
        return -1
    else:
        return 0

rsi_method('AAPL')


