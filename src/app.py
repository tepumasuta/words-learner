import os
from pickle import PickleBuffer
import yaml
import pathlib
from dataclasses import dataclass
from action import IAction
from database import DatabasesView
from display import IDisplay, TerminalDisplay
from inputs import IInput, TerminalInput
from serialize import ISerializer, PickleSerializer
from common import _type_check


class Configuration:
    POSSIBLE_SETTINGS = 'databases', 'test', 'db-format'
    DEFAULT_PATH = os.path.expanduser('~/.wordslearner/config.yaml')
    
    def __init__(self, settings: dict | None = None):
        self.settings = settings or {'databases': [], 'test': 'default', 'db-format': 'pickle'}
    
    @staticmethod
    def from_path(path: pathlib.Path) -> 'Configuration':
        _type_check((path, pathlib.Path | str, 'Path', 'a path'))
        
        if not os.path.exists(path):
            raise OSError()
        
        with open(path) as file:
            data: dict = yaml.load(file, yaml.Loader)

        for setting in data:
            if setting not in set(Configuration.POSSIBLE_SETTINGS):
                raise ValueError(f'Wrong setting: {setting}')

        return Configuration(data)
    
    def update(self, settings: dict):
        _type_check((settings, dict, 'Settings', 'a dictionary'))
        
        for setting in settings:
            if setting not in set(Configuration.POSSIBLE_SETTINGS):
                raise ValueError(f'Wrong setting: {setting}')
        
        self.settings |= settings
    
    def dump(self):
        if not os.path.exists(os.path.expanduser('~/.wordslearner/')):
            os.mkdir(os.path.expanduser('~/.wordslearner/'))
        
        with open(Configuration.DEFAULT_PATH, 'w') as config:
            yaml.dump(self.settings, config)


@dataclass(slots=True)
class Model:
    serializer: ISerializer
    testmethod: 'ITestmethod'
    databases: DatabasesView
    configuration: Configuration


@dataclass(slots=True)
class View:
    display: IDisplay
    input: IInput


class Application:
    def __init__(self, input_device: IInput, model: Model, view: View):
        self._model = model
        self._view = view
        self._input_device = input_device

    @staticmethod
    def create(serializer: ISerializer, testmethod: 'ITestmethod', configuration: Configuration, display: IDisplay, input_device = IInput):
        return Application(Model(serializer, testmethod, DatabasesView({}), configuration), View(display, input_device), input_device) 

    def run(self):
        self.perform(self._input_device.get_action())

    @staticmethod
    def from_config(configuration: Configuration):
        dict_classes = {'pickle': PickleSerializer(), 'test': 'ITestmethod'}
        dict_classes[configuration.settings['db-format']]
        return Application.create(dict_classes[configuration.settings['db-format']], dict_classes[configuration.settings['test']], configuration, TerminalDisplay, TerminalInput)

    def perform(self, action: IAction):
        action.act(self._model, self._view)

    def exit(self):
        ...
    