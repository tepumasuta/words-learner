from abc import ABC, abstractmethod
import argparse
from action import *
from parser import PARSERS, get_help

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
        # TODO: implement get_help()
        if not args:
            return ChainAction(ErrorAction('No arguments provided'),
                               PrintAction(get_help()))

        for parser in PARSERS:
            try:
                ns = parser.parse_args(args)
                break
            except (argparse.ArgumentError, argparse.ArgumentTypeError) as _:
                continue
        else:
            # TODO: implement get_help()
            return ChainAction(ErrorAction(f'Unknown action: {args[0]}'),
                               PrintAction(get_help()))

        if 'test' in ns: return TestAction(ns.db)
        if 'get' in ns: return GetAction(ns.db, ns.key)
        if 'add' in ns: return AddAction(ns.db, ns.key, ns.values)
        # TODO: implement RemoveAction
        if 'rm' in ns: return RemoveAction(ns.db, ns.key, ns.values)
        if 'list' in ns: return ListDatabasesAction(ns.dbs)
        if 'create' in ns: return CreateDatabaseAction(ns.db, ns.db_path, ns.db_alias or ns.db)
        if 'print' in ns: return PrintDatabaseAction(ns.db)
        if 'attach' in ns: return AttachAction(ns.db_alias, ns.db_path)
        if 'detach' in ns: return DetachAction(ns.db)

    def question(self, display: "TerminalDisplay", string: str | None = None):
        if string is not None:
            display.print(string)

        return input()
