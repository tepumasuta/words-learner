import random
from abc import ABC, abstractmethod
from action import IAction, TestAction
from database import Database


class ITestmethod(ABC):
    @abstractmethod
    def test(self, data: Database) -> IAction:
        ...


class BasicTestmethod(ITestmethod):
    KEYS_AMOUNT = 20
    
    def __init__(self):
        self.amount_keys = BasicTestmethod.KEYS_AMOUNT
        self.list_keys = []

    def test(self, data: Database) -> TestAction:
        while self.amount_keys != 0:
            if len(self.list_keys) <= BasicTestmethod.KEYS_AMOUNT:
                break

            ran_choice = random.choice(data.keys())
            if ran_choice not in self.list_keys:
                self.list_keys.append(ran_choice)
                
                if self.amount_keys > len(data.keys()):
                    self.amount_keys -= 1

        return TestAction(self.list_keys)
