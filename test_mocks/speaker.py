from typing import Optional, Union

from helpers import config as config_helper
from speaker.base_speaker import BaseSpeaker
from speaker.message_type import MessageType


class MockSpeaker(BaseSpeaker):
    data: dict
    _message_patterns: dict

    def __init__(self, data: dict, message_patterns: dict):
        self.data = data
        super().__init__(message_patterns)

    def say(
        self,
        type: MessageType,
        user_name: Optional[str] = None,
        food_name: Optional[str] = None,
        energy: Union[int, float, None] = None,
    ) -> None:
        self.data["message"] = self.get_message(
            type, user_name or "test", food_name or "test", energy or 0
        )

    @staticmethod
    def get_configured_speaker(data: dict):
        settings = config_helper.load_config("./test_mocks/config.toml")
        assert settings is not None
        return MockSpeaker(data, settings["speaking"]["message_patterns"])
