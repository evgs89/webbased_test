import os
import sqlite3
import random
import datetime
from modules.userManagement import UserManagement
from modules.TestDatabase import TestDatabase
from modules.TestDatabase import ProgressDatabase


class Engine:
    def __init__(self):
        self._userManagement = UserManagement()
        self._test_db = TestDatabase()
        self._progress_db = ProgressDatabase()
        self._progress_filename = ''
        self._quiz_id = ''
        self._username = ''
        self._password = ''
        self._user_id = ''
        self._max_weight = 0
        self._init_weight = 0
        self.deck = []
        self.deck_weights = {}

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
        self._user_id = self._userManagement.valid_user(username, password)
        if self._user_id:
            self._username, self._password = username, password
        return self._user_id

    def get_available_tests(self):
        if self._user_id:
            available_tests = self._test_db.get_available_tests()
            return available_tests  ## list of sqlite3.rows "SELECT quiz_id, name, description FROM quizzes"

    def _populate_individual_progress_db(self, quiz_id):
        question_tags = self._test_db.load_quesqion_tags(quiz_id)
        conn, cur = self._connect_db()
        cur.execute("CREATE TABLE progress (question_id TEXT, weight TEXT, seen_times INTEGER, last_seen TEXT, learned INTEGER)")
        conn.commit()
        for tag in question_tags:
            cur.execute("INSERT INTO PROGRESS VALUES (?, ?, ?, ?, ?)", (tag, self._init_weight, 0, '', 0))
        conn.commit()

    def _get_weights(self):
        conn, cur = self._connect_db()
        cur.execute("SELECT question_id, weight, last_seen FROM progress")
        weights = cur.fetchall()
        return weights

    def select_test(self, quiz_id):
        if self._user_id:
            self._get_correct_weights(quiz_id)
            self._quiz_id = quiz_id
            self._progress_filename = f'databases/{self._progress_db.select_test(self._user_id, quiz_id)}.db'
            if not os.path.isfile(self._progress_filename): self._populate_individual_progress_db(quiz_id)
            self._get_correct_weights(quiz_id)
            return self._progress_db.return_progress(self._user_id, quiz_id)

    def select_mode(self, quiz_id, quantity = 20, exam = False):
        assert(self._progress_filename != '')
        weight_list = self._get_weights()
        ids = [i['question_id'] for i in weight_list]
        weights = [i['weight'] for i in weight_list]
        deck_ids = random.choices(population = ids, weights = weights, k = quantity)
        deck = self._test_db.get_questions(deck_ids, quiz_id) #dict {id: question_object}
        deck_weights = {}
        for i in weights:
            if i['question_id'] in deck: deck_weights[i['question_id']] = i['weight']
        assert(len(deck) == len(deck_weights))
        self.deck = deck
        self.deck_weights = deck_weights
        return exam

    def user_answered_question(self, question_id, correct = False):
        new_weight = self._calc_new_weight(self.deck_weights[question_id], correct)
        self.deck_weights[question_id] = new_weight
        if correct: self.deck.pop(question_id)
        return True

    def test_finished(self):
        conn, cur = self._connect_db()
        today = datetime.date.today().strftime('%d.%m.%Y')
        for question_id in self.deck_weights:
            cur.execute("UPDATE progress SET weight = ?, seen_times = seen_times + 1, last_seen = ? WHERE question_id = ?",
                        (self.deck_weights[question_id], today, question_id))
        conn.commit()
        return True

    def update_statistics(self, quiz_id, user_id = None):
        if not self._progress_filename:
            self.select_test(quiz_id, user_id)
        conn, cur = self._connect_db()
        cur.execute("SELECT question_id, weight, seen_times, last_seen FROM progress")
        sum_weight = 0
        seen_count = 0
        learned_count = 0
        info = cur.fetchall()
        for row in info:
            sum_weight += row['weight']
            if row['last_seen'] > 0: seen_count += 1
            if row['weight'] < (self._max_weight / 3) and row['seen_times'] >= 2:
                learned_count += 1
                if row['learned'] == 0:
                    cur.execute("UPDATE progress SET learned = 1 WHERE question_id = ?", row['question_id'])
        conn.commit()
        seen_percentage = seen_count / len(info) * 100
        learned_percentage = learned_count / len(info) * 100
        self._progress_db.update_progress(quiz_id, learned_percentage, seen_percentage)