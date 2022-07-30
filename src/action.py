from abc import ABC, abstractmethod
from app import Model

class IAction(ABC):
    # TODO: add type hints
    @abstractmethod
    def act(self, model: Model, view):
        ...


class TestAction(IAction):
    # TODO: implement TestAction constructor
    def __init__(self, *params):
        assert False, 'Not implemented yet'
    
    # TODO: implement TestAction act
    def act(self, model: Model, view):
        assert False, 'Not implemeted yet'
