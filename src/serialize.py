import pathlib
import os
import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict


class ISerializable(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        ...
    
    @staticmethod
    @abstractmethod
    def deserialize(raw: dict) -> 'ISerializable':
        ...


@dataclass
class StringSerializabe(ISerializable):
    value: str
    
    def serialize(self) -> dict:
        return asdict(self)

    @staticmethod
    def deserialize(raw: dict) -> 'StringSerializabe':
        return StringSerializabe(raw['value'])

@dataclass
class DictSerializable(ISerializable):
    value: dict
    
    def serialize(self) -> dict:
        return asdict(self)

    @staticmethod
    def deserialize(raw: dict) -> 'StringSerializabe':
        return DictSerializable(raw['value'])

class ISerializer(ABC):
    @staticmethod
    @abstractmethod
    def serialize_list(obj: list[ISerializable], path: pathlib.Path):
        ...
    
    @staticmethod
    @abstractmethod
    def deserialize_list(path: pathlib.Path) -> list[ISerializable]:
        ...


class PickleSerializer(ISerializer):
    @staticmethod
    def serialize_list(objs: list[ISerializable], path: pathlib.Path):
        if not os.path.exists(path):
            raise OSError()
        
        with open(path, 'wb') as out:
            pickle.dump([obj.serialize() for obj in objs], out)
    
    @staticmethod
    def deserialize_list(path: pathlib.Path) -> list[ISerializable]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File `{path}` not found")
        
        res: list[ISerializable]
        with open(path, 'rb') as data:
            res = pickle.load(data)

        return res
