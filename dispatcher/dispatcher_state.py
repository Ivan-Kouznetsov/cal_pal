from enum import Enum, auto
from typing import Optional


class DispatchExpectationType(Enum):
    Standby = auto()
    SameAsLastTimeConfirmation = auto()
    EnergyValue = auto()


class DispatchState:
    def __init__(self):
        self.user_name: Optional[str] = None
        self.food_name: Optional[str] = None
        self.previous_value: Optional[int] = None
        self.expectation: DispatchExpectationType = DispatchExpectationType.Standby
        self.user_name_try_count: int = 0

    def reset(self):
        self.expectation = DispatchExpectationType.Standby
        self.food_name = None
        self.previous_value = None
