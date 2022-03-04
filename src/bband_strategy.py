import pandas as pd
import numpy as np
import csv 

from account import Account

class BBand(object):

    def __init__(self, portfolio = [], weights = [], path='../storage/daily/tickers/'):
        self.portfolio = portfolio
        self.path = path
        self.weights = weights
        self.account = Account('bband', 100000)
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
        #print(len(df))
        #print(df[df.date == start])
        #print(df[df.date == start].close.item())
        numshares = int(self.account.balance / df[df.date == start].close.item())
        print('starting quantity', start, numshares, self.account.balance)
        numshares = self.account.buy('AAPL', numshares, df[df.date == start].close.item())
        print('starting buy', start, numshares, self.account.balance)
        df = df[::-1]
        for i in df.iterrows():
            if i[1].date == start:
                continue
            if i[1].close > i[1].UBAND and numshares > 0:
                numshares = self.account.sell('AAPL', numshares, df[df.date == i[1].date].close.item())
                print('upper hit: new quantity', i[1].date, numshares, self.account.balance)
            elif i[1].close < i[1].LBAND and numshares == 0:
                numshares = int(self.account.balance / df[df.date == i[1].date].close.item())
                numshares = self.account.buy('AAPL', numshares, df[df.date == i[1].date].close.item())
                print('lower hit: new quantity', i[1].date, numshares, self.account.balance)
        if numshares > 0:
            numshares = self.account.sell('AAPL', numshares, df[df.date == end].close.item())
        print(self.account.balance)


if __name__ == '__main__':
    sim = BBand(portfolio=['AAPL'])
    print(sim.portfolio)
    sim.get_portfolio_data()
    #print(len(sim.data))

    # make sure start and end are valid trading days!!
    sim.walkthrough(sim.data[0], "2015-06-10", "2022-02-10")
