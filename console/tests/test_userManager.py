import unittest
from typing import List, Any
import sqlite3

from modules.userManager import UserManager, DuplicateUsernameException
from modules.my_functions import id_generator


class test_UserManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.um = UserManager()
        cls.username = id_generator()
        cls.password = id_generator()

    def setUp(self):
        self.um.create_user(self.username)
        self.um.change_password(self.username, '', self.password)

    def tearDown(self):
        self.um.delete_user(self.username)

    def test_create_user(self):
        if self.um.get_user_id(self.username): self.um.delete_user(self.username)
        self.assertIsNotNone(self.um.create_user(self.username))
        with self.assertRaises(DuplicateUsernameException):
            self.um.create_user(self.username)

    def test_get_user_id(self):
        self.assertIsNotNone(self.um.get_user_id(self.username))

    def test_change_password(self):
        self.um.create_user('test_user')
        self.assertTrue(self.um.change_password('test_user', '', self.password))
        self.assertIsNone(self.um.change_password('test_user', '', self.password))
        self.um.delete_user('test_user')

    def test_valid_user(self):
        self.assertTrue(self.um.valid_user(self.username, self.password))
        self.assertIsNone(self.um.valid_user(self.username, '123'))

    def test_delete_user(self):
        self.assertTrue(self.um.delete_user(self.username))

    def test_get_list_of_users(self):
        users = [id_generator() for i in range(10)]
        for name in users:
            try: self.um.create_user(name)
            except DuplicateUsernameException: users.remove(name)
        rows_users: List[sqlite3.Row] = self.um.get_list_of_users()
        received_users = [row[1] for row in rows_users]
        self.assertTrue(set(users) - set(received_users) == set())
        for name in users: self.um.delete_user(name)


if __name__ == '__main__':
    unittest.main()
