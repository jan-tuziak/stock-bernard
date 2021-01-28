#! /usr/bin/python3

import logging
import time
import json
import pandas as pd

from src.data_handler import DataHandler
from src.lighthouse import Lighthouse
from src.postman import Postman

def execute_lighthouse():
    #start timer
    startTime = time.time()

    # get app config
    with open('data/money_spyder.json') as json_file:
        config = json.load(json_file)
    
    # Config logger
    logging.basicConfig(level=logging.INFO, **config['logger'])
    
    #Print App Header
    logging.info("Money Spyder's Lighthouse starting")
    
    #define the timeframes
    timeframes = [
        {"multiplier":1, 
        "timespan": "minute"},
        {"multiplier":15, 
        "timespan": "minute"}
    ]
    '''Polygon timeframes definitions:
        - multiplier (int)
        - timespan (string) - minute, hour, day, week, month, quarter, year
    '''

    # get list of stocks
    dh = DataHandler(config['poly_key'], config['data_hole']['csv_name'], timeframes)
    dh.get_stocks_from_csv(600)
    dh.add_close_poly()
    #df = dh.df

    lh = Lighthouse(dh)  
    # filter stocks by sma300x15min > sma100x15min
    lh.filter_sma_greater_than_sma(timeframes[1] ,300, timeframes[1], 100)
    
    # filter stocks by sma30x15min > sma100x15min
    lh.filter_sma_greater_than_sma(timeframes[1], 30, timeframes[1], 100)
    
    # filter stocks by sma900x1min > sma300x1min
    lh.filter_sma_greater_than_sma(timeframes[0], 900, timeframes[0], 300)

    # save stocks to file
    lh.save_stocks_to_file()

    # Create TradingViewList String from stocks
    stocks_to_observe = lh.create_tv_string()
    
    # Send Email with promising stocks
    crt = ['600 stocks with highest market capitalization','sma300x15min > sma100x15min','sma30x15min > sma100x15min', 'sma900x1min > sma300x1min']
    pstm = Postman(**config['postman'])
    pstm.send_lh_email(stocks_to_observe, crt)

    # Log script execution time
    executionTime = (time.time() - startTime)
    logging.info(f'Lighthouse execution time: {time.strftime("%H:%M:%S", time.gmtime(executionTime))}')
    logging.info(f'Stocks to observe: {stocks_to_observe}')

if __name__ == "__main__":
    execute_lighthouse()
