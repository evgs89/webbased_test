import unittest
from os.path import isfile
from collections import namedtuple
from modules.quiz_engine import Engine
from modules.userManager import UserManager
from modules.TestDatabase import TestDatabase
from modules.my_functions import create_test_questions


class test_Engine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        um = UserManager()
        um.create_user('test_user')
        um.change_password('test_user', '', '12345678')
        td = TestDatabase()
        td.load_to_db(create_test_questions(), 'test_db', 'test base, please delete', replace = True)
        cls.quiz_id = td.get_test_id('test_db')
        cls.engine = Engine()

    @classmethod
    def tearDownClass(cls):
        um = UserManager()
        td = TestDatabase()
        um.delete_user('test_user')
        td.delete_test(td.get_test_id('test_db'))

    def setUp(self):
        self.engine.auth_user('test_user', '12345678')

    def test_auth_user(self):
        self.assertIsNone(self.engine.auth_user('test_user', '123'))
        self.assertIsNotNone(self.engine.auth_user('test_user', '12345678'))

    def test_select_test(self):
        self.assertIsNone(self.engine.select_test(None))
        self.assertIsNotNone(self.engine.select_test(self.quiz_id))
        self.assertTrue(isfile(self.engine.select_test(self.quiz_id)))

    def test_get_progress(self):
        self.engine.select_test(self.quiz_id)
        self.assertIsInstance(self.engine.get_progress(), tuple)
        self.assertIn(0, self.engine.get_progress())

    def test_get_available_tests(self):
        self.assertIn((self.quiz_id, 'test_db', 'test base, please delete'),
                      self.engine.get_available_tests())

    def test_select_mode(self):
        self.assertTrue(self.engine.select_mode(5, True))
        self.assertTrue(len(self.engine.deck) == 5)
        self.assertTrue(self.engine.exam)

    def test_get_random_question_from_deck(self):
        self.engine.select_test(self.quiz_id)
        self.engine.select_mode(5, True)
        self.assertIsNotNone(self.engine.get_random_question_from_deck())
        self.assertTrue(len(self.engine.get_random_question_from_deck() == 4))

    def test_user_answered_question(self):
        self.engine.select_test(self.quiz_id)
        self.engine.select_mode(5, False)
        question = self.engine.get_random_question_from_deck()
        right_answers = [i for i in range(4)
                         if question.answers[i][1] == 'Answer 1'
                         or question.answers[i][1] == 'Answer 4']
        self.assertIsInstance(self.engine.user_answered_question(question.tag))




if __name__ == '__main__':
    unittest.main()
