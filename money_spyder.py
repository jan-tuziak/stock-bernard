#! /usr/bin/python3

import logging
import time
import json
import pandas as pd

from src.lighthouse import Lighthouse
from src.postman import Postman
from src.data_hole import DataHole

if __name__ == "__main__":
    #start timer
    startTime = time.time()

    #create main dataframe
    df = pd.DataFrame()

    # get app config
    with open('money_spyder.json') as json_file:
        config = json.load(json_file)
    
    # Config logger
    logging.basicConfig(level=logging.INFO, **config['logger'])
    
    #Print App Header
    logging.info("Money Spyder's Lighthouse starting.")
    
    # get list of stocks
    dh = DataHole(df, config['av_key'], config['data_hole']['csv_name'])
    dh.get_from_csv(600)
    df = dh.df

    lh = Lighthouse(df, config['av_key'])  
    # filter stocks by sma300x15min > sma100x15min
    lh.filter_sma_greater_than_sma('15min',300, '15min', 100)
    
    # filter stocks by sma30x15min > sma100x15min
    lh.filter_sma_greater_than_sma('15min',30, '15min', 100)
    
    # filter stocks by sma900x1min > sma300x1min
    lh.filter_sma_greater_than_sma('1min',900, '1min', 300)

    # Create TradingViewList String from stocks
    stocks_to_observe = lh.create_tv_string()
    
    # Send Email with promising stocks
    crt = ['600 stocks with highest market capitalization','sma300x15min > sma100x15min','sma30x15min > sma100x15min', 'sma900x1min > sma300x1min']
    pstm = Postman(**config['postman'])
    pstm.send_lh_email(stocks_to_observe, crt)

    # Log script execution time
    executionTime = (time.time() - startTime)
    logging.info(f'Lighthouse execution time: {time.strftime("%H:%M:%S", time.gmtime(executionTime))}')