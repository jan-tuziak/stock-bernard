'''Get stock data from Alpha Vantage API'''

import logging
# logging.basicConfig(level=logging.DEBUG)
import time
import os

from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.fundamentaldata import FundamentalData

AV_KEY = os.environ['AV_KEY']
RETRIES = 3
WAIT_AFTER_ERR = 5
tech_ind = TechIndicators(key=AV_KEY)
fund_data = FundamentalData(key=AV_KEY)

def get_latest_sma(symbol:str='GOOGL', interval:str='daily', time_period:int=20) -> tuple[float, Exception]:
    '''Methond for getting the latest sma value for given stock'''
    err = None
    for _ in range(RETRIES):
        try:
            #wait because can make 75 API calls per minute
            time.sleep(1)
            data, meta_data = tech_ind.get_sma(symbol=symbol, interval=interval, time_period=time_period, series_type='close')   
            data_l = list(data)
            data_l.sort(reverse=True)
            key=data_l[0]
            sma = float(data[key]['SMA'])
            logging.debug(f"{symbol} sma{time_period}x{interval} = {sma}")
            return sma, None
        except Exception as e:
            time.sleep(WAIT_AFTER_ERR)
            err = e
    logging.error(f'Failed to get SMA for {symbol} from AV API. Error msg: {err}')
    return -1, err
        
def get_smas(symbol:str='GOOGL', interval:str='daily', time_period:int=20, lookbacks:list[int]=[100,200]) -> tuple[list[float], Exception]:
    '''Methond for getting list of sma values for given stock'''
    err = None
    for _ in range(RETRIES):
        try:
            #wait because can make 75 API calls per minute
            time.sleep(1)
            data, meta_data = tech_ind.get_sma(symbol=symbol, interval=interval, time_period=time_period, series_type='close')   
            data_l = list(data)
            data_l.sort(reverse=True)
            sma_all = []
            for key in data_l:
                sma = float(data[key]['SMA'])
                sma_all.append(sma)
            smas = []
            for lb in lookbacks:
                smas.append(sma_all[lb])
            logging.debug(f"{symbol} smas{time_period}x{interval} = {smas}")
            return smas, None
        except Exception as e:
            time.sleep(WAIT_AFTER_ERR)
            err = e
    logging.error(f'Failed to get SMAs for {symbol} from AV API. Error msg: {err}')
    return [-1], err

def get_overview(symbol:str='GOOGL'):
    err = None
    try:
        return fund_data.get_company_overview(symbol)[0], None
    except Exception as e:
        time.sleep(WAIT_AFTER_ERR)
        err = e
    logging.error(f'Failed to get overview data for {symbol} from AV API. Error msg: {err}')
    return {}, err

if __name__ == "__main__":
    print(get_overview())
    print(get_latest_sma())
    print(get_smas())