import pandas as pd
import numpy as np
import csv 


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





if __name__ == '__main__':
    sim = BBand(portfolio=['AAPL'])
    print(sim.portfolio)
    sim.get_portfolio_data()
    print(len(sim.data))
    print(len(sim.data[0]))
