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

from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

class Lighthouse():
    def __init__(self, stocks, av_key):
        # if column "lighthouse" has value "false" it did not pass through lighthouse filter
        self.col_name = "lighthouse"
        self.col_fail = "false"
        self.stocks = stocks
        for s in self.stocks:
            s[self.col_name] = ""
        #self.df[self.col_name] = ""
        self.symbols = []
        #self.quotes = stocks
        #self.stocks = stocks
        self.key = av_key
        self.ti = TechIndicators(key=self.key)
        self.ts = TimeSeries(key=self.key)
        self.lastAPICall = datetime.now()
        self.breakBetweenAPICalls = 2 #number of seconds to wait between API calls
    
    def filter_by_daily_turnover(self, min_turnover = 1000000):
        logging.info('Filtering Stocks by daily Turnover')
        self.df = self.df[self.df['volume'] > min_turnover]
        logging.info(f'Number of Stocks: {len(self.df)}')

    def _get_sma(self, stock, interval='15min', time_period=300):
        """
        time_period:  How many data points to average (default 20)
        interval:  time interval between two conscutive values,
                supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
                'weekly', 'monthly' (default 'daily')
        return: sma - list of sma values. First value is the newest SMA.
        """
        try:
            sma = self.ti.get_sma(stock, time_period=time_period, interval=interval)
        except:
            return []
        sma_data = sma[0]
        sma_metadata = sma[1]
        sma = []
        for key in sma_data:
            sma.append(float(sma_data[key]['SMA']))
        return sma
    
    def _add_sma(self, interval, time_period):
        """Add list of SMA values to object's quotes list as "smaPERIODxINTERVAL" dict element"""
        # sma_str = self._create_sma_str(interval, time_period)
        # if sma_str not in list(self.df.columns):
        #     self.df[sma_str] = ""
        #     for idx, row in self.df.iterrows():
        #         if row[self.col_name] == self.col_fail: continue
        #         sma = self._get_sma(row['symbol'], interval, time_period)
        #         if sma == []:
        #             self.df.at[idx, sma_str] = -1
        #             row[self.col_name] = self.col_fail
        #         else:
        #             self.df.at[idx, sma_str] = sma[0]
        if interval == '1min':
            for s in self.stocks:
                c_idx = s["data1min"].columns.get_loc("c")
                s["data1min"][f'sma{time_period}'] = np.nan
                s["data1min"][f'sma{time_period}'] = s["data1min"].iloc[:,c_idx].rolling(window=time_period).mean()
        if interval == '15min':
            for s in self.stocks:
                c_idx = s["data15min"].columns.get_loc("c")
                s["data1min"][f'sma{time_period}'] = np.nan
                s["data15min"][f'sma{time_period}'] = s["data15min"].iloc[:,c_idx].rolling(window=time_period).mean()
        #DEBUG 
        #time.sleep(13)

    
    def filter_greater_than_sma(self, interval='15min', time_period=300):
        """Filter out those stocks that are below given SMA"""
        self._add_sma(interval, time_period)
        #remove the stocks if sma is empty or sma is greater than close price
        sma_str = self._create_sma_str(interval, time_period)
        logging.info(f'Filtering Stocks by "close" greater than {sma_str}')
        for idx, row in self.df.iterrows():
            if row[self.col_name] == self.col_fail: continue
            if row["close"] < row[sma_str]:
                self.df.at[idx, self.col_name] = self.col_fail
        logging.info(f'Number of Stocks: {len(self.quotes)}')

    def filter_sma_greater_than_sma(self, x_interval, x_period, y_interval, y_period):
        """Filter through the stocks and leave the ones whose smaX is higher than smaY.
        For instance, smaX is sma300x15min, smaY is sma100x15min -> leave stocks where sma300x15min > sma100x15min"""
        self._add_sma(x_interval, x_period)
        self._add_sma(y_interval, y_period)
        #remove the stocks if sma is empty or sma is greater than close price
        sma_str_lr = self._create_sma_str(y_interval, y_period)
        sma_str_hr = self._create_sma_str(x_interval, x_period)
        logging.info(f'Filtering Stocks by {sma_str_hr} > {sma_str_lr}')
        #logging.info(self.df.head())
        # for idx, row in self.df.iterrows():
        #     if row[self.col_name] == self.col_fail: continue
        #     if row[sma_str_hr] < row[sma_str_lr]:
        #         self.df.at[idx, self.col_name] = self.col_fail
        for s in self.stocks:
            if s[self.col_name] == self.col_fail: continue
            if s[f"data{y_interval}"][f"sma{y_period}"].iloc[-1] < s[f"data{x_interval}"][f"sma{x_period}"].iloc[-1]:
                s[self.col_name] = self.col_fail 


    def _create_sma_str(self, interval, time_period):
        return f"sma{time_period}x{interval}"


    
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

    def save_stocks_to_file(self):
        stocks_copy = self.stocks.copy()
        for s in stocks_copy:
            temp = s["data15min"].to_dict(orient='records')[-1]
            temp["date_time"] = temp["date_time"].strftime('%Y-%m-%d %H:%M:%S')
            s["data15min"] = temp
            
            temp = s["data1min"].to_dict(orient='records')[-1]
            temp["date_time"] = temp["date_time"].strftime('%Y-%m-%d %H:%M:%S')
            s["data1min"] = temp
            
            # s["data15min"] = s["data15min"].to_dict(orient='records')[-1]
            # s["data1min"] = s["data1min"].to_dict(orient='records')[-1]
        with open('stocks.txt', 'w') as fout:
            json.dump(stocks_copy, fout, indent=4)


if __name__ == "__main__":
    pass
    # #logging.basicConfig(level=logging.DEBUG)
    # avf = Lighthouse()
    # avf.get_data()
    # avf.filter_by_daily_turnover(2000000)
    # avf.filter_greater_than_sma('15min',900)
    # print(avf.create_tv_string())
    # #pprint.pprint(avf.quotes)