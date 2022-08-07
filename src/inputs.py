from abc import ABC, abstractmethod
import argparse
from action import IAction, TestAction
from parser import PARSERS

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
        for parser in PARSERS:
            try:
                ns = parser.parse_args(args)
                break
            except (argparse.ArgumentError, argparse.ArgumentTypeError) as e:
                continue
        else:
            # TODO: implement error action return
            return IAction()
        
        if 'test' in ns: return TestAction(ns.db)
        if 'get' in ns: return GetAction(ns.key)
        if 'add' in ns: return AddAction(ns.key, ns.values)
        if 'rm' in ns: return RemoveAction(ns.key, ns.values)

        # TODO: implement database action

    def question(self, display: "TerminalDisplay", string: str | None = None):
        if string is not None:
            display.print(string)

        return input()
