from .i_command import ICommand
from .properties import IProperty
from utils import convert_string_to_hex


class Command(ICommand):
    START_FRAME_BYTES = "30 30 00 00"
    LENGTH_FRAME_BYTES = "00 22 01 06"
    DEFAULT_LENGTH = 6

    def __init__(self, name:str, address:IProperty, params: [IProperty] = [None] * DEFAULT_LENGTH):
        self.__address = address
        self.__params = params

    def get_command(self):
        address_string = self.__address.get_hex_string()

        print(self.__params)
        param_strings = [param.get_hex_string() if param is not None else "00 00 00 00" for param in self.__params]
        print(f"Param String: {param_strings}")
        return f"{Command.START_FRAME_BYTES} {Command.LENGTH_FRAME_BYTES} {address_string} {' '.join(param_strings)}"

    def get_hex_command(self):
        command_str = self.get_command()
        return convert_string_to_hex(command_str)
