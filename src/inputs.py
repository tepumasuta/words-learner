from abc import ABC, abstractmethod

class IInput(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def get_action(self) -> 'IAction':
        ...

    @abstractmethod
    def question(self, display: "IDisplay"):
        ...

class TerminalInput(IInput):
    def __init__(self):
        ...

    # TODO: implement get action
    def get_action(self) -> 'IAction':
        ...

    def question(self, display: "TerminalDisplay", string: str | None = None):
        if string is not None:
            display.print(string)

        return input()
