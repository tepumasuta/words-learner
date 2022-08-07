from abc import ABC, abstractmethod
from database import Database
from app import Model, View

class IAction(ABC):
    @abstractmethod
    def act(self, model: Model, view: View):
        ...


class PerformTestAction(IAction):
    def __init__(self, keys: list[str], database: Database):
        self.result = []
        self._keys = keys
        self._data = database
    
    def act(self, model: Model, view: View):
        for key in self._keys:
            expected_values = set(self._data[key].contents)
            answer = view.input.question(f'{key}\n')
            self.result.append((key, answer, answer in expected_values, expected_values))


class ResultTestAction(IAction):
    def __init__(self, results: list[str, str, bool, list[str]]):
        self._results = results
    
    def act(self, model: Model, view: View):
        total_score = sum(entry[2] for entry in self.result)
        max_score = len(self._results)
        percentage = 100 * total_score / max_score
        wrong = list(filter(lambda x: x[2], self._results))
        
        view.display.print(f'\nAnswered correctly: {total_score}/{max_score} ({percentage:.1f})\n')
        view.display.print('Guessed wrong:')
        for key, answer, _, expected in wrong:
            view.display.print(f'{key} - {answer} (expected: {", ".join(expected)})\n')
