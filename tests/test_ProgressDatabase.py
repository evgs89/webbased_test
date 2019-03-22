import unittest
from modules.userManager import UserManager
from modules.TestDatabase import TestDatabase, ProgressDatabase
from modules.my_functions import id_generator, create_test_questions


class tets_ProgressDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.um = UserManager()
        cls.pd = ProgressDatabase(cls.um)
        cls.td = TestDatabase()
        cls.td.load_to_db(create_test_questions(), 'test_db', 'test, please remove', replace = True)

    @classmethod
    def tearDownClass(cls):
        cls.td.delete_test(cls.td.get_test_id('test_db'))

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

    def test_select_test(self):
        self.assertIsNotNone(self.pd.select_test(self.um.get_user_id('test_user'), self.td.get_test_id('test_db')[0]))

    def test_update_progress(self):
        ID = self.pd.select_test(self.um.get_user_id('test_user'), self.td.get_test_id('test_db')[0])
        self.assertTrue(self.pd.update_progress(ID, 50, 70))
        progress = self.pd.return_progress(self.um.get_user_id('test_user'), self.td.get_test_id('test_db')[0])
        self.assertIn(50, progress)
        self.assertIn(70, progress)

    def test_return_progress(self):
        progress = self.pd.return_progress(self.um.get_user_id('test_user'), self.td.get_test_id('test_db')[0])
        self.assertIsInstance(progress, tuple)






























if __name__ == '__main__':
    unittest.main()
