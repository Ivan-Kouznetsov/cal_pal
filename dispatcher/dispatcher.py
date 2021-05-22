import re
from enum import Enum
from typing import Final, Optional, cast

from listener.preprocessor import Preprocessor
from responder.base_responder import BaseResponseService

from .dispatcher_state import DispatchExpectationType, DispatchState


class Keywords(Enum):
    NeverMind = "NeverMind"
    Total = "Total"
    Undo = "Undo"
    Eat = "Eat"
    Math = "Math"
    Yes = "Yes"
    Name = "Name"
    Greet = "Greet"


class DispatchService:
    def __init__(
        self,
        preprocessor: Preprocessor,
        responder: BaseResponseService,
        keywords: dict,
        user_name: Optional[str] = None,
    ):
        self._preprocessor = preprocessor
        self._responder = responder
        self._keywords = keywords
        self._state: Final = DispatchState()
        self._state.expectation = DispatchExpectationType.Standby
        self._state.user_name = user_name

    def _has_keyword(self, keyword: Enum, s: str) -> bool:
        for word in self._keywords[keyword.value]:
            if re.search(f"\\b{word}\\b", s) is not None:
                return True

        return False

    def _get_keyword_param(self, keyword: Enum, user_input: str) -> Optional[str]:
        match = None
        for word in self._keywords[keyword.value]:
            match = re.search(f"(?<={word}\\s).*", user_input)
            if match is not None:
                return match[0]

        return None

    def dispatch(self, user_input: str) -> None:
        if len(user_input) == 0:
            return

        # try to filter put nonsense

        if self._state.user_name is None:
            if self._has_keyword(Keywords.Name, user_input):
                user_name = self._get_keyword_param(Keywords.Name, user_input)
                if user_name is not None:
                    self._state.user_name = user_name
                    self._responder.greet(user_name)
                else:
                    self._responder.bad_input()
            else:
                self._responder.set_up(self._state.user_name_try_count > 0)
                self._state.user_name_try_count += 1
        elif self._has_keyword(Keywords.Greet, user_input):
            self._responder.greet(self._state.user_name or "")
        elif self._has_keyword(Keywords.Total, user_input):
            self._responder.total(self._state.user_name)
        elif self._has_keyword(Keywords.Math, user_input):
            param = self._get_keyword_param(Keywords.Math, user_input)
            if param is not None:
                self._responder.math(self._preprocessor.text_to_math(param))
            else:
                self._responder.bad_input()
        elif self._has_keyword(Keywords.NeverMind, user_input):
            self._responder.never_mind()
            self._state.reset()
        elif self._has_keyword(Keywords.Undo, user_input):
            self._responder.undo(self._state.user_name)
        elif (
            self._has_keyword(Keywords.Eat, user_input)
            and self._state.expectation == DispatchExpectationType.Standby
        ):
            food_name = self._get_keyword_param(Keywords.Eat, user_input)
            if food_name is not None:
                self._state.food_name = food_name
                self._state.previous_value = self._responder.eat(
                    self._state.user_name, food_name
                )
                if self._state.previous_value is None:
                    self._state.expectation = DispatchExpectationType.EnergyValue
                else:
                    self._state.expectation = (
                        DispatchExpectationType.SameAsLastTimeConfirmation
                    )
            else:
                self._state.reset()
                self._responder.bad_input()
        elif self._state.expectation == DispatchExpectationType.EnergyValue:
            self._responder.set_energy_value(
                self._state.user_name,
                cast(str, self._state.food_name),
                self._preprocessor.text_to_math(user_input),
            )
            self._state.expectation = DispatchExpectationType.Standby
        elif (
            self._state.expectation
            == DispatchExpectationType.SameAsLastTimeConfirmation
        ):
            assert self._state.food_name is not None

            if self._has_keyword(Keywords.Yes, user_input):
                self._responder.eat(
                    self._state.user_name,
                    self._state.food_name,
                    self._state.previous_value,
                )
                self._state.reset()
            else:
                self._responder.eat(
                    self._state.user_name, self._state.food_name, None, True
                )
                self._state.expectation = DispatchExpectationType.EnergyValue
