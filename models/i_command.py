from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def get_command(self):
        pass

    @abstractmethod
    def get_hex_command(self):
        pass
