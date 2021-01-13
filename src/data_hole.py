import os
import csv
import logging
import requests
import pandas as pd
import numpy as np

from alpha_vantage.timeseries import TimeSeries

class DataHole:
    def __init__(self, df, av_key, csv_name):
        self.df = df
        self.main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.america_csv = csv_name
        self.csv_path = os.path.join(self.main_dir, 'data' ,self.america_csv)
        self.av_key = av_key
    
    def get_from_csv(self, num_of_stocks):
        logging.info(f'Getting data from {self.america_csv}')
        columns = ['Ticker', 'Exchange']
        self.df = pd.read_csv(self.csv_path, usecols=columns, nrows=num_of_stocks)
        self.df.rename(columns={'Ticker':'symbol', 'Exchange':'exchange'}, inplace = True)
        logging.info(f'Number of Stocks acquired: {len(self.df.index)}')
    
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

    def add_volume(self):
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

if __name__ == "__main__":
    df = pd.DataFrame()
    dh = DataHole(df, av_key="E6H2MXTA1P7JD4II", csv_name="america_2021-01-09.csv")
    dh.get_from_av()
    dh.add_volume()
    print(dh.df.loc[dh.df['symbol'] == 'AACG'])
    print(dh.df.loc[dh.df['symbol'] == 'BC-P-C'])