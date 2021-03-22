'''Alpha Vantage implementation of Data Source class'''

from src.data_handler.data_source.i_data_source import IDataSource

from alpha_vantage.techindicators import TechIndicators

class AVDataSource(IDataSource):
    def __init__(self, av_key):
        self.ti = TechIndicators(key=av_key)
    
    
    def get_latest_sma(self, symbol='GOOGL', interval='daily', time_period=20):
        '''Methond for getting the latest sma value for given stock'''
        data, meta_data = ti.get_sma(symbol=symbol, interval=interval, time_period=time_period)
        data_l = list(data)
        data_l.sort(reverse=True)
        key=data_l[0]
        return float(data[key]['SMA'])