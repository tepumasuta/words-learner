import datetime
import os
from dataclasses import dataclass, field, asdict
from typing import Any
from serialize import *


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
        
    def keys(self):
        return tuple(self._data.keys())
