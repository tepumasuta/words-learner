from abc import ABC, abstractmethod
from database import Database, Record


class IAction(ABC):
    @abstractmethod
    def act(self, model: 'Model', view: 'View'):
        ...


class TestAction(IAction):
    def __init__(self, database: str):
        self._db_name = database[0]
    
    def act(self, model: 'Model', view: 'View'):
        if self._db_name not in model.databases.get_db_names():
            ErrorAction(f'No such database `{self._db_name}` found').act(model, view)
            return
        
        db = model.databases.get_database(self._db_name)

        performed_action: PerformTestAction = model.testmethod.test(db)
        performed_action.act(model, view)
        result_action = ResultTestAction(performed_action.result)
        result_action.act(model, view)


class PerformTestAction(IAction):
    def __init__(self, keys: list[str], database: Database):
        self.result = []
        self._keys = keys
        self._data = database
    
    def act(self, model: 'Model', view: 'View'):
        for key in self._keys:
            expected_values = set(self._data[key].contents)
            answer = view.input.question(f'{key}\n')
            self.result.append((key, answer, answer in expected_values, expected_values))


class ResultTestAction(IAction):
    def __init__(self, results: list[str, str, bool, list[str]]):
        self._results = results
    
    def act(self, model: 'Model', view: 'View'):
        total_score = sum(entry[2] for entry in self.result)
        max_score = len(self._results)
        percentage = 100 * total_score / max_score
        wrong = list(filter(lambda x: x[2], self._results))
        
        view.display.print(f'\nAnswered correctly: {total_score}/{max_score} ({percentage:.1f})\n')
        view.display.print('Guessed wrong:')
        for key, answer, _, expected in wrong:
            view.display.print(f'{key} - {answer} (expected: {", ".join(expected)})\n')


class GetAction(IAction):
    def __init__(self, database: str, key: str):
        self._db_name = database
        self._key = key
    
    def act(self, model: 'Model', view: 'View'):
        if self._db_name not in model.databases.get_db_names():
            ErrorAction(f'No such database `{self._db_name}`').act(model, view)
            return

        db = model.databases.get(self._db_name)
        vals = db.get(self._key, f'No such key `{self._key}` found in database `{db.name}`')

        if isinstance(vals, Record):
            view.display.print(f'Found values: {", ".join(vals.contents)}')
        else:
            view.display.error(vals)


class ListDatabasesAction(IAction):
    def __init__(self, databases: list[str]):
        self._dbs = databases

    def act(self, model: 'Model', view: 'View'):
        if not self._dbs:        
            view.display.print('\n'.join(map(lambda x: '- ' + x, model.databases.get_db_names())))
            return

        db_names = set(model.databases.get_db_names())
        
        for db_name in self._dbs:
            if db_name not in db_names:
                view.display.error(f'No such database `{db_name}`')
                continue
            
            view.display.print(', '.joib(model.databases.get(db_name).keys()))

class ErrorAction(IAction):
    def __init__(self, err_msg: str | Exception):
        self._err_msg = err_msg
    
    def act(self, model: 'Model', view: 'View'):
        view.display.error(self._err_msg)


class PrintAction(IAction):
    def __init__(self, message: str):
        self._message = message

    def act(self, model: 'Model', view: 'View'):
        view.display.print(self._message)


class AddAction(IAction):
    def __init__(self, database: str, key: str, value: list):
        self._db_name = database
        self._key = key
        self._value = value
    
    def act(self, model: 'Model', view: 'View'):
        if self._db_name not in model.databases.get_db_names():
            ErrorAction(f'No such database `{self._db_name}`')
            return

        db = model.databases.get(self._db_name)
        for value in self._value:    
            try:
                db.add(self._key, value)
            except ValueError as e:
                ErrorAction(e).act(model, view)
        return

class PrintDatabaseAction(IAction):
    def __init__(self, db_name: str):
        self._db_name = db_name

    def act(self, model: 'Model', view: 'View'):
        try:
            db = model.databases.get_database(self._db_name)
        except KeyError as e:
            ErrorAction(e).act(model, view)

        for key, value in db:
            print(f"{key} - {', '.join(value)}")


class RemoveKeyAction(IAction):
    def __init__(self, key: str, value: str | None = None):
        self._key = key
        self._value = value

    def act(self, model: 'Model', view: 'View'):
        if self._value is None:
            Database.remove(self._key)
        else:
            ...

class ChainAction(IAction):
    def __init__(self, *actions: IAction):
        self._actions = actions
    
    def act(self, model: 'Model', view: 'View'):
        for action in self._actions:
            action.act(model, view)
