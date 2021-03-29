import pprint
import logging

import config
from src.data_handler.stocks_finder.csv_stocks_finder import CSVStocksFinder
from src.data_handler.data_source.av_data_source import AVDataSource
from src.stocks_warehouse.json_warehouse import JsonWarehouse
from src.criterias.criterias_handler import CriterasHandler

class DataHandler:
    def __init__(self):
        logging.debug("Initializing Data Handler")
        self._stock_finder = CSVStocksFinder(config.csv_path)
        self._data_source = AVDataSource(config.av_key)
        self._warehouse = JsonWarehouse(config.json_path)
        self._crits_handler = CriterasHandler(self._warehouse, self._data_source)

    def get_data(self):
        #Initialize Warehouse with stocks from CSV
        self._warehouse.init_from_symbols(self._stock_finder.get_top_stocks_by_daily_turnover(config.num_of_stocks_to_read))
        #Add Data
        self._crits_handler.add_needed_data_for_crits()
        #Save warehouse to file
        self._warehouse.serialize()



if __name__ == "__main__":
    pass
    # from alpha_vantage.techindicators import TechIndicators
    # ti = TechIndicators(key=config.av_key)
    # # Get json object with the intraday data and another with  the call's metadata
    # data, meta_data = ti.get_sma(symbol='GOOGL', interval='daily', time_period=20)
    # data_l = list(data)
    # data_l.sort(reverse=True)
    # key=data_l[0]
    # pprint.pprint(float(data[key]['SMA']))