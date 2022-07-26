from abc import ABC, abstractmethod
import pathlib


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
    def serialize_list(obj: list[ISerializable], path: pathlib.Path):
        ...
    
    @staticmethod
    @abstractmethod
    def deserialize_list(path: pathlib.Path) -> list[ISerializable]:
        ...
