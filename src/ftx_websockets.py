from xml.etree.ElementTree import TreeBuilder
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
from websocket import create_connection
import websockets
import asyncio

abspath = os.path.abspath(os.getcwd())
finpath = Path(abspath).resolve().parent

api_path = str(finpath) + '/ftx_key.txt'

with open(api_path) as f:
    lines = f.readlines()
    API_key = lines[0]
    API_secret = lines[1]
    API_key = API_key.strip('\n')
    API_secret = API_secret.strip('\n')


# async def listen():
#     url = 'wss://ftx.us/ws/'

#     async with websockets.connect(url) as ws:
#         ws.send(json.dumps({'op':'subscribe', 'channel':'orderbook', 'market':'BTC/USD'}))
        
#         while True:
#             ws.send(json.dumps({'op':'subscribe', 'channel':'orderbook', 'market':'BTC/USD'}))


#             msg = ws.recv()
#             msg = json.loads(msg) 
#             print(msg)

#asyncio.get_event_loop().run_until_complete(listen())

print('starting')
ws = create_connection('wss://ftx.us/ws/')

print('connected')

ws.send(json.dumps({'op':'subscribe', 'channel':'orderbook', 'market':'BTC/USD'}))


while True:
    result = ws.recv()
    result = json.loads(result)
    print(result)







