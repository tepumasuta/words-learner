import datetime
import os
from dataclasses import dataclass, field, asdict
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
