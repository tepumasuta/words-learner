import datetime
import os
import pathlib
from dataclasses import dataclass, field, asdict
from typing import Any
from serialize import ISerializable, ISerializer


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
    def __init__(self, path: pathlib.Path, serializer: ISerializer) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError()

        self._path = path
        self._serializer = serializer

        self._data: dict[str, Record]
        self._name: str

        self._name, self._data = map(
            ISerializable.deserialize,
            serializer.deserialize_list(path))

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> pathlib.Path:
        return self._path

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str, default_value: Any) -> tuple[Record, ...] | Any:
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string. Recieved `{key}` of type `{type(key)}`")
        
        if key not in self:
            return default_value
        
        return tuple(entry.copy() for entry in self._data[key])

    def __getitem__(self, key: str) -> tuple[Record, ...]:
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string. Recieved `{key}` of type `{type(key)}`")

        if key not in self:
            raise KeyError(f"Key `{key}` not found")

        return tuple(entry.copy() for entry in self._data[key])

    def add(self, key: str, value: str, date: datetime.date = None, repeated_times: int = 0):
        if date is None:
            date = datetime.date.today()
        
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string. Recieved `{key}` of type `{type(key)}")
        if not isinstance(value, str):
            raise TypeError(f"Value must be a string. Recieved `{value}` of type `{type(value)}")
        if not isinstance(date, datetime.date):
            raise TypeError(f"Date must be a date. Recieved `{date}` of type `{type(date)}")
        if not isinstance(repeated_times, int):
            raise TypeError(f"Repeated times must be int. Recieved `{repeated_times}` of type `{type(repeated_times)}")
        
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
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string. Recieved `{key}` of type `{type(key)}")
        if value is not None and not isinstance(value, str):
            raise TypeError(f"Value must be a string or None. Recieved `{value}` of type `{type(value)}")
        
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
        if not isinstance(db_name, str):
            raise TypeError(f"Database name must be a string. Recieved `{db_name}` of type `{type(db_name)}")
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string. Recieved `{key}` of type `{type(key)}")
        if not all(isinstance(value, str) for value in values):
            raise TypeError(f"Values must contain only strings. Values: `{values}`")
        
        # TODO: implement parameters
        if parameters is not None:
            assert False, "Not implemeted yet"
        
        if db_name not in self._databases:
            raise KeyError(f"Database `{db_name}` not found")
        
        db = self._databases[db_name]
        for value in values:
            db.add(key, value)
    
    def get(self, db_name: str, key: str):
        if not isinstance(db_name, str):
            raise TypeError(f"Database name must be a string. Recieved `{db_name}` of type `{type(db_name)}")
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string. Recieved `{key}` of type `{type(key)}")
        
        if db_name not in self._databases:
            raise KeyError(f"Database `{db_name}` not found")
        
        db = self._databases[db_name]
        
        if key not in db:
            raise KeyError(f"Key `{key}` not found")
        
        return db.get(key)
    
    def link(self, db_name_from: str, db_name_to: str, reverse: bool = False):
        if not isinstance(db_name_from, str):
            raise TypeError(f"Database name must be a string. Recieved `{db_name_from}` of type `{type(db_name_from)}")
        if not isinstance(db_name_to, str):
            raise TypeError(f"Database name must be a string. Recieved `{db_name_to}` of type `{type(db_name_to)}")
        if not isinstance(reverse, bool):
            raise TypeError(f"Reverse must be a bool. Recieved `{reverse}` of type `{type(reverse)}")
        
        if db_name_from not in self._databases:
            raise KeyError(f"Database `{db_name_from}` not found")
        if db_name_to not in self._databases:
            raise KeyError(f"Database `{db_name_to}` not found")
        
        self._links[db_name_from].append((self._databases[db_name_to], {reverse: reverse}))
    
    def unlink(self, db_name_from: str, db_name_to: str):
        if not isinstance(db_name_from, str):
            raise TypeError(f"Database name must be a string. Recieved `{db_name_from}` of type `{type(db_name_from)}")
        if not isinstance(db_name_to, str):
            raise TypeError(f"Database name must be a string. Recieved `{db_name_to}` of type `{type(db_name_to)}")

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
        if not isinstance(db_name, str):
            raise TypeError(f"Database name must be a string. Recieved `{db_name}` of type `{type(db_name)}")
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string. Recieved `{key}` of type `{type(key)}")
        if value is not None and not isinstance(value, str):
            raise TypeError(f"Value must be a string or None. Recieved `{value}` of type `{type(value)}")
        
        if db_name not in self._databases:
            raise KeyError(f"Database `{db_name}` not found")
        
        db = self._databases[db_name]
        
        db.remove(key, value)
