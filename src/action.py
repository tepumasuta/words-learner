from abc import ABC, abstractmethod
from database import Database
from collections import namedtuple

class IAction(ABC):
    @abstractmethod
    def act(self, model: 'Model', view: 'View'):
        ...


class PerformTestAction(IAction):
    def __init__(self, keys: list[str], database: Database):
        self.result = []
        self._keys = keys
        self._data = database
    
    def act(self, model: 'Model', view: 'View'):
        for key in self._keys:
            expected_values = set(self._data[key].contents)
            answer = view.input.question(key)
            self.result.append((key, answer, answer in expected_values, expected_values))
