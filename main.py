#! /usr/bin/python3
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

from fastapi import FastAPI, BackgroundTasks
app = FastAPI()

# from src.data_handler_poly import DataHandlerPoly
from src.data_handler.data_handler_av import DataHandlerAV
from src.lighthouse import Lighthouse

def get_stocks_data():
    startTime = time.time()
    dh = DataHandlerAV()
    dh.get_data()
    del dh
    executionTime = (time.time() - startTime)
    executionTimeStr = time.strftime("%H:%M:%S", time.gmtime(executionTime))
    logging.info(f'Stocks data loop time: {executionTimeStr}')

def start_stocks_data_loop():
    get_stocks_data()
    while True:
        now = datetime.datetime.now()
        # if weekend day wait for 1 hour and skip this iteration
        cur_date = now.strftime("%Y-%m-%d")
        if len(pd.bdate_range(cur_date,cur_date)) == 0:
            time.sleep(60 * 60) 
            continue
        
        # if outside of market hours (+/- 1 hour) wait for 5 min and skip this iteration
        opening_hours = datetime.time(config.market_opening_hour[0] - 1, config.market_opening_hour[1])
        closing_hours = datetime.time(config.market_closing_hour[0] + 1, config.market_closing_hour[1])
        if now.time() < opening_hours or now.time() > closing_hours:
            time.sleep(5 * 60)
            continue

        get_stocks_data()

def execute_lighthouse():
    lh = Lighthouse()  
    stocks_to_observe = lh.get_lighthouse_stocks()
    del lh
    return stocks_to_observe

# Start Stocks Data Loop
@app.on_event("startup")
def start_data_loop():
    _thread.start_new_thread(start_stocks_data_loop, ())

@app.get("/")
async def root():
    return {"message": "Hello from Money Spyder"}

@app.get("/lighthouse")
async def run_lighthouse():
    return {"stocks_to_observe":execute_lighthouse()}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
