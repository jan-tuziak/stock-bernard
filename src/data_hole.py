import os
import csv
import logging
import requests
import pandas as pd
import numpy as np
import json
import datetime

from alpha_vantage.timeseries import TimeSeries

class DataHole:
    def __init__(self, av_key, poly_key, csv_name):
        self.stocks = []
        self.df = pd.DataFrame()
        self.main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.america_csv = csv_name
        self.csv_path = os.path.join(self.main_dir, 'data' ,self.america_csv)
        self.av_key = av_key
        self.poly_key = poly_key

    def poly_url(self, stock, minutes, from_date, to_date):
        return f'https://api.polygon.io/v2/aggs/ticker/{stock}/range/{minutes}/minute/{from_date}/{to_date}?unadjusted=true&sort=asc&limit=40000&apiKey={self.poly_key}'
    
    def get_stocks_from_csv(self, num_of_stocks):
        logging.info(f'Getting data from {self.america_csv}')
        df = pd.DataFrame()
        columns = ['Ticker', 'Exchange']
        # self.df = pd.read_csv(self.csv_path, usecols=columns, nrows=num_of_stocks)
        # self.df.rename(columns={'Ticker':'symbol', 'Exchange':'exchange'}, inplace = True)
        # logging.info(f'Number of Stocks acquired: {len(self.df.index)}')
        df = pd.read_csv(self.csv_path, usecols=columns, nrows=num_of_stocks)
        df.rename(columns={'Ticker':'symbol', 'Exchange':'exchange'}, inplace = True)
        for idx, row in df.iterrows():
            self.stocks.append({"symbol":row["symbol"], "exchange":row["exchange"]})
        logging.info(f'Number of Stocks acquired: {len(self.stocks)}')
    
    def get_from_av(self):
        logging.info(f'Getting data from Alpha Vantage')
        query = f"https://www.alphavantage.co/query?function=LISTING_STATUS&state=active&apikey={self.av_key}"
        response = requests.get(query)
        csv_file = 'MoneySpyderStocksTemp.csv' 
        with open(csv_file, 'w') as f:
            f.write(response.text)

        columns = ['symbol', 'name', 'exchange', 'assetType']
        self.df = pd.read_csv(csv_file, usecols=columns)
        
        os.remove(csv_file)

        #if number of received stocks is smaller than 2000 than it means something is wrong
        if len(self.df) < 2000: raise ValueError('Received too few stocks. Check if Alpha Vantage is operating correctly.')

        #leave only Stocks
        self.df = self.df[self.df['assetType'] == 'Stock']

        logging.info(f'Number of Stocks acquired: {len(self.df)}')

    def add_volume_and_close_av(self):
        """
        Get global quote from AV and insert volume and close to DF
        Example of Quote:
            {
                "01. symbol": "IBM",
                "02. open": "124.2200",
                "03. high": "126.0300",
                "04. low": "123.9900",
                "05. price": "125.8800",
                "06. volume": "3574696",
                "07. latest trading day": "2020-12-31",
                "08. previous close": "124.3400",
                "09. change": "1.5400",
                "10. change percent": "1.2385%",
            }
        """
        ts = TimeSeries(key=self.av_key)
        for idx, row in self.df.iterrows():
            try:
                quote = ts.get_quote_endpoint(row['symbol'])[0]
                vol = quote["06. volume"]
                close = quote["05. price"]
            except:
                vol = np.nan
                close = np.nan
            self.df.at[idx, 'volume'] = vol
            self.df.at[idx, 'close'] = close

    def get_symbol_index(self, symbol):
        return self.df[self.df['symbol'] == symbol].index.values.astype(int)[0]
    
    def add_close_poly(self):
        to_date = str(datetime.date.today())
        from_date = datetime.date.today() - datetime.timedelta(days=20) 
        for s in self.stocks:
            for minut in [1, 15]:
                s[f"data{minut}min"] = np.nan
                #s[f"data{minut}min"] = s[f"data{minut}min"].astype(object)
                #get data and add date_time columne
                response = requests.get(self.poly_url(s["symbol"], minut, from_date, to_date))
                data = json.loads(response.text)
                if data["status"] == 'ERROR':
                    raise ValueError(f'Polygon API returned an error. API data: {data}')
                temp_df = pd.DataFrame(data['results'])
                for idx2,row2 in temp_df.iterrows():
                    temp_df.at[idx2, 'date_time'] = datetime.datetime.utcfromtimestamp(row2['t']/1000) - datetime.timedelta(hours=5) #.astimezone(dateutil.tz.gettz('US/Eastern'))#.strftime('%Y-%m-%d %H:%M:%S')
                #remove ETH data
                opening_hours = datetime.time(9, 30)
                closing_hours = datetime.time(16, 00)
                #logging.info(f'Amout of all data: {len(temp_df)}')
                idx_rem = []
                for idx3, row3 in temp_df.iterrows():
                    if row3['date_time'].time() >= opening_hours and row3['date_time'].time() <= closing_hours: continue
                    idx_rem.append(idx3)
                temp_df.drop(idx_rem, inplace=True)
                temp_df.reset_index(inplace=True)
                s[f"data{minut}min"] = temp_df

        logging.info(f'Amout of data: {len(self.stocks)}')

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    dh = DataHole(poly_key="3U413sHUAdFisFvcp6TReoTsEZ_GgpLp", av_key="E6H2MXTA1P7JD4II", csv_name="america_2021-01-09.csv")
    dh.get_stocks_from_csv(1)
    dh.add_close_poly()
    #print(dh.df.columns)
    # idx = dh.get_symbol_index("AAPL")
    # print(dh.df["data1min"][idx]["c"])
    # print(dh.df["data15min"][idx]["c"])
    #print(dh.df[(dh.df["symbol"] == 'AAPL')]["data1min"]["v"])
    print(dh.stocks)