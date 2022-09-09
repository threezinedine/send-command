import unittest
from utils import convert_string_to_hex, convert_hex_to_string



class TestUtils(unittest.TestCase):
    def test_convert_string_to_hex(self):
        string = "30 30 00 01 06"
        assert convert_string_to_hex(string) == b'\x30\x30\x00\x01\x06'

    def test_convert_hex_to_string(self):
        hexStr = b'\x30\x30\x00\x01\x06'
        assert convert_hex_to_string(hexStr) == "30 30 00 01 06"
