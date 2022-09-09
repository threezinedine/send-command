import unittest
from unittest.mock import Mock
from models.properties import Property
from models import Command
from views import ITextSource



class TestSendCommandEndToEnd(unittest.TestCase):
    def test_create_stop_command(self):
        function_source = Mock(spec=ITextSource)
        function_source.get_text.return_value = "6"

        address_property = Property(num_bytes=2, text_source=function_source)
        command = Command("stop", address_property)

        result = command.get_command()

        expected = "30 30 00 00 00 22 01 06 00 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
        self.assertEqual(result, expected)
