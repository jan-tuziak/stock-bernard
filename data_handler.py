import datetime
import logging
import pandas as pd
import time

import database
import stocks_from_csv

NUM_OF_STOCKS_TO_ANALYZE = 1000

def execute_data_handler() -> None:
    logging.info(f'DH Start')
    startTime = time.time()
    
    # TODO: Add necessary stock data (smas) to database
    err = database.add_stock_parameters()
    # TODO: Add Overview data to stocks that passed Lighthouse Long or Lighthouse Short
    executionTime = (time.time() - startTime)
    executionTimeStr = time.strftime("%H:%M:%S", time.gmtime(executionTime))
    # TODO: write execution time to database
    database.add_execution_time(executionTimeStr)
    logging.info(f'DH End. Execution time: {executionTimeStr}')


def start_data_handler_loop() -> None:
    stocks, err = stocks_from_csv.get_stock_list(NUM_OF_STOCKS_TO_ANALYZE)
    if err:
        logging.error(f'Could not get stock list from csv. Error msg: {err}')
        return
    err = database.add_stock_list(stocks)
    if err:
        logging.error(f'Could not add stock list to database. Error msg: {err}')
        return
    execute_data_handler()
    while True:
        now = datetime.datetime.now()
        # if weekend day wait for 1 hour and skip this iteration
        cur_date = now.strftime("%Y-%m-%d")
        if len(pd.bdate_range(cur_date,cur_date)) == 0:
            # logging.info("Weekend - waiting 1h")
            time.sleep(60 * 60) 
            continue

        # if outside of data handler activation window wait for 30min and skip this iteration
        dh_activation_window_start = datetime.time(0, 00)   # 00:00 UTC (midnight)
        dh_activation_window_end = datetime.time(1, 00)     # 01:00 UTC
        if now.time() < dh_activation_window_start or now.time() > dh_activation_window_end:
            # logging.info("outside of DH activation window - waiting 30min")
            time.sleep(30 * 60)
            continue

        execute_data_handler()