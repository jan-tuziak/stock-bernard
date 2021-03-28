import config
import logging

# import pprint
# from datetime import datetime
# import csv
# import os
# import time
# import requests
# import json
# import numpy as np
# import pandas as pd

from src.stocks_warehouse.json_warehouse import JsonWarehouse
from src.criterias.criterias_handler import CriterasHandler

class Lighthouse():
    def __init__(self):
        self._warehouse = JsonWarehouse(config.json_path)
        self._warehouse.deserialize()
        self._crits_handler = CriterasHandler(self._warehouse)
        # # if column "lighthouse" has value "false" it did not pass through lighthouse filter
        # self.col_name = "lighthouse"
        # self.col_fail = "false"
        # self.stocks = []

    
    def get_lighthouse_stocks(self):
        self._crits_handler.check_against_crits()
        return self._warehouse.get_stocks_for_tv()

    # def load_stocks_from_file(self):
    #     # Read stocks data from file
    #     with open(config.stocks_filename) as json_file:
    #         self.stocks = json.load(json_file)
    #     # Add "Lighthouse" key to stocks
    #     for s in self.stocks:
    #         s[self.col_name] = ""


    # #def filter_sma_greater_than_sma(self, x_timeframe, x_period, y_timeframe, y_period):
    # def filter_sma_greater_than_sma(self, criteria):
    #     """Filter through the stocks and leave the ones whose smaX is higher than smaY.
    #     For instance, smaX is sma300x15min, smaY is sma100x15min -> leave stocks where sma300x15min > sma100x15min"""
    #     # sma_str_lr = f"sma{y_period}x{y_timeframe['multiplier']}{y_timeframe['timespan']}"
    #     # sma_str_hr = f"sma{x_period}x{x_timeframe['multiplier']}{x_timeframe['timespan']}"
    #     # logging.info(f'Filtering Stocks by {sma_str_hr} > {sma_str_lr}')
    #     logging.debug(f"Filtering Stocks by {config.criteria_str(criteria)}")
    #     for s in self.stocks:
    #         if s[self.col_name] == self.col_fail: continue
    #         elif s[config.data_str(criteria['y_timeframe'])][config.sma_str(criteria['y_period'])] > s[config.data_str(criteria['x_timeframe'])][config.sma_str(criteria['x_period'])]:
    #             s[self.col_name] = self.col_fail 
    
    # def create_tv_string(self):
    #     tv_stocks = []
    #     for s in self.stocks:
    #         #TradingView does not what 'NYSE ARCA' is. It recognizes those symbols as port of "AMEX" exchange
    #         if s[self.col_name] == self.col_fail: continue
    #         if s['exchange'] == 'NYSE ARCA': 
    #             exch = 'AMEX'
    #         else:
    #             exch = s['exchange']
    #         tv_stocks.append(exch + ':' + s['symbol'])
    #     stocks_to_observe = ','.join(tv_stocks)
    #     #logging.debug(f'TV String: {tv_stocks}')
    #     logging.debug(f'Stocks to observe: {stocks_to_observe}')
    #     return stocks_to_observe

if __name__ == "__main__":
    pass
    # #logging.basicConfig(level=logging.DEBUG)
    # avf = Lighthouse()
    # avf.get_data()
    # avf.filter_by_daily_turnover(2000000)
    # avf.filter_greater_than_sma('15min',900)
    # print(avf.create_tv_string())
    # #pprint.pprint(avf.quotes)