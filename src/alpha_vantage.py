import requests
import os 
import csv
import json
from datetime import datetime
import time
import logging

# Example Qyery - https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=compact&apikey=B451TTOLQ2VOY99L

#TODO finish implementing filter FilterStocksByDailyTurnover

class AlphaVantageCustomScreener():
    def __init__(self, debug=False, ):
        self.debug = debug
        self.functions = {
            'list': 'LISTING_STATUS',
            '1min-ly': 'TIME_SERIES_INTRADAY&interval=1min',
            'hourly': 'TIME_SERIES_INTRADAY&interval=60min',
            'daily': 'TIME_SERIES_DAILY',
            'weekly': 'TIME_SERIES_WEEKLY'
        }
        self.site = 'www.alphavantage.co'
        self.key = 'B451TTOLQ2VOY99L'
        self.query_format =  'https://%s/query?function=%s%s'
        self.stocks = []
        self.lastAPICall = datetime.now()
        self.breakBetweenAPICalls = 12 #number of seconds to wait between API calls

    def SearchForStocks(self):
        self.PopulateStocks()
        self.FilterStocksByDailyTurnover(2000000)

    def PopulateStocks(self):
        #Get all stocks and save it into list of directories
        response = self._executeRequest('list')
        csv_file = 'stocks.csv' 
        with open(csv_file, 'w') as f:
            f.write(response.text)

        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            self.stocks = list(reader)

        os.remove(csv_file)

        #if number of received stocks is smaller than 2000 than it means something is wrong
        if len(self.stocks) < 2000: raise ValueError('Received too few stocks. Check if Alpha Vantage is operating correctly.')

        #remove any entries that 'assetType' is not 'Stocks'
        stocks_to_remove = []
        for idx in range(len(self.stocks)):
            if self.stocks[idx]['assetType'] != 'Stock': stocks_to_remove.append(idx)
        logging.debug(f'Stocks Only - Stocks to remove: {stocks_to_remove}')
        for i in sorted(stocks_to_remove, reverse=True):
            self.stocks.pop(i)

        #if debug is true remove everything except for first 10 stocks
        if self.debug:
            temp = self.stocks.copy()
            self.stocks.clear()
            for x in range(10):
                self.stocks.append(temp[x])

    def FilterStocksByDailyTurnover(self, minTurnover = 1000000):
        stocks_to_remove = []
        for idx in range(len(self.stocks)):
            newest_time_data = self._getStocksNewestTimeData('daily', self.stocks[idx]['symbol'])
            stock_turnover_daily = float(newest_time_data['4. close']) * int(newest_time_data['5. volume'])
            if stock_turnover_daily < minTurnover: stocks_to_remove.append(idx)
        logging.debug(f'Turnover Filter - Stocks to remove: {stocks_to_remove}')
        for i in sorted(stocks_to_remove, reverse=True):
            self.stocks.pop(i)

    def PrintToTradingViewList(self):
        tv_stocks = []
        for s in self.stocks:
            tv_stocks.append(s['exchange'] + ':' + s['symbol'])
        logging.debug(f'TV String: {tv_stocks}')
        return ','.join(tv_stocks)

    def _getStocksNewestTimeData(self,function, symbol):
        args = {
            'symbol':       symbol,
            'outputsize':   'compact'
        }
        response = self._executeRequest(function, args)
        #logging.debug(f'Response.Text: {response.text}')
        all_data = json.loads(response.text)
        time_data = all_data[list(all_data.keys())[1]]
        newest_time_data = time_data[list(time_data.keys())[0]]
        return newest_time_data

    def _executeRequest(self, function, args={}):
        #calculate if enough amount of time has passed since last API call. If not - wait
        time_to_wait =  self.breakBetweenAPICalls - (datetime.now() - self.lastAPICall).total_seconds()
        logging.debug(f'Time to wait: {time_to_wait}s')
        if time_to_wait > 0: time.sleep(time_to_wait)
        #add arguments
        args['apikey'] = self.key
        arguments = ''
        for key in args:
            arguments += f'&{key}={args[key]}'
        #format query string
        query = self.query_format % (self.site, self.functions[function], arguments)
        logging.debug(f'Query: {query}')
        #set last API call and execute the API call
        self.lastAPICall = datetime.now()
        return requests.get(query)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    av = AlphaVantageCustomScreener(debug=True)
    print(av.PrintToTradingViewList())


    