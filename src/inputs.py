from abc import ABC, abstractmethod
import argparse
from action import *
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
        # TODO: implement error action return
        if not args:
            ...
            return IAction()

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
        if 'get' in ns: return GetAction(ns.db, ns.key)
        # TODO: implement AddAction
        if 'add' in ns: return AddAction(ns.db, ns.key, ns.values)
        # TODO: implement RemoveAction
        if 'rm' in ns: return RemoveAction(ns.db, ns.key, ns.values)
        if 'list' in ns: return ListDatabasesAction(ns.dbs)
        if 'create' in ns: return CreateDatabaseAction(ns.db, ns.db_path, ns.db_alias or ns.db)

        # TODO: implement database action

    def question(self, display: "TerminalDisplay", string: str | None = None):
        if string is not None:
            display.print(string)

        return input()
