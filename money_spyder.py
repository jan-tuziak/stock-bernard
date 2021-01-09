#! /usr/bin/python3

import logging
import time
import json

from src.lighthouse import Lighthouse
from src.postman import Postman
from src.data_hole import DataHole

if __name__ == "__main__":
    #start timer
    startTime = time.time()

    # get app config
    with open('money_spyder.json') as json_file:
        config = json.load(json_file)
    
    # Config logger
    logging.basicConfig(level=logging.INFO, **config['logger'])
    
    #Print App Header
    logging.info("Money Spyder's Lighthouse starting.")
    
    # get list of stocks
    dh = DataHole(config['av_key'], config['data_hole']['csv_name'])
    stocks = dh.get_from_csv(600)

    lh = Lighthouse(config['av_key'], stocks)  
    # filter stocks by sma100x15min < sma300x15min
    lh.filter_sma_greater_than_sma('15min',100, '15min', 300)
    
    # filter stocks by sma100x15min < sma30x15min
    lh.filter_sma_greater_than_sma('15min',100, '15min', 30)

    # Create TradingViewList String from stocks
    stocks_to_observe = lh.create_tv_string()
    
    # Send Email with promising stocks
    crt = ['600 stocks with highest market capitalization','sma300x15min > sma100x15min','sma30x15min > sma100x15min']
    pstm = Postman(**config['postman'])
    pstm.send_lh_email(stocks_to_observe, crt)

    # Log script execution time
    executionTime = (time.time() - startTime)
    logging.info(f'Lighthouse execution time: {executionTime/3600}h')