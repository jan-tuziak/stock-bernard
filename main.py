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
from src.stocks_warehouse.json_warehouse import JsonWarehouse
from src.ui import ui_root, ui_lighthouse, ui_datastocks, ui_failedsymbols, ui_executiontime

app = FastAPI()

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
    stocks_data, table_data = execute_lighthouse()
    return ui_lighthouse(stocks_data, table_data, False)

@app.get("/lighthouse/{sector}")
async def run_lighthouse_sector(sector):
    stocks_data, table_data = execute_lighthouse()
    return ui_lighthouse(stocks_data, table_data, False, sector)

@app.get("/inverted_lighthouse")
async def run_inverted_lighthouse():
    stocks_data, table_data = execute_inverted_lighthouse()
    return ui_lighthouse(stocks_data, table_data, True)

@app.get("/inverted_lighthouse/{sector}")
async def run_inverted_lighthouse_sector(sector):
    stocks_data, table_data = execute_inverted_lighthouse()
    return ui_lighthouse(stocks_data, table_data, True, sector)

@app.get("/datastocks")
async def datasctocks():
    jw = JsonWarehouse(config.stocks_data_json_path, config.diagnostics_path)
    datastocks = jw.read_stocks_data()
    del jw
    return ui_datastocks(datastocks)

@app.get("/failedsymbols")
async def failedsymbols():
    jw = JsonWarehouse(config.stocks_data_json_path, config.diagnostics_path)
    failed_symbols = jw.read_failed_symbols()
    del jw
    return ui_failedsymbols(failed_symbols)

@app.get("/executiontime")
async def executiontime():
    jw = JsonWarehouse(config.stocks_data_json_path, config.diagnostics_path)
    execute_time = jw.read_execution_time()
    del jw
    return ui_executiontime(execute_time)

def execute_lighthouse(sector=""):
    lh = Lighthouse()  
    stocks_to_observe, overview_table_data = lh.get_lighthouse_stocks(sector)
    del lh
    return stocks_to_observe, overview_table_data

def execute_inverted_lighthouse(sector=""):
    lh = Lighthouse()  
    stocks_to_observe, overview_table_data = lh.get_lighthouse_stocks_inverted(sector)
    del lh
    return stocks_to_observe, overview_table_data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
