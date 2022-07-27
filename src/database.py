import datetime
import os
import pathlib
from dataclasses import dataclass, field, asdict
from typing import Any
from serialize import ISerializable, ISerializer


def _type_check(*params: tuple[Any, type, str, str]):
    for var, var_type, var_name, var_type_name in params:
        if not isinstance(var, var_type):
            raise TypeError(f"{var_name} must be {var_type_name}. Recieved `{var}` of type {type(var)}")

@dataclass(slots=True)
class Record(ISerializable):
    mapped_word: str
    contents: list[str] = field(default_factory=list)
    last_update_date: datetime.date = field(default_factory=datetime.date.today)
    repeated_times: int = 0

    def serialize(self) -> dict:
        return asdict(self)

    @staticmethod
    def deserialize(raw: dict) -> 'Record':
        return Record(raw['mapped_word'],
                      raw['contents'],
                      raw['last_update_date'],
                      raw['repeated_times'])

    def copy(self):
        return Record(
            self.mapped_word,
            list(self.contents),
            self.last_update_date,
            self.repeated_times,
        )


class Database:
    def __init__(self, path: pathlib.Path, serializer: ISerializer, name: str, data: dict[str, Record]):
        self._path = path
        self._serializer = serializer
        self._name: str = name
        self._data: dict[str, Record] = data
    
    @staticmethod
    def load(path: pathlib.Path, serializer: ISerializer) -> 'Database':
        if not os.path.exists(path):
            raise FileNotFoundError()

        name, data = map(ISerializable.deserialize,
                         serializer.deserialize_list(path))

        return Database(path, serializer, name, data)

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> pathlib.Path:
        return self._path

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str, default_value: Any) -> tuple[Record, ...] | Any:
        _type_check((key, str, 'Key', 'a string'))
        
        if key not in self:
            return default_value
        
        return tuple(entry.copy() for entry in self._data[key])

    def __getitem__(self, key: str) -> tuple[Record, ...]:
        _type_check((key, str, 'Key', 'a string'))

        if key not in self:
            raise KeyError(f"Key `{key}` not found")

        return tuple(entry.copy() for entry in self._data[key])

    def add(self, key: str, value: str, date: datetime.date = None, repeated_times: int = 0):
        if date is None:
            date = datetime.date.today()

        _type_check((key, str, 'Key', 'a string'),
                    (value, str, 'Value', 'a string'),
                    (date, datetime.date, 'Date', 'a date'),
                    (repeated_times, int, 'Repeated times', 'int'))

        if key in self and value in key[self]:
            raise ValueError(f"Value is already in database at {key}. Trying to override it with `{value}`")
        if repeated_times < 0:
            raise ValueError(f'Repeated times must be greater than 0. Received: {repeated_times}')
        
        if key not in self:
            self._data[key] = Record(key, [value], date, repeated_times)
            return

        self._data[key].contents.append(value)
        self._data[key].last_update_date = date
        self._date[key].repeated_times = repeated_times

    def remove(self, key: str, value: str | None = None):
        _type_check((key, str, 'Key', 'a string'),
                    (value, str | None, 'Value', 'a string or None'))

        if key not in self:
            raise KeyError(f'Key `{key}` not found')

        if value is None:
            self._data.pop(key)
            return

        try:
            self._data[key].contents.remove(value)
        except ValueError:
            raise KeyError(f'Value `{value}` not found at {key}')
        
    def dump(self):
        self._serializer.serialize_list([self._name, self._data], self._path)


class DatabasesView:
    def __init__(self, links: dict[str, list[tuple[Database, dict]]], *databases):
        self._databases: dict[str, Database] = {db.name: db for db in databases}
        self._links = links
    
    def update(self, db_name: str, key: str, values: list[str], parameters: dict[str, Any] = None):
        _type_check((db_name, str, 'Database name', 'a string'))
        
        # TODO: implement parameters
        if parameters is not None:
            assert False, "Not implemeted yet"
        
        if db_name not in self._databases:
            raise KeyError(f"Database `{db_name}` not found")
        
        db = self._databases[db_name]
        for value in values:
            db.add(key, value)
    
    def get(self, db_name: str, key: str):
        _type_check((db_name, str, 'Database name', 'a string'))
        
        if db_name not in self._databases:
            raise KeyError(f"Database `{db_name}` not found")
        
        return self._databases[db_name].get(key)
    
    def link(self, db_name_from: str, db_name_to: str, reverse: bool = False):
        _type_check((db_name_from, str, 'Database name', 'a string'),
                    (db_name_to, str, 'Database name', 'a string'),
                    (reverse, bool, 'Reverse', 'a bool'))
        
        if db_name_from not in self._databases:
            raise KeyError(f"Database `{db_name_from}` not found")
        if db_name_to not in self._databases:
            raise KeyError(f"Database `{db_name_to}` not found")
        
        self._links[db_name_from].append((self._databases[db_name_to], {reverse: reverse}))
    
    def unlink(self, db_name_from: str, db_name_to: str):
        _type_check((db_name_from, str, 'Database name', 'a string'),
                    (db_name_to, str, 'Database name', 'a string'))

        if db_name_from not in self._databases:
            raise KeyError(f"Database `{db_name_from}` not found")
        if db_name_to not in self._databases:
            raise KeyError(f"Database `{db_name_to}` not found")
        
        if db_name_to not in map(lambda x: x[0], self._links[db_name_from]):
            raise ValueError(f"Database {db_name_from} is not linked to {db_name_to}")
        
        for i, x in enumerate(map(lambda x: x[0], self._links[db_name_from])):
            if x == db_name_to:
                break
        
        self._links[db_name_from].pop(i)
    
    def remove(self, db_name: str, key: str, value: str | None):
        _type_check((db_name, str, 'Database name', 'a string'))
        
        if db_name not in self._databases:
            raise KeyError(f"Database `{db_name}` not found")
        
        self._databases[db_name].remove(key, value)

    def dump(self):
        for db in self._databases.values():
            db.dump()
    
    def delete(self, db_name: str):
        _type_check((db_name, str, 'Database name', 'a string'))
        
        if db_name not in self._databases:
            raise KeyError(f"Database `{db_name}` not found")
        
        path = self._databases[db_name].path
        
        if db_name in self._links:
            self._links.pop(db_name)
        db = self._databases[db_name]
        for key, val in self._links.items():
            if db in map(lambda x: x[0], val):
                for i, val in enumerate(map(lambda x: x[0], val)):
                    if val == db:
                        break
                self._links[key].pop(i)
        self._databases.pop(db_name)
        os.remove(path)
    
    def detach(self, db_name: str):
        _type_check((db_name, str, 'Database name', 'a string'))
        
        if db_name not in self._databases:
            raise KeyError(f"Database `{db_name}` not found")
        
        if db_name in self._links:
            self._links.pop(db_name)
        db = self._databases[db_name]
        for key, val in self._links.items():
            if db in map(lambda x: x[0], val):
                for i, val in enumerate(map(lambda x: x[0], val)):
                    if val == db:
                        break
                self._links[key].pop(i)
        self._databases.pop(db_name)
