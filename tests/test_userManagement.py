import unittest
from modules.userManagement import UserManagement, DuplicateUsernameException
from modules.my_functions import id_generator, hash_password

class test_UserManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.um = UserManagement()
        cls.username = id_generator()
        cls.password = id_generator()

    @classmethod
    def tearDownClass(cls):
        cls.um.delete_user(cls.username)

    def test_create_user(self):
        if self.um._is_user(self.username): self.um.delete_user(self.username)
        self.assertIsNotNone(self.um.create_user(self.username))
        self.assertRaises(DuplicateUsernameException)

    def test_change_password(self):
        try: self.um.create_user(self.username)
        except DuplicateUsernameException: pass
        self.assertTrue(self.um.change_password(self.username, self.password, '') or self.um.change_password(self.username, '', self.password))
        self.um.change_password(self.username, '', self.password)

    def test_valid_user(self):
        try: self.um.create_user(self.username)
        except DuplicateUsernameException: pass
        self.assertTrue(self.um.valid_user(self.username, '') or self.um.valid_user(self.username, self.password))
        if self.um.valid_user(self.username, ''): self.um.change_password(self.username, '', self.password)
        self.assertTrue(self.um.valid_user(self.username, self.password))

    def test_delete_user(self):
        self.assertTrue(self.um.delete_user(self.username))

    def test_get_list_of_users(self):
        users = [id_generator() for i in range(10)]
        for name in users:
            try: self.um.create_user(name)
            except DuplicateUsernameException: users.remove(name)
        rows_users = self.um.get_list_of_users()
        recieved_users = [row[1] for row in rows_users]
        self.assertTrue(set(recieved_users) - set(users) == set())
        for name in users: self.um.delete_user(name)


