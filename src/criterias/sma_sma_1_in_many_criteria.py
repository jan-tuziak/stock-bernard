'''Criteria that checks wether given sma is bigger than other sma'''

from src.criterias.i_criteria import ICriteria

class SmaSma1InManyCriteria(ICriteria):

    def __init__(self, time_period_x, interval_x, time_period_y, interval_y, lookback):
        self._time_period_x = time_period_x
        self._interval_x = interval_x
        self._time_period_y = time_period_y
        self._interval_y = interval_y
        self._lookback = lookback

    def check_symbol(self, warehouse, symbol):
        smas_x = warehouse.get_smas(symbol, self._time_period_x, self._interval_x)
        smas_y = warehouse.get_smas(symbol, self._time_period_y, self._interval_y)
        for lb in self._lookback:
            if smas_x[lb-1] > smas_y[lb-1]: return True
        return False

    def add_needed_data(self, warehouse, data_source):
        for symbol in warehouse.get_symbols():
            if not warehouse.is_symbol_rejected(symbol):
                smas_x = data_source.get_smas(symbol, self._interval_x, self._time_period_x, max(self._lookback))
                smas_y = data_source.get_smas(symbol, self._interval_y, self._time_period_y, max(self._lookback))
                warehouse.add_smas(symbol, self._time_period_x, self._interval_x, smas_x)
                warehouse.add_smas(symbol, self._time_period_y, self._interval_y, smas_y)
                if len(smas_x) == 0 or len(smas_y) == 0: warehouse.set_rejected(symbol)
                if smas_x[0] == 0 or smas_y[0] == 0: warehouse.set_rejected(symbol)