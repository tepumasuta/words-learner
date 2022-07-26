from abc import ABC, abstractmethod

class IAction(ABC):
    @abstractmethod
    def act(self):
        ...