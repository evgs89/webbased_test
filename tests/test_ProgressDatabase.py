import unittest
from modules.userManagement import UserManagement
from modules.TestDatabase import ProgressDatabase


class tets_ProgressDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.um = UserManagement()
        cls.pd = ProgressDatabase(cls.um)

    def setUp(self):
        self.um.create_user('test_user')

    def tearDown(self):
        self.um.delete_user('test_user')

    def test_something(self):
        self.assertEqual(True, False)




















if __name__ == '__main__':
    unittest.main()
