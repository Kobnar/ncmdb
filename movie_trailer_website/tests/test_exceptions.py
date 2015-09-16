__author__ = 'kobnar'
from unittest import TestCase


class ValidationErrorTests(TestCase):
    def setUp(self):
        from ..exceptions import ValidationError
        self.error = ValidationError('test_field', 'invalid_value')
        self.expected_msg = 'Invalid value for \'test_field\': invalid_value'

    def test_field_set(self):
        self.assertEqual('test_field', self.error.field)

    def test_value_set(self):
        self.assertEqual('invalid_value', self.error.value)

    def test_msg_set(self):
        self.assertEqual(self.expected_msg, self.error.msg)

    def test_str_set(self):
        self.assertEqual(self.expected_msg, str(self.error))

    def test_repr_set(self):
        self.assertEqual(self.expected_msg, repr(self.error))
