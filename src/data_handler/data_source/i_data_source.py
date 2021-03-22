'''Informal Interface for Data Source class'''

class IDataSource:

    def get_latest_sma(self, symbol='GOOGL', interval='daily', time_period=20):
        '''
        Methond for getting the latest sma value for given stock
        '''
        return NotImplementedError
