from os import remove
from typing import Final
from unittest import TestCase

from dao.sqlite_dao import SqliteDAO


class SqliteDAOTests(TestCase):
    test_db_name: Final = "test_dao.db"
    user_name: Final = "test_user"

    def setUp(self):
        self.db = SqliteDAO(self.test_db_name)
        assert self.db.try_init_db_if_needed()

    def tearDown(self):
        remove(self.test_db_name)

    # happy path

    def test_init(self):
        db = SqliteDAO(":memory:")
        self.assertTrue(db.try_init_db_if_needed())

    def test_save(self):
        self.assertTrue(self.db.try_save_entry(self.user_name, "fish", 10))
        self.assertEqual(10, self.db.try_get_daily_total(self.user_name))

    def test_undo(self):
        self.assertTrue(self.db.try_save_entry(self.user_name, "fish", 10))
        self.assertTrue(self.db.try_remove_last(self.user_name))
        self.assertEqual(0, self.db.try_get_daily_total(self.user_name))

    def test_get_food_energy(self):
        self.assertTrue(self.db.try_save_entry(self.user_name, "fish", 10))
        self.assertEqual(10, self.db.try_get_food_energy(self.user_name, "fish"))
        self.assertEqual(None, self.db.try_get_food_energy(self.user_name, "nothing"))

    def test_get_last_user_name(self):
        self.assertIsNone(self.db.try_get_last_user_name())
        self.assertTrue(self.db.try_save_entry(self.user_name, "fish", 10))
        self.assertEqual(self.db.try_get_last_user_name(), self.user_name)

    # errors
    def test_connect_error(self):
        db = SqliteDAO("\0")
        self.assertFalse(db.try_init_db_if_needed())

    def test_save_error(self):
        db = SqliteDAO(":memory:")
        # fails because the Food table does not exist
        self.assertFalse(db.try_save_entry(self.user_name, "", 7))
