from typing import Optional

from dao.base_dao import BaseDAO


class MockFailDAO(BaseDAO):
    def try_init_db_if_needed(self) -> bool:
        return False

    def try_save_entry(self, user_name: str, name: str, energy: int) -> bool:
        return False

    def try_get_daily_total(self, user_name: str) -> Optional[int]:
        return None

    def try_remove_last(self, user_name: str) -> bool:
        return False

    def try_get_food_energy(self, user_name: str, name: str) -> Optional[int]:
        return None

    def try_get_last_user_name(self) -> Optional[str]:
        return None
