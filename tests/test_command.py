import unittest
from unittest.mock import Mock
from models.properties import IProperty
from models import Command


class TestCommand(unittest.TestCase):
    def test_stop_command_generates_human_interface_string(self):
        expected = "30 30 00 00 00 22 01 06 00 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
        address_property = Mock(spec=IProperty)
        address_property.get_hex_string.return_value = "00 06"
        stop_command = Command("stop", address_property)

        generated_string = stop_command.get_command()

        self.assertEqual(generated_string, expected)

    def test_stop_command_generates_hex_string(self):
        expected = b'\x30\x30\x00\x00\x00\x22\x01\x06\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        address_property = Mock(spec=IProperty)
        address_property.get_hex_string.return_value = "00 06"
        stop_command = Command("stop", address_property)

        generated_string = stop_command.get_hex_command()

        self.assertEqual(generated_string, expected)

    def test_reset_command_generates_human_inteface_string(self):
        expected = "30 30 00 00 00 22 01 06 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
        address_property = Mock(spec=IProperty)
        address_property.get_hex_string.return_value = "00 04"
        reset_command = Command("reset", address_property)

        generated_string = reset_command.get_command()

        self.assertEqual(generated_string, expected)
        
    def test_run_command_generates_human_interface_string_with_fifth_parameter(self):
        expected = "30 30 00 00 00 22 01 06 00 05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 00"
        address_property = Mock(spec=IProperty)
        address_property.get_hex_string.return_value = "00 05"

        fifth_param = Mock(spec=IProperty)
        fifth_param.get_hex_string.return_value = "00 00 00 03"

        run_command = Command("run", address_property, [None, None, None, None, fifth_param, None])

        generated_string = run_command.get_command()

        self.assertEqual(generated_string, expected)


    def test_read_encoder_command_generates_human_interface_string_with_fifth_and_sixth_parameter(self):
        expected = "30 30 00 00 00 22 01 06 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 05 00 00 00 23"
        address_property = Mock(spec=IProperty)
        address_property.get_hex_string.return_value = "00 0e"

        fifth_param = Mock(spec=IProperty)
        fifth_param.get_hex_string.return_value = "00 00 00 05"

        sixth_param = Mock(spec=IProperty)
        sixth_param.get_hex_string.return_value = "00 00 00 23"

        read_encoder_command = Command("read_encoder_command", address_property, [None, None, None, None, fifth_param, sixth_param])

        generated_string = read_encoder_command.get_command()

        self.assertEqual(generated_string, expected)
