from abc import ABC, abstractmethod


class ISerializable(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        ...
    
    @staticmethod
    @abstractmethod
    def deserialize(raw: dict) -> 'ISerializable':
        ...
