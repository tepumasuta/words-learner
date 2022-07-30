from abc import ABC, abstractmethod

class IAction(ABC):
    @abstractmethod
    def act(self, model: 'Model', view: 'View'):
        ...


class TestAction(IAction):
    # TODO: implement TestAction constructor
    def __init__(self, *params):
        assert False, 'Not implemented yet'
    
    # TODO: implement TestAction act
    def act(self, model: 'Model', view):
        assert False, 'Not implemeted yet'
