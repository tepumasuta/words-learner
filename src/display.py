from abc import ABC, abstractmethod

class IDisplay(ABC):
    @staticmethod
    @abstractmethod
    def print(self, str: str):
        ...

    @staticmethod
    @abstractmethod
    def error(self,  str: str):
        ...

    @staticmethod
    @abstractmethod
    def log(self,  str: str):
        ...        