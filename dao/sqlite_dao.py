import sqlite3
import time
from datetime import date, datetime
from typing import Final, Optional

from .base_dao import BaseDAO


class SqliteDAO(BaseDAO):
    def __init__(self, db_name: str):
        self._db_name = db_name

    def _try_connect(self) -> Optional[sqlite3.Connection]:
        try:
            return sqlite3.connect(self._db_name)
        except:
            return None

    def try_init_db_if_needed(self) -> bool:
        success = False
        con: Final = self._try_connect()

        if con is not None:
            try:
                cur = con.cursor()

                cur.execute(
                    "create table if not exists Food (timestamp INT, user_name TEXT, name TEXT, energy INT);"
                )

                success = True
            except:  # pragma: no cover
                pass
            finally:
                con.close()

        return success

    def try_save_entry(self, user_name: str, name: str, energy: int) -> bool:
        success = False
        con: Final = self._try_connect()

        if con is not None:
            try:
                cur = con.cursor()

                cur.execute(
                    "insert into Food values (:timestamp, :user_name, :name, :energy);",
                    {
                        "timestamp": int(time.time()),
                        "user_name": user_name,
                        "name": name,
                        "energy": energy,
                    },
                )

                con.commit()
                success = True
            except:  # pragma: no cover
                pass
            finally:
                con.close()

        return success

    def try_get_daily_total(self, user_name: str) -> Optional[int]:
        today: Final = date.today()
        midnight_timespamp: Final = datetime(
            today.year, today.month, today.day
        ).timestamp()

        result = None

        con: Final = self._try_connect()
        if con is not None:
            try:
                cur = con.cursor()

                cur.execute(
                    "select sum(energy) from Food where timestamp >= :timestamp and user_name = :user_name;",
                    {"timestamp": midnight_timespamp, "user_name": user_name},
                )

                fetch_result = cur.fetchone()
                result = 0 if fetch_result[0] is None else fetch_result[0]

            except:  # pragma: no cover
                pass
            finally:
                con.close()

        return result

    def try_remove_last(self, user_name: str) -> bool:
        success = False
        con: Final = self._try_connect()

        if con is not None:
            try:
                cur = con.cursor()

                cur.execute(
                    "delete from Food where rowid = (select max(rowid) from Food) and user_name = :user_name;",
                    {"user_name": user_name},
                )
                con.commit()
                success = True
            except:  # pragma: no cover
                pass
            finally:
                con.close()

        return success

    def try_get_food_energy(self, user_name: str, name: str) -> Optional[int]:
        result = None
        con: Final = self._try_connect()

        if con is not None:
            try:
                cur = con.cursor()

                cur.execute(
                    "select energy from Food where name = :name and user_name = :user_name order by rowid desc limit 1;",
                    {"name": name, "user_name": user_name},
                )

                fetch_result = cur.fetchone()
                if fetch_result is not None:
                    result = fetch_result[0]
            except:  # pragma: no cover
                pass
            finally:
                con.close()

        return result

    def try_get_last_user_name(self) -> Optional[str]:
        result = None
        con: Final = self._try_connect()

        if con is not None:
            try:
                cur = con.cursor()

                cur.execute("select user_name from Food order by rowid desc limit 1")

                fetch_result = cur.fetchone()
                if fetch_result is not None:
                    result = fetch_result[0]
            except:  # pragma: no cover
                pass
            finally:
                con.close()

        return result
