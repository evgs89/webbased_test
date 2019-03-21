import unittest
from modules.userManager import UserManager
from modules.TestDatabase import TestDatabase, ProgressDatabase
from tests.test_TestDatabase import create_test_questions
from modules.my_functions import id_generator


class tets_ProgressDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.um = UserManager()
        cls.pd = ProgressDatabase(cls.um)
        cls.td = TestDatabase()
        cls.td.load_to_db(create_test_questions(), 'test_db', 'test, please remove', replace = True)

    @classmethod
    def tearDownClass(cls):
        cls.td.delete_test(cls.td.get_id_by_testname('test_db'))

    def setUp(self):
        self.um.create_user('test_user')

    def tearDown(self):
        self.um.delete_user('test_user')

    def test_create_user(self):
        ID = id_generator()
        self.assertTrue(self.pd.create_user(ID))
        self.pd.delete_user(ID)

    def test_delete_user(self):
        ID = id_generator()
        self.pd.create_user(ID)
        self.assertTrue(self.pd.delete_user(ID))

    def test_add_test(self):
        ID = id_generator()
        self.assertTrue(self.pd.add_test(ID))
        self.pd.delete_test(ID)

    def test_delete_test(self):
        ID = id_generator()
        self.pd.add_test(ID)
        self.assertTrue(self.pd.delete_test(ID))

    def test_update_progress(self):
        user = self.td.get_id_by_testname('test_db')
        self.assertTrue(self.pd.update_progress())


























if __name__ == '__main__':
    unittest.main()
