import unittest
from modules.TestDatabase import TestDatabase, DuplicateTestNameException
from modules.importer import TestQuestion
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

    @classmethod
    def tearDownClass(cls):
        try: os.remove('test.db')
        except FileNotFoundError: pass
        cls.td.delete_test(cls.td.get_test_id('test_db'))

    def setUp(self):
        if self.td.get_test_id('test_db'): self.td.delete_test(self.td.get_test_id('test_db'))

    def test_save_to_db_file(self):
        self.assertTrue(self.td.save_to_db_file('test.db', self.questions, replace = True))
        with self.assertRaises(DuplicateTestNameException):
            self.td.save_to_db_file('test.db', self.questions, replace = False)
        os.remove('test.db')

    def test_load_to_db(self):
        id = self.td.load_to_db(create_test_questions(), 'test_db', 'automatically created db, remove it')
        self.assertIsInstance(id, str)

    def test_get_test_id(self):
        self.assertTrue(self.td.load_to_db(create_test_questions(),
                                           'test_db',
                                           'automatically created db, remove it') in self.td.get_test_id('test_db'))

    def test_load_question_tags(self):
        self.assertEqual(5, len(self.td.load_quesqion_tags(self.td.load_to_db(create_test_questions(),
                                                                              'test_db',
                                                                              'automatically created db, remove it'))))

    def test_get_questions(self):
        id = self.td.load_to_db(create_test_questions(), 'test_db', 'automatically created db, remove it')
        tags = self.td.load_quesqion_tags(id)
        questions = self.td.get_questions(id, tags)
        for tag in tags:
            self.assertIsInstance(questions[tag], TestQuestion)

    def test_load_from_db(self):
        questions = self.td.load_from_db(self.td.load_to_db(create_test_questions(),
                                                            'test_db',
                                                            'automatically created db, remove it'))
        for tag in questions.keys():
            self.assertIsInstance(questions[tag], TestQuestion)

    def test_get_available_test(self):
        self.td.load_to_db(create_test_questions(), 'test_db', 'automatically created db, remove it')
        testrows = self.td.get_available_tests()
        self.assertIsNotNone(testrows)
        self.assertNotEqual(testrows, [])
        self.assertTrue('test_db' in [i[1] for i in testrows])

    def test_get_test_info(self):
        info = self.td.get_test_info(self.td.load_to_db(create_test_questions(),
                                                        'test_db',
                                                        'automatically created db, remove it'))
        self.assertIsNotNone(info)
        self.assertIsInstance(info, tuple)

    def test_delete_test(self):
        self.assertTrue(self.td.delete_test(self.td.load_to_db(create_test_questions(),
                                                               'test_db',
                                                               'automatically created db, remove it')))


if __name__ == '__main__':
    unittest.main()
