from unittest import TestCase

from helpers import config as config_helper
from listener.preprocessor import Preprocessor


class TestInterpreter(TestCase):
    def setUp(self):
        settings = config_helper.load_config("./test_mocks/config.toml")
        assert settings is not None
        self.preprocessor = Preprocessor(settings["listening"]["replacements"])

    def test_addition(self):

        self.assertEqual("4+5", self.preprocessor.text_to_math("four plus five"))
        self.assertEqual(
            "4+5+2+900+87+123",
            self.preprocessor.text_to_math(
                "four plus five plus two plus nine hundred and eighty seven plus one hundred twenty three"
            ),
        )

    def test_ignoring_start_text(self):
        self.assertEqual(
            "4+5", self.preprocessor.text_to_math("what is four plus five")
        )

    def test_fractions(self):
        self.assertEqual(
            "3*0.25*300",
            self.preprocessor.text_to_math("three quarters times three hundred"),
        )

    def test_1000_by_2(self):
        self.assertEqual(
            "1000/2", self.preprocessor.text_to_math("a thousand divided by two")
        )
