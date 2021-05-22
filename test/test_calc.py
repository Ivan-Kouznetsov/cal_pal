from unittest import TestCase

from math_interpreter.calc import calc


class TestInterpreter(TestCase):
    def test_addition(self):
        self.assertEqual(8, calc("4 + 4"))
        self.assertEqual(3, calc("1 + 1+1"))

    def test_subtraction(self):
        self.assertEqual(0, calc("4 - 4"))
        self.assertEqual(1, calc("1 + 1-1"))

    def test_many_operations(self):
        self.assertEqual(
            3025, calc("1 + 10 * 6 * 10 * 10 / 2 / 1 / 1 / 1 + 6 + 7 + 8 + 9 / (2 + 1)")
        )

    def test_invalid_operator(self):
        try:
            calc("1 +/* 10 * 6 / (2 + 1)")
        except Exception as e:
            self.assertEqual("next_term: Expected a token", str(e))

    def test_invalid_brackets(self):
        try:
            calc("1 + 10 * 6 / (2 + 1(")
        except Exception as e:
            self.assertEqual("next_term: Invalid syntax", str(e))

    # Edge cases

    def test_leading_decimal_point(self):
        self.assertEqual(20.1, calc(".1 + 10 * 6 / (2 + 1)"))

    def test_dangeling_decimal_point(self):
        self.assertEqual(21, calc("1. + 10 * 6 / (2 + 1)"))

    def test_extra_decimal_points(self):
        try:
            calc("1..0 + 10 * 6 / (2 + 1)")
        except Exception as e:
            self.assertEqual("parse: Invalid syntax", str(e))

    def test_illegal_char(self):
        try:
            calc("1$0 + 10 * 6 / (2 + 1)")
        except Exception as e:
            self.assertEqual("Illegal character '$'", str(e))
