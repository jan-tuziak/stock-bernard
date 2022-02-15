#! /usr/bin/python3
import _thread
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s")
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import data_handler
import ui
import database
import stocks_from_csv

app = FastAPI()

# Start Stocks Data Loop
@app.on_event("startup")
def app_startup():
    _thread.start_new_thread(data_handler.start_data_handler_loop, ())
    pass

@app.get("/", response_class=HTMLResponse)
async def root():
    return ui.root()

@app.get("/lighthouse_long")
async def run_lighthouse_long():
    lh_long_results, err = database.get_lighthouse_long_results()
    if err:
        return ui.error(err)
    return ui.lighthouse(lh_long_results, True)

@app.get("/lighthouse_short")
async def run_lighthouse_short():
    lh_short_results, err = database.get_lighthouse_short_results()
    if err:
        return ui.error(err)
    return ui.lighthouse(lh_short_results, False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="127.0.0.1", port=port)