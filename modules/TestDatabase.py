from modules.importer import TestQuestion
from modules.my_functions import id_generator
from modules.userManagement import UserManagement
import os
import sqlite3


class TestDatabase:
    def __init__(self):
        self._db_file = 'databases/quizzes.db'
        if not os.path.isfile(self._db_file):
            conn = sqlite3.connect(self._db_file)
            cur = conn.cursor()
            cur.execute("CREATE TABLE quizzes (quiz_id TEXT, quiz_filename TEXT, name TEXT, description TEXT, max_weight REAL, initial_weight REAL)")
            conn.commit()

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

    @staticmethod
    def load_from_db_file(filename):
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        cursor.execute("SELECT tag, question, question_pic FROM questions")
        raw_questions = cursor.fetchall()
        questions = []
        for row in raw_questions:
            question = TestQuestion()
            question.number = row[0]
            question.question = row[1]
            question.question_picture = row[2]
            cursor.execute("SELECT correct, answer, answer_pic FROM answers WHERE tag = ?", question.number)
            answers = cursor.fetchall()
            for answer in answers: question.add_answer(answer[1], answer[0], answer[2])
            questions.append(question)
        return questions

    def load_to_db(self, questions, name = None, description = None):
        _id = id_generator(10)
        filename = 'databases/{0}.db'.format(_id)
        self.save_to_db_file(filename, questions, True)
        test_name = name if name else _id
        test_description = description if description else ''
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        max_weight = len(questions)
        init_weight = (max_weight + 1)/2
        cur.execute("INSERT INTO quizzes VALUES (?, ?, ?, ?, ?, ?)", (_id, _id+'.db', test_name, test_description, max_weight, init_weight))
        conn.commit()

    def get_available_tests(self):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        cur.execute("SELECT quiz_id, name, description FROM quizzes")
        return cur.fetchall()

    def get_test_info(self, quiz_id):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        cur.execute("SELECT max_weight, initial_weight FROM quizzes WHERE quiz_id = ?", quiz_id)
        return cur.fetchone()


class ProgressDatabase:
    def __init__(self):
        self._db_file = 'databases/progress.db'
        if not os.path.isfile(self._db_file):
            conn, cur = self._connect_db()
            cur.execute("CREATE TABLE progress (id TEXT, user_id TEXT, quiz_id TEXT, learned_percent REAL, seen_percent REAL, last_use TEXT)")
            conn.commit()

    def _connect_db(self):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        return [conn, cur]

    def add_user(self, user_id):
        conn, cur = self._connect_db()
        tdb = TestDatabase()
        _id = id_generator(10)
        available_tests = tdb.get_available_tests()
        for test in available_tests:
            cur.execute("INSERT INTO progress VALUES (?, ?, ?, ?, ?, ?", (_id, user_id, test['quiz_id'], 0, 0, ''))
        conn.commit()

    def delete_user(self, user_id):
        conn, cur = self._connect_db()
        cur.execute("DELETE FROM progress WHERE user_id = ?", user_id)
        conn.commit()

    def add_test(self, quiz_id):
        conn, cur = self._connect_db()
        um = UserManagement()
        _id = id_generator(10)
        users = [i['user_id'] for i in um.get_list_of_users()]
        for user in users:
            cur.execute("INSERT INTO progress VALUES (?, ?, ?, ?, ?, ?", (_id, user, quiz_id, 0, 0, ''))
        conn.commit()

    def delete_test(self, quiz_id):
        conn, cur = self._connect_db()
        cur.execute("DELETE FROM progress WHERE quiz_id = ?", quiz_id)

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


