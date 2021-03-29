#! /usr/bin/python3

def get_stocks_data():
    import config

    import sys
    import datetime
    import _thread
    import logging
    logging.basicConfig(level=logging.INFO, **config.logger)
    import time
    import json
    import os
    import uvicorn
    import pandas as pd

    from src.data_handler import DataHandlerPoly
    from src.lighthouse import Lighthouse

    startTime = time.time()
    dh = DataHandlerPoly()
    dh.get_stocks_from_csv()
    dh.add_close_poly()
    dh.add_smas()
    dh.save_stocks_to_file()
    dh.clear_memory()
    executionTime = (time.time() - startTime)
    executionTimeStr = time.strftime("%H:%M:%S", time.gmtime(executionTime))
    logging.info(f'Stocks data loop time: {executionTimeStr}')

if __name__ == "__main__":
    get_stocks_data()