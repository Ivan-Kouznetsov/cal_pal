import re
from abc import ABC, abstractmethod
from typing import Optional, Union

from .message_type import MessageType


class BaseSpeaker(ABC):
    @abstractmethod
    def __init__(self, message_patterns: dict):
        self._message_patterns = message_patterns

    def get_message(
        self,
        type: MessageType,
        user_name: Optional[str],
        food_name: Optional[str],
        energy: Union[int, float, None],
    ) -> str:

        response = self._message_patterns[type.value]

        if food_name is not None:
            response = re.sub("{food_name}", food_name, response)
        if energy is not None:
            response = re.sub("{energy}", str(round(energy)), response)
        if user_name is not None:
            response = re.sub("{user_name}", user_name, response)
        return response

    @abstractmethod
    def say(
        self,
        type: MessageType,
        user_name: Optional[str] = None,
        food_name: Optional[str] = None,
        energy: Union[int, float, None] = None,
    ) -> None:
        pass
