'''Informal Interface for StocksWarehouse classes'''

class IStocksWarehouse:

    def add_sma(self, symbol, time_period, interval, value):
        '''add sma value to a given symbol'''
        return NotImplementedError

    def get_sma(self, symbol, time_period, interval):
        '''get sma value for given symbol'''
        return NotImplementedError

    def add_smas(self, symbol, time_period, interval, values):
        '''add list of sma values to a given symbol'''
        return NotImplementedError

    def get_smas(self, symbol, time_period, interval):
        '''get list of sma values for given symbol'''
        return NotImplementedError

    def get_symbols(self):
        '''get list of all symbols'''
        return NotImplementedError
    
    def set_rejected(self, symbol):
        '''set rejected file for given symbol. Stocks that were marked 
        as rejected will be skipped in any further calculations/handling'''
        return NotImplementedError

    def get_stocks_for_tv(self, include_rejected=False):
        '''return string of all stocks (rejected included if rejected=True) in a format
        for TradingView'''
        return NotImplementedError

    def serialize(self):
        '''seialize warehouse'''
        return NotImplementedError
    
    def deserialize(self):
        '''deseialize warehouse'''
        return NotImplementedError

    def add_overview_data(self, symbol):
        '''add overview data for given symbol'''
        return NotImplementedError

    def get_overview_data(self, symbol):
        '''get overview data for given symbol'''
        return NotImplementedError

        
    def get_data_for_overview_table(self, sector):
        '''get overview data for HTML Table for given sector if specified'''
        return NotImplementedError