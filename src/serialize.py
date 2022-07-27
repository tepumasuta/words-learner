import pathlib
import os
import pickle
from abc import ABC, abstractmethod


class ISerializable(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        ...
    
    @staticmethod
    @abstractmethod
    def deserialize(raw: dict) -> 'ISerializable':
        ...


class ISerializer(ABC):
    @staticmethod
    @abstractmethod
    def serialize_list(obj: list[ISerializable | str], path: pathlib.Path):
        ...
    
    @staticmethod
    @abstractmethod
    def deserialize_list(path: pathlib.Path) -> list[ISerializable]:
        ...


class PickleSerializer(ISerializer):
    @staticmethod
    def serialize_list(objs: list[ISerializable | str], path: pathlib.Path):
        def is_special(obj) -> bool:
            return isinstance(obj, str)
        
        if not os.path.exists(path):
            raise OSError()
        
        with open(path) as out:
            pickle.dump([obj.serialize() if not is_special(obj) else obj for obj in objs], out)
    
    @staticmethod
    def deserialize_list(path: pathlib.Path) -> list[ISerializable]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File `{path}` not found")
        
        res: list[ISerializable]
        with open(path) as data:
            res = pickle.load(data)

        return res
