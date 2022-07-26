from abc import ABC, abstractmethod

from action import IAction

class IInput(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    @staticmethod
    def get_action(self) -> IAction:
        ...