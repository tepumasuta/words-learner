from abc import ABC, abstractmethod
from action import IAction

class IInput(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def get_action(self) -> IAction:
        ...

    @abstractmethod
    def question(self, display: "IDisplay"):
        ...

class TerminalInput(IInput):
    def __init__(self):
        ...

    def get_action(self) -> IAction:
        #VOVA
        ...

    def question(self, display: "TerminalDisplay", string: str | None = None):
        if string is not None:
            display.print(string)
        
        return input()

