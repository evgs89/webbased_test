import os
import sqlite3
from modules.userManagement import UserManagement
from modules.TestDatabase import TestDatabase
from modules.TestDatabase import ProgressDatabase


class Engine:
    def __init__(self):
        self._userManagement = UserManagement()
        self._test_db = TestDatabase()
        self._progress_db = ProgressDatabase()
        self._progress_filename = ''
        self._username = ''
        self._password = ''
        self._max_weight = 0
        self._init_weight = 0

    def _calc_new_weight(self, weight, answer):
        if answer: new_weight = weight - 0.5 * (weight - 1)
        else: new_weight = weight + (self._max_weight - weight) * 0.5
        return new_weight

    def _get_correct_weights(self, quiz_id):
        quiz_info = self._test_db.get_test_info(quiz_id)
        self._max_weight = quiz_info['max_weight']
        self._init_weight = quiz_info['initial_weight']


    def _connect_db(self):
        conn = sqlite3.connect(self._progress_filename)
        cur = conn.cursor()
        return (conn, cur)

    def auth_user(self, username, password):
        user_id = self._userManagement.valid_user(username, password)
        if user_id:
            self._username, self._password = username, password
            available_tests = self._test_db.get_available_tests()
            return available_tests ## list of sqlite3.rows "SELECT quiz_id, name, description FROM quizzes"

    def _populate_individual_progress_db(self, quiz_id):
        question_tags = self._test_db.load_quesqion_tags(quiz_id)
        conn, cur = self._connect_db()
        cur.execute("CREATE TABLE progress (question_id TEXT,weight TEXT, seen_times INTEGER, last_login TEXT, learned INTEGER)")
        conn.commit()
        for tag in question_tags:
            cur.execute("INSERT INTO PROGRESS VALUES (?, ?, ?, ?, ?)", (tag, self._init_weight, 0, '', 0))
        conn.commit()

    def _get_weights(self):
        conn, cu


    def select_test(self, user_id, quiz_id):
        self._get_correct_weights(quiz_id)
        self._progress_filename = f'databases/{self._progress_db.select_test(user_id, quiz_id)}.db'
        if not os.path.isfile(self._progress_filename): self._populate_individual_progress_db(quiz_id)


        return self._progress_db.return_progress(user_id, quiz_id)

    def select_mode(self, quiz_id, quantity = 20, exam = False):




