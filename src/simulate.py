# functions to simulate trade actions
# buy, sell w boolean success/fails
# stateless mechanics operating as an environment

# python imports
import csv
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import collections

# custom imports
import logger
import account

class Simulate(object):

    def __init__(self, name, start_bal=100000, time_steps=100, save_dir='backup/', restore=False, config=None):
        self.name = name
        self.save_dir = save_dir
        self.account = account.Account(name, start_bal)
        self.log = logger.Logging()
        self.portfolio = {}
        self.baseline = {}
        self.baseline = account.Account('baseline', start_bal)
        self.actions = {}
        self.start = None
        self.end = None

    def run_default_spy(self, start, end, spypath='SPY_2021-12-20.csv'):
        self.start = start
        self.end = end
        spy = pd.read_csv(spypath)
        #print(spy.head())
        quantity = self.buy_max(self.baseline, start, spy)
        self.baseline.sell('SPY', quantity, spy[spy.date == end].close[0])
        base = start
        date_list = spy.date[(spy.date >= start) & (spy.date <=end)].values
        rolling = self.get_rolling(spy.close[(spy.date >= start) & (spy.date <=end)])
        closing = self.get_rolling(spy.close[(spy.date == start) | (spy.date == end)])
        plt.plot(date_list, rolling, color='k')
        plt.title('SPY Baseline: Period Gain {:.2f}%'.format(closing.values[-1]))
        plt.xticks(rotation=45)
        plt.show()
        return 0

    def get_rolling(self, slice, window=1):
        rolling = slice.pct_change(window).fillna(0)
        return rolling

    def buy_max(self, account, t, data):
        #print(data[data.date == t].close)
        quantity = account.balance // data[data.date == t].close.item()
        price = data[data.date == t].close.item()
        account.buy('SPY', quantity, data[data.date == t].close.item(), True)
        return quantity


    def set_actions(self):
        return 0

    def roll_forward(self, start):
        # move ahead one action step (day, minute, until)
        # process in account, process actions, baseline

        return 0 

if __name__ == '__main__':
    sim = Simulate('testsim')
    print(sim.account.balance)
    sim.run_default_spy('2021-01-04', '2021-12-17')
    sim.baseline.view_balance_history()
