#! /usr/bin/python3
import config

import _thread
import logging
logging.basicConfig(level=logging.INFO, **config.logger)
import os
import uvicorn

from fastapi import FastAPI

from src.lighthouse import Lighthouse
from src.data_handler.data_handler_loop import DataHandlerLoop

app = FastAPI()

# Start Stocks Data Loop
@app.on_event("startup")
def start_data_loop():
    dhl = DataHandlerLoop()
    _thread.start_new_thread(dhl.start_data_handler_loop, ())

@app.get("/")
async def root():
    return {"message": "Hello from Money Spyder"}

@app.get("/lighthouse")
async def run_lighthouse():
    return {"stocks_to_observe":execute_lighthouse()}

@app.get("/jsonfile")
async def jsonfile():
    import json
    with open(config.json_path) as json_file:
            return json.load(json_file)

def execute_lighthouse():
    lh = Lighthouse()  
    stocks_to_observe = lh.get_lighthouse_stocks()
    del lh
    return stocks_to_observe

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)