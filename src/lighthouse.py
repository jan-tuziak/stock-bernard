import config
import logging

from src.stocks_warehouse.json_warehouse import JsonWarehouse
from src.criterias.criterias_handler import CriterasHandler

class Lighthouse():
    def __init__(self):
        self._warehouse = JsonWarehouse(config.stocks_data_json_path, config.diagnostics_path)
        self._crits_handler = CriterasHandler(self._warehouse)
    
    def get_lighthouse_stocks(self, sector):
        self._crits_handler.check_against_crits()
        return self._warehouse.get_stocks_for_tv(sector), self._warehouse.get_data_for_overview_table(sector)

    def get_lighthouse_stocks_inverted(self, sector):
        self._crits_handler.check_against_inverted_crits()
        return self._warehouse.get_stocks_for_tv_inverted(sector), self._warehouse.get_data_for_overview_table_inverted(sector)

if __name__ == "__main__":
    pass