from abc import ABC, abstractmethod


class TemporaryStorage(ABC):

    @abstractmethod
    def get(self, name: str):
        ...

    @abstractmethod
    def set_value(self, name: str, new_value: float):
        ...
