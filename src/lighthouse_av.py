
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

class LighthouseAV():
    def __init__(self):
        # Example of stock entry in stocks list: 
        # {'assetType': 'Stock', 'delistingDate': 'null', 'exchange': 'NYSE', 'ipoDate': '1999-11-18', 'name': 'Agilent Technologies Inc', 'status': 'Active', 'symbol': 'A'}
        self.symbols = []
        self.quotes = []
        self.key = 'E6H2MXTA1P7JD4II'
        self.ti = TechIndicators(key=self.key)
        self.ts = TimeSeries(key=self.key)
        #self.get_global_quotes()
        self.lastAPICall = datetime.now()
        self.breakBetweenAPICalls = 2 #number of seconds to wait between API calls

    def get_data(self):
        self._get_symbols()
        self._get_global_quotes()

    def _get_symbols(self):
        #Get all stocks and save it into list of directories
        logging.info('Acquiring list of Symbols')
        #success, response = self._execute_req('list', {"state":"active"})
        query = f"https://www.alphavantage.co/query?function=LISTING_STATUS&state=active&apikey={self.key}"
        response = requests.get(query)
        csv_file = 'MoneySpyderStocksTemp.csv' 
        with open(csv_file, 'w') as f:
            f.write(response.text)

        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            self.stocks = list(reader)

        os.remove(csv_file)

        #if number of received stocks is smaller than 2000 than it means something is wrong
        if len(self.stocks) < 2000: raise ValueError('Received too few stocks. Check if Alpha Vantage is operating correctly.')

        logging.info('Removing non-Stock assests')
        stocks_to_remove = []
        
        for idx in range(len(self.stocks)):
            #remove any entries that 'assetType' is not 'Stocks'
            if self.stocks[idx]['assetType'] != 'Stock': stocks_to_remove.append(idx)
            #Fix wierd bug - Stock "BC-P-C" is saved as "BC/PC" for some reason. Rewrite the symbol if "BC/PC" is found
            if self.stocks[idx]['symbol'] == "BC/PC": self.stocks[idx]['symbol'] = "BC-P-C"
        logging.debug(f'Stocks Only - Stocks to remove: {stocks_to_remove}')
        for i in sorted(stocks_to_remove, reverse=True):
            self.stocks.pop(i)  

        #TODO remove this line
        #self.stocks = self.stocks[0:20]

        logging.info(f'Number of Stocks acquired: {len(self.stocks)}')
    
    def filter_by_daily_turnover(self, min_turnover = 1000000):
        stocks_to_remove = []
        num_of_loops = len(self.quotes)
        logging.info('Filtering Stocks by daily Turnover')
        for idx in range(num_of_loops):
            logging.debug(f'Filtering Stocks by daily Turnover... {self.quotes[idx]["exchange"]}:{self.quotes[idx]["01. symbol"]} ({idx+1} out of {num_of_loops})')
            #check if turnover daily is big enough
            stock_turnover_daily = float(self.quotes[idx]['05. price']) * int(self.quotes[idx]['06. volume'])
            if stock_turnover_daily < min_turnover: stocks_to_remove.append(idx)
        logging.debug(f'\r\nTurnover Filter - Stocks to remove: {stocks_to_remove}')
        for i in sorted(stocks_to_remove, reverse=True):
            self.stocks.pop(i)
        logging.info(f'Number of Stocks: {len(self.stocks)}')

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
        if sma_str not in self.quotes[0]:
            for i in range(len(self.quotes)):
                symbol = self.quotes[i]['01. symbol']
                sma = self._get_sma(symbol, interval, time_period)
                self.quotes[i][sma_str] = sma
    
    def filter_greater_than_sma(self, interval='15min', time_period=300):
        """Filter out those stocks that are below given SMA"""
        self._add_sma(interval, time_period)
        #remove the stocks if sma is empty or sma is greater than close price
        sma_str = self._create_sma_str(interval, time_period)
        logging.info(f'Filtering Stocks by SMA greater than {sma_str}')
        stocks_remove = []
        for idx in range(len(self.quotes)):
            if (self.quotes[idx][sma_str] == []) or (self.quotes[idx][sma_str][0] > self.quotes[idx]['05. price']):
                stocks_remove.append(idx)
                continue
        if stocks_remove != []:
            for sr in reversed(stocks_remove):
                self.quotes.pop(sr)
        logging.info(f'Number of Stocks: {len(self.quotes)}')

    def _create_sma_str(self, interval, time_period):
        return f"sma{time_period}x{interval}"

    def _get_global_quotes(self):
        """
        Get global quote from AV and add exchange
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
                "exchange": "NYSE"
            }
        """
        quotes_to_remove = []
        for i in range(len(self.stocks)):
            quote = self.ts.get_quote_endpoint(self.stocks[i]['symbol'])[0]
            # if something goes wrong when handling the quote remove it
            try:
                quote['exchange'] = self.stocks[i]['exchange']
                quote['05. price'] = float(quote['05. price'])
            except:
                quotes_to_remove.append(i)
            self.quotes.append(quote)
        if quotes_to_remove != []:
            for i in reversed(quotes_to_remove):
                self.quotes.pop(i)
    
    def create_tv_string(self):
        tv_stocks = []
        for s in self.quotes:
            #TradingView does not what 'NYSE ARCA' is. It recognizes those symbols as port of "AMEX" exchange
            if s['exchange'] == 'NYSE ARCA': 
                exch = 'AMEX'
            else:
                exch = s['exchange']
            #Compose the string
            tv_stocks.append(exch + ':' + s['01. symbol'])
        logging.debug(f'TV String: {tv_stocks}')
        return ','.join(tv_stocks)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    avf = LighthouseAV()
    avf.get_data()
    avf.filter_by_daily_turnover(2000000)
    avf.filter_greater_than_sma('15min',900)
    print(avf.create_tv_string())
    #pprint.pprint(avf.quotes)