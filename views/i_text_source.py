from abc import ABC, abstractmethod
from functools import partial


class ITextChangable(ABC):
    @abstractmethod
    def connect(self, callback, data):
        pass

    @abstractmethod
    def toggle_state(self):
        pass

    @abstractmethod
    def reset(self):
        pass


class ITextSource(ABC):
    @abstractmethod
    def get_text(self) -> str:
        pass

    @abstractmethod
    def set_text(self, text:str):
        pass


class TextSource(ITextSource, ITextChangable):
    def __init__(self, source):
        self.__source = source
        self.__source.setReadOnly(True)

    def get_text(self):
        return self.__source.text()

    def toggle_state(self, state):
        self.__source.setReadOnly(state)

    def connect(self, callback):
        self.__source.textChanged.connect(callback)

    def reset(self):
        self.__source.setText("")
        self.__source.setReadOnly(True)

    def set_text(self, text):
        self.__source.setText(text)
