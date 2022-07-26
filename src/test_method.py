from abc import ABC, abstractmethod

from action import IAction

class ITestmethod(ABC):
    @abstractmethod
    def test(self) -> IAction:
        ...