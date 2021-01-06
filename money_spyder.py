#! /usr/bin/python3

import logging
import time

from src.lighthouse import Lighthouse
from src.postman import Postman

if __name__ == "__main__":
    #start timer
    startTime = time.time()
    
    # Config logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
    #Print App Header
    logging.info("Money Spyder's Lighthouse starting.")
    
    # get list of stocks
    lh = Lighthouse()
    lh.get_data()

    # filter stocks by daily turnover
    lh.filter_by_daily_turnover(2000000)
    
    # filter stocks by sma100x15min < sma300x15min
    lh.filter_sma_greater_than_sma('15min',100, '15min', 300)

    # Create TradingViewList String from stocks
    stocks_to_observe = lh.create_tv_string()
    
    # Send Email with promising stocks
    pstm = Postman()
    addresses = ['jan.tuziak@outlook.com', 'tomasztuziak@yahoo.com']
    pstm.send_lh_email(addresses, stocks_to_observe)

    # Log script execution time
    executionTime = (time.time() - startTime)
    logging.info(f'Lighthouse execution time: {executionTime/3600}h')