import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
import collections
import csv
import os
import time
import json
from datetime import datetime
from pathlib import Path
from datetime import datetime
import random
# custom imports
import logger
import requests


abspath = os.path.abspath(os.getcwd())
finpath = Path(abspath).resolve().parent

api_path = str(finpath) + '/ftx_key.txt'

with open(api_path) as f:
    lines = f.readlines()
    API_key = lines[0]
    API_secret = lines[1]
    API_key = API_key.strip('\n')
    API_secret = API_secret.strip('\n')


def get_orderbook_once():
    orderbook = requests.get('https://ftx.com/api/markets/BTC/USDT/orderbook').json()

    orderbook_asks = pd.DataFrame(orderbook['result']['asks'])
    orderbook_bids = pd.DataFrame(orderbook['result']['bids'])
    df = pd.merge(orderbook_bids , orderbook_asks , left_index=True, right_index=True)  
    df = df.rename({"0_x":"Bid Price","1_x":"Bid Amount",
                "0_y":"Ask Price","1_y":"Ask Amount"}, axis='columns')
    df = df[['Bid Amount', 'Bid Price', 'Ask Price', 'Ask Amount']]
    return df

def update():
    label['text'] = get_orderbook_once()
    window.after(1000, update)

window = Tk()

window.geometry('300x500')
window.title('order book')

label = Label(window, text='hello')
label.pack()

update()

window.mainloop()



# while True:
#     try:
#         orderbook = requests.get('https://ftx.com/api/markets/BTC/USDT/orderbook').json()

#         orderbook_asks = pd.DataFrame(orderbook['result']['asks'])
#         orderbook_bids = pd.DataFrame(orderbook['result']['bids'])
#         df = pd.merge(orderbook_bids , orderbook_asks , left_index=True, right_index=True)  
#         df = df.rename({"0_x":"Bid Price","1_x":"Bid Amount",
#                 "0_y":"Ask Price","1_y":"Ask Amount"}, axis='columns')
#         print(df)
    
#     except KeyboardInterrupt:
#         print('done')
#         break