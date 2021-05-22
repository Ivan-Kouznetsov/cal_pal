from typing import Final, Optional, Union

import pyttsx3  # type: ignore

from .base_speaker import BaseSpeaker
from .message_type import MessageType


class SpeakerTtsx3(BaseSpeaker):
    def __init__(self, message_patterns: dict):
        self._engine = pyttsx3.init()
        super().__init__(message_patterns)

    def say(
        self,
        type: MessageType,
        user_name: Optional[str] = None,
        food_name: Optional[str] = None,
        energy: Union[int, float, None] = None,
    ) -> None:

        self._engine.say(self.get_message(type, user_name, food_name, energy))
        self._engine.runAndWait()
