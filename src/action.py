from abc import ABC, abstractmethod

class IAction(ABC):
    # TODO: add type hints
    @abstractmethod
    def act(self, model, view):
        ...


class TestAction(IAction):
    # TODO: implement TestAction constructor
    def __init__(self, *params):
        assert False, 'Not implemented yet'
    
    # TODO: implement TestAction act
    def act(self, model, view):
        assert False, 'Not implemeted yet'
