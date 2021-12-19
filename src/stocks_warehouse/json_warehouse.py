'''Json implemention os Stocks Warehouse'''

import logging
import json

class JsonWarehouse():
    def __init__(self, stocks_data_json_path, diagnostics_json_path):
        self.stocks_data_json_path = stocks_data_json_path
        self.diagnostics_json_path = diagnostics_json_path
        self.stocks = []
        self._get_last_data_from_db()

    # ************************* Private Functions **********************************
    def _get_last_data_from_db(self):
        with open(self.stocks_data_json_path) as json_file:
            self.stocks = json.load(json_file)

    def _create_rejected_field(self):
        for s in self.stocks:
            s['rejected'] = False
            s['rejected_inv'] = False

    def _get_idx(self, symbol):
        idx =  next((index for (index, d) in enumerate(self.stocks) if d["symbol"] == symbol), None)
        if idx == None: raise IndexError(f'Symbol {symbol} not found in Warehouse.')
        return idx

    def _sma_str(self, time_period, interval):
        return f"sma{time_period}x{interval}"

    def _smas_str(self, time_period, interval):
        return f"smas{time_period}x{interval}"
    # ******************************************************************************

    # ********************* Functions for Criterias *************************
    def add_sma(self, symbol, time_period, interval, value):
        idx = self._get_idx(symbol)
        self.stocks[idx][self._sma_str(time_period, interval)] = value

    def get_sma(self, symbol, time_period, interval):
        idx = self._get_idx(symbol)
        return self.stocks[idx].get(self._sma_str(time_period, interval), -1)

    def add_smas(self, symbol, time_period, interval, values):
        '''add list of sma values to a given symbol'''
        idx = self._get_idx(symbol)
        self.stocks[idx][self._smas_str(time_period, interval)] = values

    def get_smas(self, symbol, time_period, interval):
        '''get list of sma values for given symbol'''
        idx = self._get_idx(symbol)
        return self.stocks[idx].get(self._smas_str(time_period, interval), [-1])
    # **************************************************************************

    # ***************************************** Functions for Overview ************************************
    def add_overview_data(self, symbol, overview_data):
        '''add overview data for given symbol'''
        idx = self._get_idx(symbol)
        self.stocks[idx]['overview'] = overview_data

    def get_overview_data(self, symbol):
        '''get overview data for given symbol'''
        idx = self._get_idx(symbol)
        return self.stocks[idx].get('overview')

    def _get_data_for_overview_table(self, sector="", rejected_key="rejected", include_rejected=False):
        '''get overview data for HTML Table for given sector if specified'''
        ov_tbl_data = []
        for s in self.stocks:
            #skip this stock if "include_rejected" is False and is rejected
            if (not include_rejected) and s[rejected_key]: continue

            #skip if sector is defined and the stock is not of this sector
            if (len(sector)!=0) and s.get('sector') != sector: continue

            one_stock_data = {}
            one_stock_data['symbol'] = s.get('symbol')
            one_stock_data['exchange'] = s.get('exchange')
            one_stock_data['overview'] = s.get('overview')
            one_stock_data['sector'] = s.get('sector')
            ov_tbl_data.append(one_stock_data)
        logging.debug(f'Overview Table Data: {ov_tbl_data}')
        return ov_tbl_data

    def get_data_for_overview_table(self, sector="", include_rejected=False):
        return self._get_data_for_overview_table(sector, "rejected", include_rejected)

    def get_data_for_overview_table_inverted(self, sector="", include_rejected=False):
        return self._get_data_for_overview_table(sector, "rejected_inv", include_rejected)
    # ******************************************************************************************************

    # **************************** Read and Save Data **************************************
    def write_execution_time(self, time_str):
        '''save data handler loop execution time'''
        diag = self.read_diagnostics()
        diag['data_handler_execution_time'] = time_str
        self.save_diagnostics(diag)
        # with open(config.execute_time_path, 'w') as fout:
        #     json.dump(time_json, fout, indent=4)

    def read_execution_time(self):
        '''read data handler loop execution time'''
        return self.read_diagnostics().get('data_handler_execution_time')

    def read_diagnostics(self) -> dict:
        with open(self.diagnostics_json_path) as json_file:
            return json.load(json_file)

    def save_diagnostics(self, diag):
        with open(self.diagnostics_json_path, 'w') as fout:
            json.dump(diag, fout, indent=4)

    def read_stocks_data(self):
        with open(self.stocks_data_json_path) as json_file:
            data = json.load(json_file)
            return json.dumps(data, indent=4, sort_keys=True)

    def save_stocks_data(self):      
        with open(self.stocks_data_json_path, 'w') as fout:
            json.dump(self.stocks, fout, indent=4)
        logging.info(f'Number of Stocks saved to file: {len(self.stocks)}')

    def write_failed_symbols(self,failed_symbols):
        diag = self.read_diagnostics()
        diag['failed_symbols'] = failed_symbols
        self.save_diagnostics(diag)
        # with open(config.execute_time_path, 'w') as fout:
        #     json.dump(time_json, fout, indent=4)

    def read_failed_symbols(self):
        return self.read_diagnostics().get('failed_symbols')
    # *************************************************************************************

    # **************************************** Utility Functions ***************************
    def restart_warehouse(self, symbols):
        self.stocks = symbols
        self._create_rejected_field()

    def get_symbols(self):
        stocks_list = []
        for s in self.stocks:
            stocks_list.append(s["symbol"])
        return stocks_list

    def set_rejected(self, symbol):
        idx  = self._get_idx(symbol)
        self.stocks[idx]['rejected'] = True

    def set_rejected_inv(self, symbol):
        idx  = self._get_idx(symbol)
        self.stocks[idx]['rejected_inv'] = True

    def is_symbol_rejected(self, symbol):
        idx  = self._get_idx(symbol)
        try:
            return self.stocks[idx]['rejected']
        except:
            return False

    def is_symbol_rejected_inv(self, symbol):
        idx  = self._get_idx(symbol)
        try:
            return self.stocks[idx]['rejected_inv']
        except:
            return False
    
    def _get_stocks_for_tv(self, sector="", rejected_key="rejected", include_rejected=False):
        tv_stocks = []
        for s in self.stocks:
            #skip this stock if "include_rejected" is False and is rejected
            if (not include_rejected) and s[rejected_key]: continue
            
            #skip if sector is defined and the stock is not of this sector
            if (len(sector)!=0) and s.get('sector')!=sector: continue

            #TradingView does not what 'NYSE ARCA' is. It recognizes those symbols as part of "AMEX" exchange
            if s.get('exchange') == 'NYSE ARCA': 
                exch = 'AMEX'
            else:
                exch = s.get('exchange')
            tv_stocks.append(exch + ':' + s['symbol'])
        stocks_to_observe = ', '.join(tv_stocks)
        #logging.debug(f'TV String: {tv_stocks}')
        logging.debug(f'Stocks to observe: {stocks_to_observe}')
        return stocks_to_observe

    def get_stocks_for_tv(self, sector="", include_rejected=False):
        return self._get_stocks_for_tv(sector, 'rejected', include_rejected)

    def get_stocks_for_tv_inverted(self, sector="", include_rejected=False):
        return self._get_stocks_for_tv(sector, 'rejected_inv', include_rejected)
    # ****************************************************************************************