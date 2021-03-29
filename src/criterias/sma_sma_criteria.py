'''Criteria that checks wether given sma is bigger than other sma'''

from src.criterias.i_criteria import ICriteria

class SmaSmaCriteria(ICriteria):

    def __init__(self, time_period_x, interval_x, time_period_y, interval_y):
        self._time_period_x = time_period_x
        self._interval_x = interval_x
        self._time_period_y = time_period_y
        self._interval_y = interval_y

    def check_symbol(self, warehouse, symbol):
            sma_x = warehouse.get_sma(symbol, self._time_period_x, self._interval_x)
            sma_y = warehouse.get_sma(symbol, self._time_period_y, self._interval_y)
            return sma_x > sma_y

    def add_needed_data(self, warehouse, data_source):
        for symbol in warehouse.get_symbols():
            if not warehouse.is_symbol_rejected(symbol):
                sma_x = data_source.get_latest_sma(symbol, self._interval_x, self._time_period_x)
                sma_y = data_source.get_latest_sma(symbol, self._interval_y, self._time_period_y)
                warehouse.add_sma(symbol, self._time_period_x, self._interval_x, sma_x)
                warehouse.add_sma(symbol, self._time_period_y, self._interval_y, sma_y)
                if sma_x == 0 or sma_y == 0: warehouse.set_rejected(symbol)