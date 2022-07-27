from abc import ABC, abstractmethod

class IAction(ABC):
    # TODO: add type hints
    @abstractmethod
    def act(self, model, view):
        ...
