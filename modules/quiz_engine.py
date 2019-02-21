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

    def _calc_new_weight(self, weight, answer):
        if answer: new_weight = weight - 0.5 * (weight - 1)
        else: new_weight = weight + (self._max_weight - weight) * 0.5
        return new_weight


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

    def select_test(self, user_id, quiz_id):
        quiz_info = self._test_db.get_test_info(quiz_id)
        max_weight = quiz_info['max_weight']
        init_weight = quiz_info['initial_weight']
        self._progress_filename = f'databases/{self._progress_db.select_test(user_id, quiz_id)}.db'
        if not os.path.isfile(self._progress_filename):
            conn, cur = self._connect_db()
            cur.execute("CREATE TABLE progress (quiestion_id TEXT, weight TEXT, pass_hash TEXT, last_login TEXT)")
            conn.commit()
        return self._progress_db.return_progress(user_id, quiz_id)

    def select_mode(self, quiz_id, quantity = 20, exam = False):




