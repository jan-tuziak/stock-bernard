import requests
import os 
import csv
import json
from datetime import datetime
import time
import logging

# Example Qyery - https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=compact&apikey=B451TTOLQ2VOY99L

#TODO implement try/except that removes symbols from self.stocks if data received from API for that given symbol is "Error Message"

class AlphaVantageCustomScreener():
    def __init__(self, debug=False, printToConsole=False):
        self.debug = debug
        self.printToConsole = printToConsole
        self.functions = {
            'list': 'LISTING_STATUS',
            '1min-ly': 'TIME_SERIES_INTRADAY&interval=1min',
            'hourly': 'TIME_SERIES_INTRADAY&interval=60min',
            'daily': 'TIME_SERIES_DAILY',
            'weekly': 'TIME_SERIES_WEEKLY'
        }
        self.site = 'www.alphavantage.co'
        self.key = 'E6H2MXTA1P7JD4II'
        self.query_format =  'https://%s/query?function=%s%s'
        self.stocks = []
        self.lastAPICall = datetime.now()
        self.breakBetweenAPICalls = 2 #number of seconds to wait between API calls

    def SearchForStocks(self):
        self.PopulateStocks()
        self.FilterStocksByDailyTurnover(2000000)

    def PopulateStocks(self):
        #Get all stocks and save it into list of directories
        self.print('Acquiring list of Symbols... ')
        success, response = self._executeRequest('list', {"state":"active"})
        csv_file = 'MoneySpyderStocksTemp.csv' 
        with open(csv_file, 'w') as f:
            f.write(response.text)

        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            self.stocks = list(reader)

        os.remove(csv_file)

        #if number of received stocks is smaller than 2000 than it means something is wrong
        if len(self.stocks) < 2000: raise ValueError('Received too few stocks. Check if Alpha Vantage is operating correctly.')

        self.print('Removing non-Stock assests... ')
        stocks_to_remove = []
        
        for idx in range(len(self.stocks)):
            #remove any entries that 'assetType' is not 'Stocks'
            if self.stocks[idx]['assetType'] != 'Stock': stocks_to_remove.append(idx)
            #also removes these symbols, because for some reason Alpha Vantage does not work with them
            #if self.stocks[idx]['symbol'] in ["CLNY-P-B-CL", "CLNY-P-E-CL","HZAC-U"]: stocks_to_remove.append(idx)
            #Fix wierd bug - Stock "BC-P-C" is saved as "BC/PC" for some reason. Rewrite the symbol if "BC/PC" is found
            if self.stocks[idx]['symbol'] == "BC/PC": self.stocks[idx]['symbol'] = "BC-P-C"
        logging.debug(f'Stocks Only - Stocks to remove: {stocks_to_remove}')
        for i in sorted(stocks_to_remove, reverse=True):
            self.stocks.pop(i)
        self.print(f'Number of Stocks acquired: {len(self.stocks)}')

        #if debug is true remove everything except for first 10 stocks
        if self.debug:
            temp = self.stocks.copy()
            self.stocks.clear()
            for x in range(10):
                self.stocks.append(temp[x])
            self.stocks = temp
            self.print(f'Debug Mode is on. Adjusting the Number of Stocks acquired to 10')

    def FilterStocksByDailyTurnover(self, minTurnover = 1000000):
        stocks_to_remove = []
        num_of_loops = len(self.stocks)
        for idx in range(num_of_loops):
            self.print(f'Filtering Stocks by daily Turnover... {self.stocks[idx]["exchange"]}:{self.stocks[idx]["symbol"]} ({idx+1} out of {num_of_loops})      ', end='\r')
            success, newest_time_data = self._getStocksNewestTimeData('daily', self.stocks[idx]['symbol'])
            if success:
                #check if turnover daily is big enough
                stock_turnover_daily = float(newest_time_data['4. close']) * int(newest_time_data['5. volume'])
                if stock_turnover_daily < minTurnover: stocks_to_remove.append(idx)
            else:
                #api call with that symbol failed. remove the symbol
                stocks_to_remove.append(idx)
                self.print(f'\r\nRemoved Stock: {self.stocks[idx]["exchange"]}:{self.stocks[idx]["symbol"]}')
        logging.debug(f'\r\nTurnover Filter - Stocks to remove: {stocks_to_remove}')
        for i in sorted(stocks_to_remove, reverse=True):
            self.stocks.pop(i)
        self.print(f'Filtering Stocks by daily Turnover... {num_of_loops} out of {num_of_loops}')
        self.print(f'Number of Stocks left after Daily Turnover Filter: {len(self.stocks)}')

    def PrintToTradingViewList(self):
        tv_stocks = []
        for s in self.stocks:
            #TradingView does not what 'NYSE ARCA' is. It recognizes those symbols as port of "AMEX" exchange
            if s['exchange'] == 'NYSE ARCA': 
                exch = 'AMEX'
            else:
                exch = s['exchange']
            #Compose the string
            tv_stocks.append(exch + ':' + s['symbol'])
        logging.debug(f'TV String: {tv_stocks}')
        return ','.join(tv_stocks)

    def _getStocksNewestTimeData(self,function, symbol):
        args = {
            'symbol':       symbol,
            'outputsize':   'compact'
        }
        success, response = self._executeRequest(function, args)
        #logging.debug(f'Response.Text: {response.text}')
        newest_time_data = []
        if success:
            all_data = json.loads(response.text)
            logging.debug(all_data)
            time_data = all_data[list(all_data.keys())[1]]
            newest_time_data = time_data[list(time_data.keys())[0]]
        return success, newest_time_data

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
        response = requests.get(query)
        try:
            #if API is list symbols then just return the response
            if function == 'list': return True, response
            #otherwise check for error messages 
            api_data = json.loads(response.text)
            first_key = list(api_data.keys())[0]
            # return True or False for success and response
            success = True
            if first_key == 'Error Message': success = False
        except:
            success = False
        return success, response

    def print(self, msg, end='\r\n'):
        if self.printToConsole: print(f'AlphaVantageCustomScreener::{msg}', end=end)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    av = AlphaVantageCustomScreener(debug=True, printToConsole=True)
    av.SearchForStocks()
    print(av.PrintToTradingViewList())


    