from abc import ABC, abstractmethod
from sys import stderr

class IDisplay(ABC):
    @staticmethod
    @abstractmethod
    def print(string: str):
        ...

    @staticmethod
    @abstractmethod
    def error(string: str):
        ...

    @staticmethod
    @abstractmethod
    def log(string: str):
        ... 

class TerminalDisplay(IDisplay):
    @staticmethod
    def print(string: str):
        print(string)

    @staticmethod
    def error(string: str):
        print('[ERROR]', string, file=stderr)

    @staticmethod
    def log(string: str):
        print('[INFO]', string)
