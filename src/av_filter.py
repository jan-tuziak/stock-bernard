
import logging
import pprint

from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

class AVFilter():
    def __init__(self, stocks):
        self.stocks = stocks
        # Example of stock entry in stocks list: 
        # {'assetType': 'Stock', 'delistingDate': 'null', 'exchange': 'NYSE', 'ipoDate': '1999-11-18', 'name': 'Agilent Technologies Inc', 'status': 'Active', 'symbol': 'A'}
        self.ti = TechIndicators(key='E6H2MXTA1P7JD4II')
        self.ts = TimeSeries(key='E6H2MXTA1P7JD4II')
        self.quotes = []
        self.get_global_quotes()
    
    def get_sma(self, stock, interval='15min', time_period=300):
        """
        time_period:  How many data points to average (default 20)
        interval:  time interval between two conscutive values,
                supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
                'weekly', 'monthly' (default 'daily')
        return: sma - list of sma values. First value is the newest SMA.
        """
        sma = self.ti.get_sma(stock, time_period=time_period, interval=interval)
        sma_data = sma[0]
        sma_metadata = sma[1]
        sma = []
        for key in sma_data:
            sma.append(float(sma_data[key]['SMA']))
        return sma
    
    def filter_greater_than_sma(self, interval='15min', time_period=300):
        filtered = []
        sma_str = f"sma{time_period}x{interval}"
        if sma_str not in self.quotes[0]:
            for i in range(len(self.quotes)):
                symbol = self.quotes[i]['01. symbol']
                sma = self.get_sma(symbol, interval, time_period)
                self.quotes[i][sma_str] = sma
        #TODO add quote removal based on sma. If sma is an empty list remove that quote
    
    def get_global_quotes(self):
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
        for stock in self.stocks:
            quote = self.ts.get_quote_endpoint(stock['symbol'])[0]
            quote['exchange'] = stock['exchange']
            self.quotes.append(quote)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    avf = AVFilter([{'assetType': 'Stock', 'delistingDate': 'null', 'exchange': 'NYSE', 'ipoDate': '1999-11-18', 'name': 'Agilent Technologies Inc', 'status': 'Active', 'symbol': 'AA'}])
    avf.filter_greater_than_sma('15min',900)
    #pprint.pprint(avf.quotes)