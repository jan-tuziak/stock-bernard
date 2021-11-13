'''Class responsible for handling criterias, acting as an interface between the program and criteras'''

import config

from src.criterias.sma_sma_criteria import SmaSmaCriteria
from src.criterias.sma_sma_1_in_many_criteria import SmaSma1InManyCriteria

class CriterasHandler:
    def __init__(self, warehouse, data_source=None):
        self._data_source = data_source
        self._warehouse = warehouse
        self._criterias = self._create_criterias(config.criterias)

    def _create_criterias(self, criterias):
        cls_criterias = []
        for c in criterias:
            if c['type'] == 'sma_x > sma_y':
                cls_criterias.append(SmaSmaCriteria(**c['parameters']))
            elif c['type'] == 'sma_x > sma_y 1inMany':
                cls_criterias.append(SmaSma1InManyCriteria(**c['parameters']))
            else:
                raise Warning(f'Invalid Criteria: "{c}". Criteria type "{c["type"]}" is invalid.')
        return cls_criterias
    
    def check_symbol(self, symbol):
        if not self._warehouse.is_symbol_rejected(symbol):
            passed = []
            for c in self._criterias:
                passed.append(c.check_symbol(self._warehouse, symbol))
            return all(p == True for p in passed)
        else:
            return False

    def add_needed_data_for_crits(self):
        for c in self._criterias:
            c.add_needed_data(self._warehouse, self._data_source)

    def check_against_crits(self):
        for symbol in self._warehouse.get_symbols():
            if self._warehouse.is_symbol_rejected(symbol): continue
            if self.check_symbol(symbol) == False: self._warehouse.set_rejected(symbol)