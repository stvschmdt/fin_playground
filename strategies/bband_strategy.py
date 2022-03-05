import pandas as pd
import numpy as np
import csv 

from ..src import Account

class BBand(object):

    def __init__(self, portfolio = [], weights = [], path='../storage/daily/tickers/'):
        self.portfolio = portfolio
        self.path = path
        self.weights = weights
        if not len(weights):
            self.weights = self.create_portfolio_split()

    def create_portfolio_split(self):
        num = len(self.portfolio)
        equal_weights = int(100. / num) / 100.
        return equal_weights

    def get_portfolio_data(self):
        data = []
        for p in self.portfolio:
            symdata = pd.read_csv(self.path + p)
            data.append(symdata)
        self.data = data
        return self.data

    def upper_hit(self, row):
        if row[1].close > row[1].UBAND:
            return 1
        else:
            return 0

    def lower_hit(self, row):
        if row[1].close < row[1].LBAND:
            return 1
        else:
            return 0


    def walkthrough(self, data, start, end):
        df = data[(data.date >=start) & (data.date <= end)]
        for i in df.iterrows():
            if i[1].close > i[1].UBAND:
                print(i[0])
            elif i[1].close < i[1].LBAND:
                print(i[0])


if __name__ == '__main__':
    sim = BBand(portfolio=['AAPL'])
    print(sim.portfolio)
    sim.get_portfolio_data()
    print(len(sim.data))
    print(sim.data[0])
    sim.walkthrough(sim.data[0], "2020-01-01", "2022-02-10")
