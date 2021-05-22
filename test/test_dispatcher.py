from typing import Final
from unittest import TestCase

from dispatcher.dispatcher import DispatchService
from helpers import config as config_helper
from listener.preprocessor import Preprocessor
from responder.responder import ResponseService
from test_mocks.dao import MockDAO
from test_mocks.speaker import MockSpeaker


class TestDispatcher(TestCase):
    def setUp(self):
        settings: Final = config_helper.load_config("./test_mocks/config.toml")
        assert settings is not None
        self.keywords: dict = settings["listening"]["keywords"]
        self.preprocessor = Preprocessor(settings["listening"]["replacements"])

    #
    # Happy Path
    #

    def test_new_food_first_item(self):
        data: Final[dict] = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)
        db: Final = MockDAO(
            data,
            {
                "db_init": True,
                "daily_total": None,
                "remove_success": True,
                "fish": None,
            },
        )

        dispatcher: Final = DispatchService(
            self.preprocessor, ResponseService(db, speaker), self.keywords, "John"
        )

        dispatcher.dispatch("eat fish")
        self.assertEqual("What is the energy value of fish?", data["message"])

    def test_math(self):
        data: dict = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)
        db: Final = MockDAO(
            data,
            {
                "db_init": True,
                "daily_total": None,
                "remove_success": True,
                "fish": None,
            },
        )

        dispatcher: Final = DispatchService(
            self.preprocessor, ResponseService(db, speaker), self.keywords, "John"
        )

        dispatcher.dispatch("what's two plus two")
        self.assertEqual("It's 4", data["message"])

    #
    # Bad Input
    #

    def test_bad_math(self):
        data: dict = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)
        db: Final = MockDAO(
            data,
            {
                "db_init": True,
                "daily_total": None,
                "remove_success": True,
                "fish": None,
            },
        )

        dispatcher: Final = DispatchService(
            self.preprocessor, ResponseService(db, speaker), self.keywords, "John"
        )

        dispatcher.dispatch("what's aaaaaa")
        self.assertEqual(
            "I couldn't catch that, what were you saying?", data["message"]
        )

        dispatcher.dispatch("what's")
        self.assertEqual(
            "I couldn't catch that, what were you saying?", data["message"]
        )
