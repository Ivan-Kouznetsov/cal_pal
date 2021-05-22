from typing import Final
from unittest import TestCase

from responder.responder import ResponseService
from test_mocks.dao import MockDAO
from test_mocks.fail_dao import MockFailDAO
from test_mocks.speaker import MockSpeaker


class TestResponder(TestCase):
    def test_never_mind(self):
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

        responder: Final = ResponseService(db, speaker)

        responder.never_mind()
        self.assertEqual("Ok", data["message"])

    def test_set_energy_value_error(self):
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

        responder: Final = ResponseService(db, speaker)

        responder.set_energy_value("john", "fish", "")
        self.assertEqual(
            "I couldn't catch that, what is the energy value of fish", data["message"]
        )

    def test_db_failure_set_energy_value(self):
        data: Final[dict] = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)
        fail_db: Final = MockFailDAO()

        responder: Final = ResponseService(fail_db, speaker)

        responder.set_energy_value("john", "fish", 10)
        self.assertEqual("Can't read from database", data["message"])

    def test_db_failure_total(self):
        data: Final[dict] = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)
        fail_db: Final = MockFailDAO()

        responder: Final = ResponseService(fail_db, speaker)

        responder.total("john")
        self.assertEqual("Can't read from database", data["message"])

    def test_db_failure_undo(self):
        data: Final[dict] = {"name": "not set", "message": "not set", "energy": -1}

        speaker: Final = MockSpeaker.get_configured_speaker(data)
        fail_db: Final = MockFailDAO()

        responder: Final = ResponseService(fail_db, speaker)

        responder.undo("john")
        self.assertEqual("Can't read from database", data["message"])
