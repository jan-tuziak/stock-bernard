import pandas_datareader as pdr
import pandas as pd
import datetime 

aapl = pdr.get_data_yahoo('AAPL')

tickers = pdr.nasdaq_trader.get_nasdaq_symbols()

print(type(tickers))