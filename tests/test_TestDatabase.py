import unittest
from modules.TestDatabase import TestDatabase
from modules.importer import TestQuestion
from modules.my_functions import id_generator
import os

def create_test_questions():
    questions = []
    for i in range(5):
        test_tag = i
        test_text = f"This is test question number {i}"
        test_answers = [(True, 'Answer 1', None),
                        (False, 'Answer 2', None),
                        (False, 'Answer 3', None),
                        (True, 'Answer 4', None)]
        q = TestQuestion()
        q.number = test_tag
        q.question = test_text
        q.answers = test_answers
        questions.append(q)
    return questions


class test_TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = create_test_questions()
        cls.td = TestDatabase()
        cls.td.save_to_db_file('testdb.db', cls.questions, replace = True
        cls.id = ''

    @classmethod
    def tearDownClass(cls):
        try: os.remove('testdb.db')
        except FileNotFoundError: pass
        cls.td.delete_test(cls.id)

    @classmethod
    def check_test_is_existing(cls):
        if not cls.id: cls.id = cls.td.get_id_by_testname('test_db')

    def test_save_to_db_file(self):
        self.assertIsNone(self.td.save_to_db_file('testdb.db', self.questions, replace = True))

    def test_load_to_db(self):
        self.id = self.td.load_to_db(create_test_questions(), 'test_db', 'automatically created db, remove it')
        self.assertIsNotNone(self.id)

