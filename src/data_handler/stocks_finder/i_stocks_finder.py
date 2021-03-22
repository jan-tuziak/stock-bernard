'''Informal Interface for Stocks Finder class'''

class IStocksFinder:

    def get_top_stocks_by_daily_turnover(self, number):
        '''Return a list of the biggest stocks by stock's daily turnover'''
        return NotImplementedError