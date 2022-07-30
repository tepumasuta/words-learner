import random
from abc import ABC, abstractmethod
from action import IAction, PerformTestAction
from database import Database


class ITestmethod(ABC):
    @abstractmethod
    def test(self, data: Database) -> IAction:
        ...


class BasicTestmethod(ITestmethod):
    KEYS_AMOUNT = 20
    
    def __init__(self):
        self._amount_keys = BasicTestmethod.KEYS_AMOUNT

    def test(self, data: Database) -> PerformTestAction:
        if len(data.keys()) >= self._amount_keys:
            self._ran_choice = random.sample(data.keys(), self._amount_keys)
        else:
            self._ran_choice = random.sample(data.keys(), len(data.keys()))
        return PerformTestAction(self._ran_choice, data)
