'''Class responsible for handling criterias, acting as an interface between the program and criteras'''

import config

from src.stocks_warehouse.json_warehouse import JsonWarehouse
from src.criterias.sma_sma_criteria import SmaSmaCriteria

class CriterasHandler:
    def __init__():
        self._warehouse = JsonWarehouse(config.json_path)
        self._warehouse.init_from_file()
        self._criterias = self._create_criterias(config.criterias)

    def _create_criterias(self, criterias):
        cls_criterias = []
        for c in criterias:
            if c['type'] == 'sma_x > sma_y':
                cls.cls_criterias.append(SmaSmaCriteria(self._warehouse, **c['parameters']))
            else:
                raise Warning(f'Invalid Criteria: "{c}". Criteria type "{type}" is invalid.')
        return cls_criterias
    
    def check_symbol(self, symbol):
        passed = []
        for c in self._criterias:
            passed.append(c.check_symbol(symbol))
        return all(p == True for p in passed)