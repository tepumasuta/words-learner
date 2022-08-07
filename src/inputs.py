from abc import ABC, abstractmethod
from action import IAction, TestAction
from parser import PARSER

class IInput(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def get_action(self, args: list[str]) -> IAction:
        ...

    @abstractmethod
    def question(self, display: "IDisplay"):
        ...

class TerminalInput(IInput):
    def __init__(self):
        ...

    def get_action(self, args: list[str]) -> IAction:
        ns = PARSER.parse_args(args)
        
        if 'test' in ns:
            return TestAction(ns.db)

        # TODO: implement database action

    def question(self, display: "TerminalDisplay", string: str | None = None):
        if string is not None:
            display.print(string)

        return input()
