from abc import ABC, abstractmethod

class IDisplay(ABC):
    @staticmethod
    @abstractmethod
    def print(str: str):
        ...

    @staticmethod
    @abstractmethod
    def error(str: str):
        ...

    @staticmethod
    @abstractmethod
    def log(str: str):
        ...        