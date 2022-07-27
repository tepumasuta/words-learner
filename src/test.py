import random
from abc import ABC, abstractmethod
from action import IAction
from database import Database


class ITestmethod(ABC):
    @abstractmethod
    def test(self, data: Database) -> IAction:
        ...


class BasicTestmethod(ITestmethod):
    KEYS_AMOUNT = 20
    
    def __init__(self, data: Database):
        self.data = data
        self.amount_keys = BasicTestmethod.KEYS_AMOUNT
        self.list_keys = []

    def test(self) -> IAction:
        while self.amount_keys != 0:
            if len(self.list_keys) <= BasicTestmethod.KEYS_AMOUNT:
                break

            ran_choice = random.choice(self.data.keys())
            if ran_choice not in self.list_keys:
                self.list_keys.append(ran_choice)
                
                if self.amount_keys > len(self.data.keys()):
                    self.amount_keys -= 1

        return tuple(self.list_keys)
