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
        self._warehouse = JsonWarehouse(config.stocks_data_json_path, config.diagnostics_path)
        self._crits_handler = CriterasHandler(self._warehouse, self._data_source)

    def get_data(self):
        #Restart Warehouse and add stocks from CSV
        self._warehouse.restart_warehouse(self._stock_finder.get_top_stocks_by_daily_turnover(config.num_of_stocks_to_read))
        #Add Data
        self._crits_handler.add_needed_data_for_crits()
        self._crits_handler.check_against_crits()
        self._crits_handler.check_against_inverted_crits()
        self.add_overview_data()
        #Save stocks data
        self._warehouse.save_stocks_data()
        #Save failed symbols to file
        failed_symbols = self._data_source.get_failed_symbols()
        self._warehouse.write_failed_symbols(failed_symbols)

    def add_overview_data(self):
        for symbol in self._warehouse.get_symbols():
            if (self._warehouse.is_symbol_rejected(symbol) and self._warehouse.is_symbol_rejected_inv(symbol)): continue
            self._warehouse.add_overview_data(symbol, self._data_source.get_overview(symbol))
    
    def write_execution_time(self, time_str):
        self._warehouse.write_execution_time(time_str)


if __name__ == "__main__":
    pass