#! /usr/bin/python3

import logging
import time

from src.lighthouse_av import LighthouseAV
from src.money_spyder_email import MoneySpyderEmail

if __name__ == "__main__":
    #start timer
    startTime = time.time()
    
    # Config logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
    #Print App Header
    logging.info("Money Spyder's Lighthouse starting.")
    
    # get list of stocks
    lh_av = LighthouseAV()
    lh_av.get_data()
    lh_av.filter_by_daily_turnover(2000000)
    
    # filter stocks by SMA
    lh_av.filter_greater_than_sma('15min',900)

    # Create TradingViewList String from stocks
    stocks_to_observe = lh_av.create_tv_string()
    
    # Send Email with promising stocks
    mse = MoneySpyderEmail()
    mse.send_lh_email('jan.tuziak@outlook.com', stocks_to_observe)

    # Log script execution time
    executionTime = (time.time() - startTime)
    logging.info(f'Lighthouse execution time: {executionTime}s')