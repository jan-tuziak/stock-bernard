import config

from scanf import scanf
import pprint
import os
import csv
import logging
import requests
import pandas as pd
import numpy as np
import json
import datetime
import time

from src. data_handler.stocks_finder.csv_stocks_finder import CSVStocksFinder
from src.data_handler.data_source.av_data_source import AVDataSource
from src.stocks_warehouse.json_warehouse import JsonWarehouse

class DataHandlerPoly:
    def __init__(self):
        logging.debug("Initializing Data Handler")
        self.stock_finder = CSVStocksFinder(config.csv_path)
        self.data_source = AVDataSource(config.av_key)
        self.warehouse - JsonWarehouse(config.json_path)
        self.stocks = []
        # self.stocks = []
        # self.main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        # self.csv_path = os.path.join(self.main_dir, 'data' ,config.stocks_csv)
        # self.ti = TechIndicators(key=config.av_key)

    def get_data(self):
        #Initialize Warehouse with stocks from CSV
        self.warehouse.init_from_symbols(self.stock_finder.get_top_stocks_by_daily_turnover(config.num_of_stocks_to_read))
        #Add 
        self.
        #Get and add sma values to stocks in warehouse
        for stck in self.warehouse.get_stocks_list:
            pass
        #Save warehouse to file

    def get_ingredients_from_criterias(self):
        pass

    # def _poly_url(self, stock, timeframe, from_date, to_date):
    #     return f'https://api.polygon.io/v2/aggs/ticker/{stock}/range/{timeframe["multiplier"]}/{timeframe["timespan"]}/{from_date}/{to_date}?unadjusted=true&sort=asc&limit=40000&apiKey={config.poly_key}'
    
    # def add_smas(self):
    #     """Add list of SMA values to object's quotes list as "smaTIMEFRAMExPERIOD" dict element"""
    #     for timeframe in config.timeframes:
    #         for idx, s in enumerate(self.stocks):
    #             for period in [30] + list(range(100, 901, 100)):
    #                 c_idx = s[config.data_str(timeframe)].columns.get_loc("c")
    #                 s[config.data_str(timeframe)][config.sma_str(period)] = np.nan
    #                 s[config.data_str(timeframe)][config.sma_str(period)] = s[config.data_str(timeframe)].iloc[:,c_idx].rolling(window=period).mean()

    # def get_stocks_from_csv(self):
    #     #logging.info(f'Getting stocks from {config.stocks_csv}')
    #     df = pd.DataFrame()
    #     columns = ['Ticker', 'Exchange']
    #     df = pd.read_csv(self.csv_path, usecols=columns, nrows=config.num_of_stocks_to_read)
    #     df.rename(columns={'Ticker':'symbol', 'Exchange':'exchange'}, inplace = True)
    #     for idx, row in df.iterrows():
    #         self.stocks.append({"symbol":row["symbol"], "exchange":row["exchange"]})
    #     logging.info(f'Number of Stocks read from csv: {len(self.stocks)}')
    #     del df
    
    # def add_close_poly(self):
    #     #logging.info(f'Acquiring data from Polygon.io')
    #     to_date = str(datetime.date.today())
    #     from_date = datetime.date.today() - datetime.timedelta(days=20)
    #     failed_stocks = []
    #     for idx, s in enumerate(self.stocks):
    #         try:
    #             for timeframe in config.timeframes:
    #                 #s[f"data{minut}min"] = np.nan
    #                 s[config.data_str(timeframe)] = np.nan
    #                 response = requests.get(self._poly_url(s["symbol"], timeframe, from_date, to_date))
    #                 data = json.loads(response.text)
    #                 if data["status"] == 'ERROR':
    #                     raise ValueError(f'Polygon API returned an error. API data: {data}')
    #                 temp_df = pd.DataFrame(data['results'])
    #                 for idx2,row2 in temp_df.iterrows():
    #                     #temp_df.at[idx2, 'date_time'] = datetime.datetime.utcfromtimestamp(row2['t']/1000) - datetime.timedelta(hours=5) #.astimezone(dateutil.tz.gettz('US/Eastern'))#.strftime('%Y-%m-%d %H:%M:%S')
    #                     temp_df.at[idx2, 'date_time'] = datetime.datetime.utcfromtimestamp(row2['t']/1000)
    #                 #remove ETH data
    #                 # opening_hours = datetime.time(9, 30)
    #                 # closing_hours = datetime.time(16, 00)
    #                 opening_hours = datetime.time(config.market_opening_hour[0], config.market_opening_hour[1])
    #                 closing_hours = datetime.time(config.market_closing_hour[0], config.market_closing_hour[1])
    #                 idx_rem = []
    #                 for idx3, row3 in temp_df.iterrows():
    #                     if row3['date_time'].time() >= opening_hours and row3['date_time'].time() < closing_hours: continue
    #                     idx_rem.append(idx3)
    #                 temp_df.drop(idx_rem, inplace=True)
    #                 temp_df.reset_index(inplace=True)
    #                 s[config.data_str(timeframe)] = temp_df
    #         except:
    #             failed_stocks.append(idx)
    #     # remove stocks that failed to get data
    #     if failed_stocks != []:
    #         for idx in sorted(failed_stocks, reverse=True):
    #             del self.stocks[idx]

    # def add_sma(self, symbol, time_period, interval):
    #     data, meta_data = self.ti.get_sma(symbol=symbol, interval=interval, time_period=time_period)
    #     data_l = list(data)
    #     data_l.sort(reverse=True)
    #     key=data_l[0]
    #     return float(data[key]['SMA'])

    # def get_data(self):
    #     smas = []
    #     for c in config.criterias_v2:
    #         temp = c.split()
    #         smas.append(temp[0], temp[2])

    #     pattern = 'sma%dx%s'
    #     for s in self.stocks:
    #         for sm in smas:
    #             time_period, interval = scanf(pattern, sm)
    #             self.add_sma(symbol=s, time_period=time_period, interval=interval)
            
    
    # def save_stocks_to_file(self):      
    #     stocks_copy = self.stocks.copy()
    #     for s in stocks_copy:
    #         for t in config.timeframes:
    #             temp = s[config.data_str(t)].to_dict(orient='records')[-1]
    #             temp["date_time"] = temp["date_time"].strftime('%Y-%m-%d %H:%M:%S')
    #             s[config.data_str(t)] = temp
    #     with open(config.stocks_filename, 'w') as fout:
    #         json.dump(stocks_copy, fout, indent=4)
    #     logging.info(f'Number of Stocks data acquired from Polygon.io and saved to file: {len(self.stocks)}')
    #     del stocks_copy

    # def clear_memory(self):
    #     self.stocks = []

if __name__ == "__main__":
    from alpha_vantage.techindicators import TechIndicators
    ti = TechIndicators(key=config.av_key)
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ti.get_sma(symbol='GOOGL', interval='daily', time_period=20)
    data_l = list(data)
    data_l.sort(reverse=True)
    key=data_l[0]
    pprint.pprint(float(data[key]['SMA']))