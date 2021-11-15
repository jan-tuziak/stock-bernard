#! /usr/bin/python3
import config

import _thread
import logging
logging.basicConfig(level=logging.INFO, **config.logger)
import os
import uvicorn
import json

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.lighthouse import Lighthouse
from src.data_handler.data_handler_loop import DataHandlerLoop
from src.ui import ui_root, ui_lighthouse, ui_datastocks, ui_failedsymbols, ui_executiontime

app = FastAPI()

def read_json_file(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)

# Start Stocks Data Loop
@app.on_event("startup")
def start_data_loop():
    dhl = DataHandlerLoop()
    _thread.start_new_thread(dhl.start_data_handler_loop, ())

@app.get("/", response_class=HTMLResponse)
async def root():
    return ui_root()

@app.get("/lighthouse")
async def run_lighthouse():
    return ui_lighthouse(execute_lighthouse())

@app.get("/datastocks")
async def datasctocks():
    datastocks = read_json_file(config.json_path)
    return ui_datastocks(datastocks)

@app.get("/failedsymbols")
async def failedsymbols():
    failed_symbols = read_json_file(config.failed_symbols_path)["failed_symbols"]
    return ui_failedsymbols(failed_symbols)

@app.get("/executiontime")
async def executiontime():
    execute_time = read_json_file(config.execute_time_path)["data_handler_execution_time"]
    return ui_executiontime(execute_time)

def execute_lighthouse():
    lh = Lighthouse()  
    stocks_to_observe = lh.get_lighthouse_stocks()
    del lh
    return stocks_to_observe

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)