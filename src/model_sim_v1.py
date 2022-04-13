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

class TraderV1(object):

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


    def get_model(self, path):
        # read in saved model from file
        self.model = None
        return self.model

    def get_preds(self, symbols, data, model=None):
        if model is None:
            model = self.model
        predictions = []
        for symbol in symbols:
            predictions.append(model(data[sym]))
        return predictions

    def get_action(self):
        # decide to buy, sell, hold
        return 0

    def execute_action(self):
        # exectue in account object
        return 0



