from os import remove
from typing import Final, cast
from unittest import TestCase

from dao.sqlite_dao import SqliteDAO
from dispatcher.dispatcher import DispatchService
from helpers import config as config_helper
from listener.preprocessor import Preprocessor
from responder.responder import ResponseService
from test_mocks.speaker import MockSpeaker


class EndToEndTests(TestCase):
    test_db_name: Final = "test.db"

    def setUp(self):
        self.db = SqliteDAO(self.test_db_name)
        self.settings = cast(
            dict, config_helper.load_config("./test_mocks/config.toml")
        )
        assert self.db.try_init_db_if_needed()
        assert self.settings is not None
        self.preprocessor = Preprocessor(self.settings["listening"]["replacements"])

    def tearDown(self):
        remove(self.test_db_name)

    def test_eat_same_food(self):
        data: Final[dict] = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)

        dispatcher: Final = DispatchService(
            self.preprocessor,
            ResponseService(self.db, speaker),
            self.settings["listening"]["keywords"],
            "John",
        )

        dispatcher.dispatch("eat fish")
        self.assertEqual("What is the energy value of fish?", data["message"])

        dispatcher.dispatch("five hundred and ten")
        self.assertEqual("Adding fish at 510", data["message"])

        dispatcher.dispatch("eat fish")
        self.assertEqual("Same fish as last time?", data["message"])

        dispatcher.dispatch("no")
        self.assertEqual("What is the energy value of fish?", data["message"])

        dispatcher.dispatch("three hundred and ten")
        self.assertEqual("Adding fish at 310", data["message"])

        dispatcher.dispatch("eat fish")
        self.assertEqual("Same fish as last time?", data["message"])

        dispatcher.dispatch("yes")
        self.assertEqual("Adding fish at 310", data["message"])

        dispatcher.dispatch("how much did I eat so far?")
        self.assertEqual(
            "So far today you have consumed 1130 energy units", data["message"]
        )

    def test_undo(self):
        data: Final[dict] = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)

        dispatcher: Final = DispatchService(
            self.preprocessor,
            ResponseService(self.db, speaker),
            self.settings["listening"]["keywords"],
            "John",
        )

        dispatcher.dispatch("eat fish")
        self.assertEqual("What is the energy value of fish?", data["message"])

        dispatcher.dispatch("five hundred and ten")
        self.assertEqual("Adding fish at 510", data["message"])

        dispatcher.dispatch("undo")
        self.assertEqual("Ok, I removed the last entry", data["message"])

        dispatcher.dispatch("how much did I eat so far?")
        self.assertEqual(
            "So far today you have consumed 0 energy units", data["message"]
        )

    def test_nevermind(self):
        data: Final[dict] = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)

        dispatcher: Final = DispatchService(
            self.preprocessor,
            ResponseService(self.db, speaker),
            self.settings["listening"]["keywords"],
            "John",
        )

        dispatcher.dispatch("eat fish")
        self.assertEqual("What is the energy value of fish?", data["message"])

        dispatcher.dispatch("never mind")
        self.assertEqual("Ok", data["message"])

    def test_empty_food(self):
        data: Final[dict] = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)

        dispatcher: Final = DispatchService(
            self.preprocessor,
            ResponseService(self.db, speaker),
            self.settings["listening"]["keywords"],
            "John",
        )

        dispatcher.dispatch("eat")
        self.assertEqual(
            "I couldn't catch that, what were you saying?", data["message"]
        )

        dispatcher.dispatch("never mind")
        self.assertEqual("Ok", data["message"])

    def test_name(self):
        data: Final[dict] = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)

        dispatcher: Final = DispatchService(
            self.preprocessor,
            ResponseService(self.db, speaker),
            self.settings["listening"]["keywords"],
        )

        dispatcher.dispatch("hi")
        self.assertEqual(
            "Hello, I will help you keep track what you eat, what's your name?",
            data["message"],
        )

        dispatcher.dispatch("hi")
        self.assertEqual(
            "Dude, just tell me what to call you",
            data["message"],
        )

        dispatcher.dispatch("i'm")
        self.assertEqual(
            "I couldn't catch that, what were you saying?", data["message"]
        )

        dispatcher.dispatch("i'm test")
        self.assertEqual("Hi test", data["message"])
