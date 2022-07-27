import random
from action import IAction
from database import Database
from test_method import ITestmethod


class BasicTestmethod(ITestmethod):
    def __init__(self, data: Database):
        self.data = data
        self.amount_keys = 20
        self.list_keys = []

    def test(self) -> IAction:
        while self.amount_keys != 0:
            if len(self.list_keys) <= 20:
                break

            ran_choice = random.choice(self.data.keys())
            if self.amount_keys <= len(self.data.keys()) and not BasicTestmethod.repeat(ran_choice):
                self.list_keys.append(ran_choice)

            elif self.amount_keys > len(self.data.keys()) and not BasicTestmethod.repeat(ran_choice):       
                self.list_keys.append(ran_choice)
                self.amount_keys -= 1

        return tuple(self.list_keys)

    def repeat(self, key):
        return key in self.list_keys
