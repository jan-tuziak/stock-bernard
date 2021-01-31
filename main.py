#! /usr/bin/python3

import logging
import time
import json
import os
import uvicorn
import pandas as pd

from fastapi import FastAPI, BackgroundTasks
app = FastAPI()

from src.data_handler import DataHandler
from src.lighthouse import Lighthouse
from src.postman import Postman

@app.get("/")
async def root():
    return {"message": "Hello from Money Spyder"}

def execute_lighthouse():
    #set lighthouse status env var
    os.environ["LH_STATUS"] = "True"

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

    lh = Lighthouse(dh, **config['lighthouse'])  
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
    
    # Log script execution time
    executionTime = (time.time() - startTime)
    executionTimeStr = time.strftime("%H:%M:%S", time.gmtime(executionTime))
    logging.info(f'Lighthouse execution time: {executionTimeStr}')
    logging.info(f'Stocks to observe: {stocks_to_observe}')
    
    # Send Email with promising stocks
    crt = ['600 stocks with highest market capitalization','sma300x15min > sma100x15min','sma30x15min > sma100x15min', 'sma900x1min > sma300x1min']
    pstm = Postman(**config['postman'])
    pstm.send_lh_email(stocks_to_observe, crt, [config['logger']['filename'], config['lighthouse']['stocks_filename']])

    #update lighthouse working status
    os.environ["LH_STATUS"] = "False"
    os.environ["LH_EXEC_TIME"] = executionTimeStr
    os.environ["LH_STOCKS"] = stocks_to_observe

@app.get("/lighthouse")
def run_lighthouse(background_tasks: BackgroundTasks):
    if os.environ["LH_STATUS"] == "True":
        return {"message":"Lighthouse already running"}
    else:
        background_tasks.add_task(execute_lighthouse)
        return {"message":"Lighthouse started in background"}

@app.get("/lighthouse/status")
def get_lighthouse_status():  
    return {"status": os.environ["LH_STATUS"], 
            "Last Execution Time":os.environ["LH_EXEC_TIME"],
            "Stocks to observe":os.environ["LH_STOCKS"]}

if __name__ == "__main__":
    pass
    # port = int(os.environ.get("PORT", 5000))
    # uvicorn.run(app, host="0.0.0.0", port=port)
