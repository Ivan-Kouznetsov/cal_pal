from abc import ABC, abstractmethod
from typing import Optional


class BaseDAO(ABC):
    @abstractmethod
    def try_init_db_if_needed(self) -> bool:
        pass

    @abstractmethod
    def try_save_entry(self, user_name: str, name: str, energy: int) -> bool:
        pass

    @abstractmethod
    def try_get_daily_total(self, user_name: str) -> Optional[int]:
        pass

    @abstractmethod
    def try_remove_last(self, user_name: str) -> bool:
        pass

    @abstractmethod
    def try_get_food_energy(self, user_name: str, name: str) -> Optional[int]:
        pass

    @abstractmethod
    def try_get_last_user_name(self) -> Optional[str]:
        pass
