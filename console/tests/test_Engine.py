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
        cls.quiz_id = td.get_test_id('test_db')[0]
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
        self.assertTrue(self.engine.select_test(self.quiz_id))

    def test_get_progress(self):
        self.engine.select_test(self.quiz_id)
        self.assertIsInstance(self.engine.get_progress(), tuple)
        self.assertIn(0, self.engine.get_progress())

    def test_get_available_tests(self):
        self.assertIn((self.quiz_id, 'test_db', 'test base, please delete'),
                      self.engine.get_available_tests())

    def test_select_mode(self):
        self.engine.select_test(self.quiz_id)
        self.assertTrue(self.engine.select_mode(5, True))
        self.assertTrue(len(self.engine.deck) == 5)
        self.assertTrue(self.engine.exam)

    def test_get_random_question_from_deck(self):
        self.engine.select_test(self.quiz_id)
        self.engine.select_mode(5, True)
        self.assertIsNotNone(self.engine.get_random_question_from_deck())
        self.assertTrue(len(self.engine.get_random_question_from_deck()) == 4)

    def quiz_runner(self, right = True):
        self.engine.select_test(self.quiz_id)
        self.engine.select_mode(5, True)
        returns = []
        for i in range(5):
            question = self.engine.get_random_question_from_deck()
            right_answers = [i for i in range(4)
                             if question.answers[i] == 'Answer 1'
                             or question.answers[i] == 'Answer 4']
            non_right_answers = [i for i in range(4) if i not in right_answers]
            answers = right_answers if right else non_right_answers
            ret = self.engine.user_answered_question(question.tag, answers)
            self.assertIsInstance(ret, tuple)
            self.assertTrue(ret[0])
            self.assertEqual(ret[1], right)
            returns.append(ret)
        return returns

    def test_user_answered_question(self):
        self.engine.select_test(self.quiz_id)
        self.engine.select_mode(5, False)
        question = self.engine.get_random_question_from_deck()
        right_answers = [i for i in range(4)
                         if question.answers[i] == 'Answer 1'
                         or question.answers[i] == 'Answer 4']
        non_right_answers = [i for i in range(4) if i not in right_answers]
        ret1 = self.engine.user_answered_question(question.tag, non_right_answers)
        self.assertIsInstance(ret1, tuple)
        self.assertFalse(ret1[0])
        self.assertFalse(ret1[1])
        ret2 = self.engine.user_answered_question(question.tag, right_answers)
        self.assertIsInstance(ret2, tuple)
        self.assertFalse(ret2[0])
        self.assertTrue(ret2[1])
        ## try correct exam
        test_results = self.quiz_runner(True)
        self.assertTrue(len(test_results) == 5)
        self.assertTrue(len(self.engine.correct_answers_to_quiz) == 0)
        ## try incorrect exam
        test_results = self.quiz_runner(False)
        self.assertTrue(len(test_results) == 5)
        self.assertTrue(len(self.engine.correct_answers_to_quiz) == 5)

    def test_test_finished(self):
        test_results = self.quiz_runner(False)
        self.assertTrue(len(test_results) == 5)
        self.assertTrue(len(self.engine.correct_answers_to_quiz) == 5)
        result = self.engine.test_finished()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) == 5)



if __name__ == '__main__':
    unittest.main()
