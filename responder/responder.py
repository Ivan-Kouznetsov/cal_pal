from typing import Final, Optional, Union

from dao.base_dao import BaseDAO
from math_interpreter.calc import calc
from speaker.base_speaker import BaseSpeaker
from speaker.message_type import MessageType

from .base_responder import BaseResponseService


class ResponseService(BaseResponseService):
    def __init__(self, db: BaseDAO, speaker: BaseSpeaker):
        self._db = db
        self._speaker = speaker

    def _db_error(self):
        self._speaker.say(MessageType.DbError)
        print("Error: Database I/O error")

    def _try_calc(self, s: str) -> Optional[float]:
        try:
            return calc(s)
        except:
            return None

    #
    # Not user-specific responses
    #

    def bad_input(self) -> None:
        print("Warning: Invalid user input")
        self._speaker.say(MessageType.BadInput)

    def math(self, math: Optional[str]) -> None:
        if math is not None:
            calc_result = self._try_calc(math)
            if calc_result is not None:
                self._speaker.say(MessageType.Math, energy=calc_result)
            else:
                self.bad_input()

    def never_mind(self) -> None:
        self._speaker.say(MessageType.Ok)

    def set_up(self, retry=False) -> None:
        if retry:
            self._speaker.say(MessageType.SetUpRetry)
        else:
            self._speaker.say(MessageType.SetUp)

    #
    # User-specific responses
    #

    def greet(self, user_name: str):
        self._speaker.say(MessageType.Greet, user_name=user_name)

    def total(self, user_name: str) -> None:
        total: Final = self._db.try_get_daily_total(user_name)
        if total is not None:
            self._speaker.say(type=MessageType.Total, energy=total)
        else:
            self._db_error()

    def undo(self, user_name: str) -> None:
        if self._db.try_remove_last(user_name):
            self._speaker.say(MessageType.UndoSuccess)
        else:
            self._db_error()

    # Returns the last value of the food if any
    def eat(
        self,
        user_name: str,
        food_name: str,
        previous_energy_value: Optional[int] = None,
        ignore_previous_energy_value: bool = False,
    ) -> Optional[int]:
        if previous_energy_value is None:
            previous_energy_value = (
                self._db.try_get_food_energy(user_name, food_name)
                if not ignore_previous_energy_value
                else None
            )

            if previous_energy_value is not None:
                self._speaker.say(type=MessageType.SameConfirm, food_name=food_name)
                return previous_energy_value
            else:
                self._speaker.say(type=MessageType.EnergyQuery, food_name=food_name)
                return None
        else:
            self.set_energy_value(user_name, food_name, previous_energy_value)
            return previous_energy_value

    def set_energy_value(
        self, user_name: str, food_name: str, expression: Union[str, int]
    ) -> None:

        energy_value: Final = (
            expression if isinstance(expression, int) else self._try_calc(expression)
        )

        if energy_value is not None:
            self._speaker.say(
                type=MessageType.AddingNotification,
                food_name=food_name,
                energy=energy_value,
            )
            if not self._db.try_save_entry(user_name, food_name, int(energy_value)):
                self._db_error()
        else:
            self._speaker.say(
                type=MessageType.EnergyQueryRetry,
                food_name=food_name,
            )
