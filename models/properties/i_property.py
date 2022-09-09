from abc import ABC, abstractmethod


class IProperty(ABC):
    @abstractmethod
    def get_hex_string(self):
        pass
