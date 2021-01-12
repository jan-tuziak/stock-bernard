import os
import csv
import logging
import requests
import pandas as pd

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
        # with open(self.csv_path, "r") as f:
        #     reader = csv.DictReader(f)
        #     self.stocks = list(reader)[:num_of_stocks]
        #     #rename keys
        #     for s in self.stocks:
        #         s['symbol'] = s.pop('Ticker')
        #         s['price'] = s.pop('Last')
        #         s['volume'] = s.pop('Volume')
        #         s['exchange'] = s.pop('Exchange')
        # logging.info(f'Number of Stocks acquired: {len(self.stocks)}')
        # return self.stocks
        columns = ['Ticker', 'Exchange']
        self.df = pd.read_csv(self.csv_path, usecols=columns, nrows=num_of_stocks)
        self.df.rename(columns={'Ticker':'symbol', 'Exchange':'exchange'}, inplace = True)
        logging.info(f'Number of Stocks acquired: {len(self.df.index)}')
    
    def get_from_av(self):
        logging.info(f'Getting data from Alpha Vantage')
        #success, response = self._execute_req('list', {"state":"active"})
        query = f"https://www.alphavantage.co/query?function=LISTING_STATUS&state=active&apikey={self.av_key}"
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

        stocks_to_remove = []
        
        for idx in range(len(self.stocks)):
            #remove any entries that 'assetType' is not 'Stocks'
            if self.stocks[idx]['assetType'] != 'Stock': stocks_to_remove.append(idx)
            #Fix wierd bug - Stock "BC-P-C" is saved as "BC/PC" for some reason. Rewrite the symbol if "BC/PC" is found
            if self.stocks[idx]['symbol'] == "BC/PC": self.stocks[idx]['symbol'] = "BC-P-C"
        logging.debug(f'Stocks Only - Stocks to remove: {stocks_to_remove}')
        for i in sorted(stocks_to_remove, reverse=True):
            self.stocks.pop(i)  

        logging.info(f'Number of Stocks acquired: {len(self.stocks)}')
        self._get_global_quotes()
        return self.stocks

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
        ts = TimeSeries(key=self.av_key)
        quotes = []
        quotes_to_remove = []
        for i in range(len(self.stocks)):
            quote = ts.get_quote_endpoint(self.stocks[i]['symbol'])[0]
            # if something goes wrong when handling the quote remove it
            try:
                quote['exchange'] = self.stocks[i]['exchange']
                quote['price'] = float(quote['05. price'])
                quote.pop('05. price')
            except:
                quotes_to_remove.append(i)
            quotes.append(quote)
        if quotes_to_remove != []:
            for i in reversed(quotes_to_remove):
                quotes.pop(i)
        self.stocks = quotes

if __name__ == "__main__":
    pass
    #/home/jan/Money-Spyder/data/america_2021-01-09.csv