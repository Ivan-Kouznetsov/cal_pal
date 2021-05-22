from abc import ABC, abstractmethod
from typing import Optional


class BaseResponseService(ABC):

    #
    # Not user-specific
    #

    @abstractmethod
    def bad_input(self) -> None:
        pass

    @abstractmethod
    def math(self, math: Optional[str]) -> None:
        pass

    @abstractmethod
    def never_mind(self) -> None:
        pass

    @abstractmethod
    def set_up(self, retry: bool) -> None:
        pass

    #
    # User-specific
    #

    @abstractmethod
    def greet(self, user_name: str) -> None:
        pass

    @abstractmethod
    def total(self, user_name: str) -> None:
        pass

    @abstractmethod
    def undo(self, user_name: str) -> None:
        pass

    @abstractmethod
    def eat(
        self,
        user_name: str,
        food_name: str,
        previous_energy_value: Optional[int] = None,
        ignore_previous_energy_value: bool = False,
    ) -> Optional[int]:
        pass

    @abstractmethod
    def set_energy_value(self, user_name: str, food_name: str, expression: str) -> None:
        pass
