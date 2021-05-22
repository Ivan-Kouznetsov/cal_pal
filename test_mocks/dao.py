from typing import Optional

from dao.base_dao import BaseDAO


class MockDAO(BaseDAO):
    data: dict
    responses: dict

    def __init__(self, data: dict, responses: dict):
        self.data = data
        self.responses = responses

    def try_init_db_if_needed(self) -> bool:
        return self.responses["db_init"]

    def try_save_entry(self, user_name: str, name: str, energy: int) -> bool:
        self.data["name"] = name
        self.data["energy"] = energy
        return True

    def try_get_daily_total(self, user_name: str) -> Optional[int]:
        return self.responses["daily_total"]

    def try_remove_last(self, user_name: str) -> bool:
        return self.responses["remove_success"]

    def try_get_food_energy(self, user_name: str, name: str) -> Optional[int]:
        return self.responses[name]

    def try_get_last_user_name(self) -> Optional[str]:
        return "john"
