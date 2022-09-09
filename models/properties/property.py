from .i_property import IProperty
from views import ITextSource


class Property(IProperty):
    EMPTY_STRING = ""
    EMPTY_BYTES = "00"
    FILL_VALUE = "0"
    HEX_STRING_DELIMITER = " "
    BYTE_LENGTH = 2
    DEFAULT_VAL = "0"

    def __init__(self, num_bytes:int, text_source:ITextSource=None):
        self.__text_source = text_source
        self.__text_source.set_text(self.DEFAULT_VAL)
        self.__num_bytes = num_bytes

    def __is_full_format(self, hex_string):
        return len(hex_string) % self.BYTE_LENGTH != 0

    def __get_one_byte_by_index(self, hex_string, index):
        return hex_string[index: index + self.BYTE_LENGTH]

    def _convert_hex_string_to_right_format(self, hex_string):
        while self.__is_full_format(hex_string):
            hex_string = self.FILL_VALUE + hex_string

        return [self.__get_one_byte_by_index(hex_string, index * self.BYTE_LENGTH) for index in range(len(hex_string) // self.BYTE_LENGTH)]


    def _get_bytes_array(self):
        int_text = self.__text_source.get_text()

        if int_text == self.EMPTY_STRING:
            return [self.EMPTY_BYTES, self.EMPTY_BYTES]
        else: 
            int_value = int(self.__text_source.get_text())
            result_strs = self._convert_hex_string_to_right_format(str(hex(int_value))[2:])
            while len(result_strs) < self.__num_bytes:
                result_strs = [self.EMPTY_BYTES] + result_strs
            return result_strs


    def get_hex_string(self) -> str:
        print(self.HEX_STRING_DELIMITER.join(self._get_bytes_array()))
        return self.HEX_STRING_DELIMITER.join(self._get_bytes_array())
