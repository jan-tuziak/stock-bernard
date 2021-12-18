'''Informal Interface for Criteria Classes'''

class ICriteria:
    def check_symbol(self, warehouse, symbol):
        return NotImplementedError

    def add_needed_data(self, warehouse, data_source):
        return NotImplementedError

    def check_symbol_inv(self, warehouse, symbol):
        result = self.check_symbol(warehouse, symbol)
        return not result