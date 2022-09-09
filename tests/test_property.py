import unittest
from unittest.mock import Mock
from views import ITextSource
from models.properties import Property


class PropertyTest(unittest.TestCase):
    def test_convert_empty_string_from_text_source_to_2_bytes_property(self):
        text_source = Mock(spec=ITextSource)
        text_source.get_text.return_value = ""

        address_property = Property(num_bytes=2, text_source=text_source)

        expected = "00 00"

        result = address_property.get_hex_string()

        self.assertEqual(expected, result)

    def test_convert_pyqt_text_source_to_2_bytes_property(self):
        text_source = Mock(spec=ITextSource)
        text_source.get_text.return_value = "35"

        address_property = Property(num_bytes=2, text_source=text_source)

        expected = "00 23"

        result = address_property.get_hex_string()

        self.assertEqual(expected, result)

    def test_convert_pyqt_text_source_to_2_bytes_property(self):
        text_source = Mock(spec=ITextSource)
        text_source.get_text.return_value = "32"

        address_property = Property(num_bytes=2, text_source=text_source)

        expected = "00 20"

        result = address_property.get_hex_string()

        self.assertEqual(expected, result)

    def test_convert_text_source_to_3_bytes_property_with_4_bytes_result(self):
        text_source = Mock(spec=ITextSource)
        text_source.get_text.return_value = "323"

        address_property = Property(num_bytes=3, text_source=text_source)

        expected = "00 01 43"

        result = address_property.get_hex_string()

        self.assertEqual(expected, result)
