import logging
import pprint
from datetime import datetime
import csv
import os
import time
import requests
import json
import numpy as np
import pandas as pd

class Lighthouse():
    def __init__(self, stocks_filename):
        # if column "lighthouse" has value "false" it did not pass through lighthouse filter
        self.dh = dh
        self.col_name = "lighthouse"
        self.col_fail = "false"
        #self.stocks = dh.stocks
        self.stocks = []
        for s in self.stocks:
            s[self.col_name] = ""
        self.symbols = []
        self.stocks_filename = stocks_filename
    
    def load_stocks_from_file(self):
        self.stocks = json.loads(self.stocks_filename)

    # def _add_sma(self, timeframe, period):
    #     """Add list of SMA values to object's quotes list as "smaTIMEFRAMExPERIOD" dict element"""
    #     for s in self.stocks:
    #         c_idx = s[self.dh._data_str(timeframe)].columns.get_loc("c")
    #         s[self.dh._data_str(timeframe)][self._sma_str(period)] = np.nan
    #         s[self.dh._data_str(timeframe)][self._sma_str(period)] = s[self.dh._data_str(timeframe)].iloc[:,c_idx].rolling(window=period).mean()

    def filter_sma_greater_than_sma(self, x_timeframe, x_period, y_timeframe, y_period):
        """Filter through the stocks and leave the ones whose smaX is higher than smaY.
        For instance, smaX is sma300x15min, smaY is sma100x15min -> leave stocks where sma300x15min > sma100x15min"""
        # self._add_sma(x_timeframe, x_period)
        # self._add_sma(y_timeframe, y_period)
        sma_str_lr = f"sma{y_period}x{y_timeframe['multiplier']}{y_timeframe['timespan']}"
        sma_str_hr = f"sma{x_period}x{x_timeframe['multiplier']}{x_timeframe['timespan']}"
        logging.info(f'Filtering Stocks by {sma_str_hr} > {sma_str_lr}')
        for s in self.stocks:
            if s[self.col_name] == self.col_fail: continue
            elif s[self.dh._data_str(y_timeframe)][self._sma_str(y_period)].iloc[-1] > s[self.dh._data_str(x_timeframe)][self._sma_str(x_period)].iloc[-1]:
                s[self.col_name] = self.col_fail 


    def _sma_str(self, period):
        return f"sma{period}"
    
    def create_tv_string(self):
        tv_stocks = []
        for s in self.stocks:
            #TradingView does not what 'NYSE ARCA' is. It recognizes those symbols as port of "AMEX" exchange
            if s[self.col_name] == self.col_fail: continue
            if s['exchange'] == 'NYSE ARCA': 
                exch = 'AMEX'
            else:
                exch = s['exchange']
            tv_stocks.append(exch + ':' + s['symbol'])
        logging.debug(f'TV String: {tv_stocks}')
        return ','.join(tv_stocks)

    # def save_stocks_to_file(self):      
    #     stocks_copy = self.stocks.copy()
    #     for s in stocks_copy:
    #         temp = s["data15minute"].to_dict(orient='records')[-1]
    #         temp["date_time"] = temp["date_time"].strftime('%Y-%m-%d %H:%M:%S')
    #         s["data15minute"] = temp
            
    #         temp = s["data1minute"].to_dict(orient='records')[-1]
    #         temp["date_time"] = temp["date_time"].strftime('%Y-%m-%d %H:%M:%S')
    #         s["data1minute"] = temp
    #     with open(self.stocks_filename, 'w') as fout:
    #         json.dump(stocks_copy, fout, indent=4)


if __name__ == "__main__":
    pass
    # #logging.basicConfig(level=logging.DEBUG)
    # avf = Lighthouse()
    # avf.get_data()
    # avf.filter_by_daily_turnover(2000000)
    # avf.filter_greater_than_sma('15min',900)
    # print(avf.create_tv_string())
    # #pprint.pprint(avf.quotes)