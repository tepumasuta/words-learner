from abc import ABC, abstractmethod

from action import IAction
from database import Database

class ITestmethod(ABC):
    @abstractmethod
    def test(self, data: Database) -> IAction:
        ...