# core functions for account management
# stateless w boolean checks

# python imports
import csv
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import collections

# custom imports
import logger

class Account(object):

    def __init__(self, name, balance):
        # use our logger class
        self.log = logger.Logging()
        self.name = name
        self.balance = balance
        self.history = {'action' : [], 'buy': [], 'sell' : [], 'balance' : [], 'day' : []}
        self.history['balance'].append(balance)
        self.history['action'].append('open')
        self.holdings = collections.defaultdict(int)
        self.log.info('created account {}'.format(name))

    def deposit(self, cash):
        self.balance += cash
        self.log.info('deposit balance {}'.format(self.balance))
        return 0

    def withdrawal(self, cash):
        if cash <= self.balance:
            self.balance += cash
            self.log.info('deposit balance {}'.format(self.balance))
        else:
            self.log.error('insufficient funds, requested: {},  balance: {}'.format(cash, self.balance))
        return 0

    def get_history(self):
        return self.history

    def get_holdings(self):
        return self.holdings

    def get_balance(self):
        return self.balance

    def pretty_display(self):
        # pretty print account details
        return 0

    def view_balance_history(self, save=False):
        fig, ax = plt.subplots(figsize=(5, 3))
        fig.subplots_adjust(bottom=0.15, left=0.2)
        ax.plot(self.history['balance'], c='k')
        ax.set_xlabel('Time')
        ax.set_ylabel('Balance', labelpad=18)
        plt.title('{} Account Summary'.format(self.name))
        plt.xticks([])
        plt.show()

    def buy(self, asset, quantity, price, partial=False, info=None):
        '''
        partial: if attempting to purchase 5, but balance supports 3, buy 3 else buy 0
        input buy details, check for balance requirements
        output -1 : no buy, +N : quantity bought
        '''
        # fail path - insufficient funds for 1
        # check for future partial unit crypto
        if quantity < 1 and quantity > 0:
            ask = quantity * price
        else:
            ask = price
        if ask >= self.balance:
            self.log.error('insufficient funds, requested: {}x{}, balance: {}'.format(quantity, ask, self.balance))
            return -1
        # happy path
        if quantity * price <= self.balance:
           # execute buy and accounting
            self.balance -= quantity * price
            self.history['balance'].append(self.balance)
            self.history['action'].append('buy')
            self.holdings[asset] += quantity
            # history buy tuple
            self.history['buy'].append( (asset, quantity, price) )
            self.log.info('filled {} of {} at {}'.format(quantity, asset, price))
        else:
            if not partial:
                self.log.error('insufficient funds, requested: {}x{}, balance: {}'.format(quantity, price, self.balance))
            return -1

            fill = 0
            # check how many could be filled for execution
            for i in range(1, quantity):
                if i * price <= self.balance:
                    fill += 1
                else:
                    break
           # execute buy and accounting
            self.balance -= fill * price
            self.history['balance'].append(self.balance)
            self.history['action'].append('buy')
            self.holdings[asset] += quantity
            self.holdings[asset] += fill
            # history buy tuple
            self.history['buy'].append( (asset, fill, price) )
            #reset for return
            quantity = fill
            self.log.info('partial fill {} of {} at {}'.format(quantity, asset, price))
        return quantity

    def sell(self, asset, quantity, price, info=None):
        '''
        '''
        if asset not in self.holdings:
            self.log.error('{} not held to sell'.format(asset))
        else:
            if self.holdings[asset] < quantity:
                self.log.error('{} sell request exceeds ownership'.format(asset))
            else:
                # execute sell
                self.holdings[asset] -= quantity
                self.balance += quantity * price
                self.history['balance'].append(self.balance)
                self.history['sell'].append( (asset, quantity, price) )
                self.history['action'].append('sell')
                self.log.info('sold {} of {} at {}'.format(quantity, asset, price))
        return quantity


    def buys(self, assets, quantities, prices, info=None):
        ''' takes an ORDERED list of assets to buy
            returns dictionary of fullments
        ''' 
        return 0


if __name__ == '__main__':
    # testing
    acc = Account('test', 100)
    soxl = 45
    acc.buy('soxl', 3,  soxl, False)
    print(acc.holdings)
    acc.buy('soxl', 2,  soxl, True)
    print(acc.holdings)
    acc.sell('soxl', 3,  soxl)
    print(acc.holdings)
    acc.sell('soxl', 2,  soxl+20)
    print(acc.holdings)
    acc.buy('soxl', 3,  soxl, False)
    print(acc.get_holdings())
    print(acc.get_history())
    acc.view_balance_history()

