'''Informal Interface for Criteria Classes'''

class ICriteria:
    def check_symbol(self, symbol):
        return NotImplementedError

    def add_needed_data(self):
        return NotImplementedError