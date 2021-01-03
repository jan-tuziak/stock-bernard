# Example of stock entry in stocks list: 
# {'assetType': 'Stock', 'delistingDate': 'null', 'exchange': 'NYSE', 'ipoDate': '1999-11-18', 'name': 'Agilent Technologies Inc', 'status': 'Active', 'symbol': 'A'}

import logging
from alpha_vantage.techindicators import TechIndicators

class AVFilter():
    def __init__(self, stocks):
        self.stocks = stocks
        self.ti = TechIndicators(key='E6H2MXTA1P7JD4II')
    
    def get_sma(self, stock, interval='15min', time_period=30):
        """
        time_period:  How many data points to average (default 20)
        interval:  time interval between two conscutive values,
                supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
                'weekly', 'monthly' (default 'daily')
        """
        sma = self.ti.get_sma(stock, time_period=time_period, interval=interval)
        return sma

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    avf = AVFilter(['AAPL'])
    for _ in range(100):
        print(_)
        sma = avf.get_sma('AAPL')
        #print(sma)
        temp2 = sma[0]
        temp = temp2[list(temp2)[0]]
        print(temp)
    #logging.info(sma)