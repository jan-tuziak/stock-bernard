import logging
import time
import datetime
import pandas as pd

import config
from src.data_handler.data_handler import DataHandler

class DataHandlerLoop():

    def execute_data_handler(self):
        logging.info(f'Stocks data loop start')
        startTime = time.time()
        dh = DataHandler()
        dh.get_data()
        del dh
        executionTime = (time.time() - startTime)
        executionTimeStr = time.strftime("%H:%M:%S", time.gmtime(executionTime))
        logging.info(f'Stocks data loop end. Loop time: {executionTimeStr}')

    def start_data_handler_loop(self):
        self.execute_data_handler()
        while True:
            now = datetime.datetime.now()
            # if weekend day wait for 1 hour and skip this iteration
            cur_date = now.strftime("%Y-%m-%d")
            if len(pd.bdate_range(cur_date,cur_date)) == 0:
                logging.info("Weekend - waiting 1h")
                time.sleep(60 * 60) 
                continue
            
            # # if outside of market hours (+/- 1 hour) wait for 5 min and skip this iteration
            # opening_hours = datetime.time(config.market_opening_hour[0] - 1, config.market_opening_hour[1])
            # closing_hours = datetime.time(config.market_closing_hour[0] + 1, config.market_closing_hour[1])
            # if now.time() < opening_hours or now.time() > closing_hours:
            #     time.sleep(5 * 60)
            #     continue

            # if outside of data handler hours then wait for 30min and skip this iteration
            opening_hours = datetime.time(config.dh_opening_hour[0], config.dh_opening_hour[1])
            closing_hours = datetime.time(config.dh_closing_hour[0], config.dh_closing_hour[1])
            if now.time() < opening_hours or now.time() > closing_hours:
                logging.info("outside of DH working hours - waiting 30min")
                time.sleep(30 * 60)
                continue

            self.execute_data_handler()