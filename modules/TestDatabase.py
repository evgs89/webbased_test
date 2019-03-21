from modules.importer import TestQuestion
from modules.my_functions import id_generator
import os
import sqlite3


class DuplicateTestNameException(Exception):
    pass


class TestDatabase:
    def __init__(self):
        self._db_file = 'databases/quizzes.db'
        if not os.path.isfile(self._db_file):
            conn = sqlite3.connect(self._db_file)
            cur = conn.cursor()
            cur.execute("CREATE TABLE quizzes (quiz_id TEXT, quiz_filename TEXT, name TEXT, description TEXT, max_weight REAL, initial_weight REAL)")
            conn.commit()

    def _get_filename(self, quiz_id):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        cur.execute("SELECT quiz_filename FROM quizzes WHERE quiz_id = ?", (quiz_id, ))
        filename = cur.fetchone()
        if filename: filename = f'databases/{filename[0]}'
        return filename

    def _quiz_exists(self, quiz_name):
        "return quiz_id for given quiz_name or None if no such test"
        quizes = self.get_available_tests()
        if quizes:
            quiz_list = {i[1]: i[0] for i in quizes}
            return quiz_list.get(quiz_name)



    @staticmethod
    def save_to_db_file(filename, questions, replace = False):
        if not os.path.isfile(filename) or replace:
            try: os.remove(filename)
            except FileNotFoundError: pass
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE questions (tag TEXT, question TEXT, question_pic BLOB)")
            conn.commit()
            cursor.execute("CREATE TABLE answers (tag TEXT, correct BOOL, answer TEXT, answer_pic BLOB)")
            conn.commit()
            for question in questions:
                cursor.execute("INSERT INTO questions values (?, ?, ?)", (question.number,
                                                                          question.question,
                                                                          sqlite3.Binary(question.question_picture) if question.question_picture else None))
                for answer in question.answers:
                    cursor.execute("INSERT INTO answers values (?, ?, ?, ?)", (question.number,
                                                                               answer[0],
                                                                               answer[1],
                                                                               sqlite3.Binary(answer[2]) if answer[2] else None))
            conn.commit()
            return True
        else: raise DuplicateTestNameException

    def load_to_db(self, questions, name = None, description = None, replace = False):
        _id = id_generator(10)
        if name:
            existing_id = self._quiz_exists(name)
            test_name = name
            if existing_id: _id = existing_id
        else:
            test_name = _id
        filename = f'databases/{_id}.db'
        if self.save_to_db_file(filename, questions, replace):
            test_description = description if description else ''
            conn = sqlite3.connect(self._db_file)
            cur = conn.cursor()
            max_weight = len(questions)
            init_weight = (max_weight + 1)/2
            cur.execute("INSERT INTO quizzes VALUES (?, ?, ?, ?, ?, ?)", (_id, _id+'.db', test_name, test_description, max_weight, init_weight))
            conn.commit()
            return _id

    def get_id_by_testname(self, name):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        cur.execute("SELECT quiz_id FROM quizzes WHERE name = ?", (name,))
        ID = cur.fetchall()
        if ID: return [i[0] for i in ID]

    def load_quesqion_tags(self, quiz_id):
        filename = self._get_filename(quiz_id)
        if filename:
            conn = sqlite3.connect(filename)
            cur = conn.cursor()
            cur.execute("SELECT tag FROM questions")
            return [i[0] for i in cur.fetchall()]

    def get_questions(self, quiz_id, question_tags):
        conn = sqlite3.connect(self._get_filename(quiz_id))
        cur = conn.cursor()
        questions = {}
        if type(question_tags) == int: question_tags = [str(question_tags), ]
        if type(question_tags) == str: question_tags = [question_tags, ]
        for tag in question_tags:
            cur.execute("SELECT question, question_pic FROM questions WHERE tag = ?", (tag, ))
            row = cur.fetchone()
            question = TestQuestion()
            question.number = tag
            question.question = row[0]
            question.question_picture = row[1]
            cur.execute("SELECT correct, answer, answer_pic FROM answers WHERE tag = ?", (tag, ))
            answers = cur.fetchall()
            for answer in answers: question.add_answer(answer[1], answer[0], answer[2])
            questions[tag] = question
        return questions

    def load_from_db(self, quiz_id):
        tags = self.load_quesqion_tags(quiz_id)
        return self.get_questions(quiz_id, tags)

    def get_available_tests(self):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        cur.execute("SELECT quiz_id, name, description FROM quizzes")
        return cur.fetchall()

    def get_test_info(self, quiz_id):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        cur.execute("SELECT max_weight, initial_weight FROM quizzes WHERE quiz_id = ?", (quiz_id, ))
        return cur.fetchone()

    def delete_test(self, quiz_id):
        "remove one test (string ID) or many (list of IDs)"
        if type(quiz_id) == str: quiz_id = [quiz_id]
        if type(quiz_id) == list:
            for ID in quiz_id:
                filename = self._get_filename(ID)
                conn = sqlite3.connect(self._db_file)
                cur = conn.cursor()
                cur.execute("DELETE FROM quizzes WHERE quiz_id = ?", (ID, ))
                conn.commit()
                try: os.remove(filename)
                except FileNotFoundError: print(f'{filename} is not found')
        return True




class ProgressDatabase:
    def __init__(self, user_manager):
        self._db_file = 'databases/progress.db'
        self.um = user_manager
        if not os.path.isfile(self._db_file):
            conn, cur = self._connect_db()
            cur.execute("CREATE TABLE progress (id TEXT, user_id TEXT, quiz_id TEXT, learned_percent REAL, seen_percent REAL, last_use TEXT)")
            conn.commit()

    def _connect_db(self):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        return [conn, cur]

    def create_user(self, user_id):
        conn, cur = self._connect_db()
        tdb = TestDatabase()
        _id = id_generator(10)
        available_tests = tdb.get_available_tests()
        for test in available_tests:
            cur.execute("INSERT INTO progress VALUES (?, ?, ?, ?, ?, ?)", (_id, user_id, test[0], 0, 0, ''))
        conn.commit()
        return cur.lastrowid is not None

    def delete_user(self, user_id):
        conn, cur = self._connect_db()
        cur.execute("DELETE FROM progress WHERE user_id = ?", (user_id, ))
        conn.commit()
        return cur.rowcount > 0

    def add_test(self, quiz_id):
        conn, cur = self._connect_db()
        _id = id_generator(10)
        users = [i['user_id'] for i in self.um.get_list_of_users()]
        for user in users:
            cur.execute("INSERT INTO progress VALUES (?, ?, ?, ?, ?, ?)", (_id, user, quiz_id, 0, 0, ''))
        conn.commit()
        return cur.lastrowid is not None

    def delete_test(self, quiz_id):
        conn, cur = self._connect_db()
        cur.execute("DELETE FROM progress WHERE quiz_id = ?", (quiz_id, ))
        return cur.rowcount > 0

    def update_progress(self, id, learned_percent, seen_percent):
        conn, cur = self._connect_db()
        cur.execute("UPDATE progress SET learned_percent = ?, seen_percent = ? WHERE id = ?", (learned_percent, seen_percent, id))
        conn.commit()
        return cur.rowcount > 0

    def select_test(self, user_id, quiz_id):
        conn, cur = self._connect_db()
        cur.execute("SELECT id FROM progress WHERE user_id = ? AND quiz_id = ?", (user_id, quiz_id))
        return cur.fetchone()['id']

    def return_progress(self, user_id, quiz_id):
        conn, cur = self._connect_db()
        cur.execute("SELECT learned_percent, seen_percent, last_use FROM progress WHERE user_id = ? AND quiz_id = ?", (user_id, quiz_id))
        return cur.fetchone()