'''Json implemention os Stocks Warehouse'''

import logging
import json

from src.stocks_warehouse.i_stocks_warehouse import IStocksWarehouse

class JsonWarehouse(IStocksWarehouse):
    def __init__(self, json_path):
        self.json_path = json_path
        self.stocks = []

    def init_from_symbols(self, symbols):
        self.stocks = symbols
        self._create_rejected_field()
    
    def deserialize(self):
        with open(self.json_path) as json_file:
            self.stocks = json.load(json_file)

    def _create_rejected_field(self):
        for s in self.stocks:
            s['rejected'] = False

    def get_symbols(self):
        stocks_list = []
        for s in self.stocks:
            stocks_list.append(s["symbol"])
        return stocks_list

    def add_sma(self, symbol, time_period, interval, value):
        idx = self._get_idx(symbol)
        self.stocks[idx][self._sma_str(time_period, interval)] = value

    def get_sma(self, symbol, time_period, interval):
        idx = self._get_idx(symbol)
        return self.stocks[idx][self._sma_str(time_period, interval)]

    def add_smas(self, symbol, time_period, interval, values):
        '''add list of sma values to a given symbol'''
        idx = self._get_idx(symbol)
        self.stocks[idx][self._smas_str(time_period, interval)] = values

    def get_smas(self, symbol, time_period, interval):
        '''get list of sma values for given symbol'''
        idx = self._get_idx(symbol)
        return self.stocks[idx][self._smas_str(time_period, interval)]

    def set_rejected(self, symbol):
        idx  = self._get_idx(symbol)
        self.stocks[idx]['rejected'] = True

    def is_symbol_rejected(self, symbol):
        idx  = self._get_idx(symbol)
        try:
            return self.stocks[idx]['rejected']
        except:
            return False
            
    def serialize(self):      
        with open(self.json_path, 'w') as fout:
            json.dump(self.stocks, fout, indent=4)
        logging.info(f'Number of Stocks saved to file: {len(self.stocks)}')

    def get_stocks_for_tv(self, sector="", include_rejected=False):
        tv_stocks = []
        for s in self.stocks:
            #skip this stock if "include_rejected" is False and is rejected
            if (not include_rejected) and s['rejected']: continue
            
            #skip if sector is defined and the stock is not of this sector
            if (len(sector)!=0) and s['sector']!=sector: continue

            #TradingView does not what 'NYSE ARCA' is. It recognizes those symbols as port of "AMEX" exchange
            if s['exchange'] == 'NYSE ARCA': 
                exch = 'AMEX'
            else:
                exch = s['exchange']
            tv_stocks.append(exch + ':' + s['symbol'])
        stocks_to_observe = ', '.join(tv_stocks)
        #logging.debug(f'TV String: {tv_stocks}')
        logging.debug(f'Stocks to observe: {stocks_to_observe}')
        return stocks_to_observe

    def _get_idx(self, symbol):
        idx =  next((index for (index, d) in enumerate(self.stocks) if d["symbol"] == symbol), None)
        if idx == None: raise IndexError(f'Symbol {symbol} not found in Warehouse.')
        return idx

    def _sma_str(self, time_period, interval):
        return f"sma{time_period}x{interval}"

    def _smas_str(self, time_period, interval):
        return f"smas{time_period}x{interval}"

    def add_overview_data(self, symbol, overview_data):
        '''add overview data for given symbol'''
        idx = self._get_idx(symbol)
        self.stocks[idx]['overview'] = overview_data

    def get_overview_data(self, symbol):
        '''get overview data for given symbol'''
        idx = self._get_idx(symbol)
        return self.stocks[idx]['overview']

    def get_data_for_overview_table(self, sector="", include_rejected=False):
        '''get overview data for HTML Table for given sector if specified'''
        ov_tbl_data = []
        for s in self.stocks:
            #skip this stock if "include_rejected" is False and is rejected
            if (not include_rejected) and s['rejected']: continue

            #skip if sector is defined and the stock is not of this sector
            if (len(sector)!=0) and s['sector']!=sector: continue

            one_stock_data = {}
            one_stock_data['symbol'] = s['symbol']
            one_stock_data['exchange'] = s['exchange']
            one_stock_data['overview'] = s['overview']
            one_stock_data['sector'] = s['sector']
            ov_tbl_data.append(one_stock_data)
        logging.debug(f'Overview Table Data: {ov_tbl_data}')
        return ov_tbl_data



