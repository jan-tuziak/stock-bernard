'''Alpha Vantage implementation of Data Source class'''

import logging
import time

from alpha_vantage.techindicators import TechIndicators

from src.data_handler.data_source.i_data_source import IDataSource

class AVDataSource(IDataSource):
    def __init__(self, av_key):
        self.ti = TechIndicators(key=av_key)
        self.count = 0
        self.retries = 3
        self.failed_symbols = []
    
    def get_latest_sma(self, symbol='GOOGL', interval='daily', time_period=20):
        '''Methond for getting the latest sma value for given stock'''
        temp_e = None
        for _ in range(self.retries):
            try:
                #wait because can make 75 API calls per minute
                time.sleep(1)
                data, meta_data = self.ti.get_sma(symbol=symbol, interval=interval, time_period=time_period, series_type='close')   
                data_l = list(data)
                data_l.sort(reverse=True)
                key=data_l[0]
                sma = float(data[key]['SMA'])
                logging.debug(f"{symbol} sma{time_period}x{interval} = {sma}")
                return sma
            except Exception as e:
                time.sleep(10)
                temp_e = e
        logging.error(f'Failed to get data for {symbol} from API: '+ str(temp_e))
        logging.debug(f"Num of errors = {self.count}. Failed symbols = {set(self.failed_symbols)}")
        self.count = self.count + 1
        self.failed_symbols.append(symbol)
        return 0
            
