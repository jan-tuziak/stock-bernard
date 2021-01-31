import os
import csv
import logging
import requests
import pandas as pd
import numpy as np
import json
import datetime
import time

class DataHandler:
    def __init__(self, poly_key, csv_name, timeframes):
        self.timeframes = timeframes
        self.stocks = []
        self.df = pd.DataFrame()
        self.main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.america_csv = csv_name
        self.csv_path = os.path.join(self.main_dir, 'data' ,self.america_csv)
        self.poly_key = poly_key

    def _poly_url(self, stock, timeframe, from_date, to_date):
        return f'https://api.polygon.io/v2/aggs/ticker/{stock}/range/{timeframe["multiplier"]}/{timeframe["timespan"]}/{from_date}/{to_date}?unadjusted=true&sort=asc&limit=40000&apiKey={self.poly_key}'
    
    def _data_str(self, timeframe):
        return f"data{timeframe['multiplier']}{timeframe['timespan']}"
    
    def _sma_str(self, period):
        return f"sma{period}"
    
    def add_smas(self, timeframe, period):
        """Add list of SMA values to object's quotes list as "smaTIMEFRAMExPERIOD" dict element"""

        for t in self.timeframes:
            for idx, s in enumerate(self.stocks):
                for period in range(100, 901, 100)
                    c_idx = s[self.dh._data_str(timeframe)].columns.get_loc("c")
                    s[self.dh._data_str(timeframe)][self._sma_str(period)] = np.nan
                    s[self.dh._data_str(timeframe)][self._sma_str(period)] = s[self.dh._data_str(timeframe)].iloc[:,c_idx].rolling(window=period).mean()

    def get_stocks_from_csv(self, num_of_stocks):
        logging.info(f'Getting stocks from {self.america_csv}')
        df = pd.DataFrame()
        columns = ['Ticker', 'Exchange']
        df = pd.read_csv(self.csv_path, usecols=columns, nrows=num_of_stocks)
        df.rename(columns={'Ticker':'symbol', 'Exchange':'exchange'}, inplace = True)
        for idx, row in df.iterrows():
            self.stocks.append({"symbol":row["symbol"], "exchange":row["exchange"]})
        logging.info(f'Number of Stocks acquired: {len(self.stocks)}')
    
    def add_close_poly(self):
        logging.info(f'Acquiring data from Polygon.io')
        to_date = str(datetime.date.today())
        from_date = datetime.date.today() - datetime.timedelta(days=20)
        failed_stocks = []
        for idx, s in enumerate(self.stocks):
            try:
                for timeframe in self.timeframes:
                    #s[f"data{minut}min"] = np.nan
                    s[self._data_str(timeframe)] = np.nan
                    response = requests.get(self._poly_url(s["symbol"], timeframe, from_date, to_date))
                    data = json.loads(response.text)
                    if data["status"] == 'ERROR':
                        raise ValueError(f'Polygon API returned an error. API data: {data}')
                    temp_df = pd.DataFrame(data['results'])
                    for idx2,row2 in temp_df.iterrows():
                        temp_df.at[idx2, 'date_time'] = datetime.datetime.utcfromtimestamp(row2['t']/1000) - datetime.timedelta(hours=5) #.astimezone(dateutil.tz.gettz('US/Eastern'))#.strftime('%Y-%m-%d %H:%M:%S')
                    #remove ETH data
                    opening_hours = datetime.time(9, 30)
                    closing_hours = datetime.time(16, 00)
                    idx_rem = []
                    for idx3, row3 in temp_df.iterrows():
                        if row3['date_time'].time() >= opening_hours and row3['date_time'].time() < closing_hours: continue
                        idx_rem.append(idx3)
                    temp_df.drop(idx_rem, inplace=True)
                    temp_df.reset_index(inplace=True)
                    s[self._data_str(timeframe)] = temp_df
            except:
                failed_stocks.append(idx)
        # remove stocks that failed to get data
        if failed_stocks != []:
            for idx in sorted(failed_stocks, reverse=True):
                del self.stocks[idx]
        logging.info(f'Number of Stocks acquired: {len(self.stocks)}')
    
    def save_stocks_to_file(self):      
        stocks_copy = self.stocks.copy()
        for s in stocks_copy:
            for t in self.timeframes:
                temp = s[self._data_str(t)].to_dict(orient='records')[-1]
                temp["date_time"] = temp["date_time"].strftime('%Y-%m-%d %H:%M:%S')
                s[self._data_str(t)] = temp
        with open(self.stocks_filename, 'w') as fout:
            json.dump(stocks_copy, fout, indent=4)

if __name__ == "__main__":
    pass
    # pd.set_option('display.max_columns', None)
    # dh = DataHole(poly_key="3U413sHUAdFisFvcp6TReoTsEZ_GgpLp", av_key="E6H2MXTA1P7JD4II", csv_name="america_2021-01-09.csv")
    # dh.get_stocks_from_csv(1)
    # dh.add_close_poly()
    # print(dh.stocks)