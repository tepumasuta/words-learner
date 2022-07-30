from abc import ABC, abstractmethod

class IDisplay(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def print(self):
        ...

    @abstractmethod
    def error(self):
        ...

    @abstractmethod
    def log(self):
        ...        