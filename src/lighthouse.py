import logging
import pprint
from datetime import datetime
import csv
import os
import time
import requests
import json

from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

class Lighthouse():
    def __init__(self, df, av_key):
        # if column "lighthouse" has value "false" it did not pass through lighthouse filter
        self.df = df
        self.col_name = "lighthouse"
        self.col_fail = "false"
        self.df[self.col_name] = ""
        self.symbols = []
        #self.quotes = stocks
        #self.stocks = stocks
        self.key = av_key
        self.ti = TechIndicators(key=self.key)
        self.ts = TimeSeries(key=self.key)
        self.lastAPICall = datetime.now()
        self.breakBetweenAPICalls = 2 #number of seconds to wait between API calls
    
    def filter_by_daily_turnover(self, min_turnover = 1000000):
        # stocks_to_remove = []
        # num_of_loops = len(self.quotes)
        # logging.info('Filtering Stocks by daily Turnover')
        # for idx in range(num_of_loops):
        #     logging.debug(f'Filtering Stocks by daily Turnover... {self.quotes[idx]["exchange"]}:{self.quotes[idx]["symbol"]} ({idx+1} out of {num_of_loops})')
        #     #check if turnover daily is big enough
        #     stock_turnover_daily = float(self.quotes[idx]['price']) * int(self.quotes[idx]['volume'])
        #     if stock_turnover_daily < min_turnover: stocks_to_remove.append(idx)
        # logging.debug(f'\r\nTurnover Filter - Stocks to remove: {stocks_to_remove}')
        # for i in sorted(stocks_to_remove, reverse=True):
        #     self.stocks.pop(i)
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
        sma_str = self._create_sma_str(interval, time_period)
        if sma_str not in list(self.df.columns):
            self.df[sma_str] = ""
            for idx, row in self.df.iterrows():
                if row[self.col_name] == self.col_fail: continue
                sma = self._get_sma(row['symbol'], interval, time_period)
                if sma == []:
                    self.df.at[idx, sma_str] = -1
                    row[self.col_name] = self.col_fail
                else:
                    self.df.at[idx, sma_str] = sma[0]
    
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
        for idx, row in self.df.iterrows():
            if row[self.col_name] == self.col_fail: continue
            if row[sma_str_hr] < row[sma_str_lr]:
                self.df.at[idx, self.col_name] = self.col_fail


    def _create_sma_str(self, interval, time_period):
        return f"sma{time_period}x{interval}"


    
    def create_tv_string(self):
        # tv_stocks = []
        # for s in self.quotes:
        #     #TradingView does not what 'NYSE ARCA' is. It recognizes those symbols as port of "AMEX" exchange
        #     if s['exchange'] == 'NYSE ARCA': 
        #         exch = 'AMEX'
        #     else:
        #         exch = s['exchange']
        #     #Compose the string
        #     tv_stocks.append(exch + ':' + s['symbol'])
        tv_stocks = []
        for idx, row in self.df.iterrows():
            #TradingView does not what 'NYSE ARCA' is. It recognizes those symbols as port of "AMEX" exchange
            if row[self.col_name] == self.col_fail: continue
            if row['exchange'] == 'NYSE ARCA': 
                exch = 'AMEX'
            else:
                exch = row['exchange']
            tv_stocks.append(exch + ':' + row['symbol'])
        logging.debug(f'TV String: {tv_stocks}')
        return ','.join(tv_stocks)


if __name__ == "__main__":
    pass
    # #logging.basicConfig(level=logging.DEBUG)
    # avf = Lighthouse()
    # avf.get_data()
    # avf.filter_by_daily_turnover(2000000)
    # avf.filter_greater_than_sma('15min',900)
    # print(avf.create_tv_string())
    # #pprint.pprint(avf.quotes)