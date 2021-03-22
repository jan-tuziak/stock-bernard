'''Criteria that checks wether given sma is bigger than other sma'''

from src.criterias.i_criteria import ICriteria

class SmaSmaCriteria(ICriteria):

    def __init__(self, time_period_x, interval_x, time_period_y, interval_y):
        self._time_period_x = time_period_x
        self._interval_x = interval_x
        self._time_period_y = time_period_y
        self._interval_y = interval_y

    def check_symbol(warehouse, symbol):
        sma_x = self._warehouse.get_sma(symbol, self._time_period_x, self._interval_x)
        sma_y = self._warehouse.get_sma(symbol, self._time_period_y, self._interval_y)
        return sma_x > sma_y

    def add_needed_data(self, warehouse):