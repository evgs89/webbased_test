import os
import sqlite3
import random
from numpy.random import choice
import datetime
from modules.userManager import UserManager
from modules.TestDatabase import TestDatabase
from modules.TestDatabase import ProgressDatabase
from collections import namedtuple

class UserNotAuthorized(Exception):
    pass


class Engine:
    def __init__(self):
        self._userManager = UserManager()
        self._test_db = TestDatabase()
        self._progress_db = ProgressDatabase(self._userManager)
        self._progress_filename = ''
        self._quiz_id = ''
        self._username = ''
        self._password = ''
        self._user_id = ''
        self._max_weight = 0
        self._init_weight = 0
        self.deck = {}
        self._current_question_id = ''
        self._current_question_keys = []
        self.exam = False
        self.deck_weights = {}
        self.correct_answers_to_quiz = []

    def _mix(self, length = 4):
        list = [i for i in range(length)]
        random.shuffle(list)
        return list

    def _calc_new_weight(self, weight, answer):
        if answer: new_weight = weight - 0.5 * (weight - 1)
        else: new_weight = weight + (self._max_weight - weight) * 0.5
        return new_weight

    def auth_user(self, username, password):
        self._user_id = self._userManager.valid_user(username, password)
        if self._user_id:
            self._username, self._password = username, password
            self.select_test(None)
        return self._user_id

    def get_available_tests(self):
        available_tests = self._test_db.get_available_tests()
        return available_tests  ## list of sqlite3.rows "SELECT quiz_id, name, description FROM quizzes"

    def select_test(self, quiz_id = None):
        assert self._user_id != ''
        if self._user_id and quiz_id:
            self._progress_db.select_test(self._user_id, quiz_id)
            self._max_weight, self._init_weight = self._progress_db.get_max_and_init_weights(quiz_id)
            self._quiz_id = quiz_id
            return True
        else:
            self._quiz_id = ''
            self._max_weight = 0
            self._init_weight = 0
            self.deck = {}
            self._current_question_id = ''
            self._current_question_keys = []
            self.exam = False
            self.deck_weights = {}
            self.correct_answers_to_quiz = []

    def get_progress(self):
        if self._quiz_id and self._user_id:
            a = self._progress_db.return_progress(self._user_id, self._quiz_id)
            return a

    def select_mode(self, quantity = 20, exam = False):
        assert(self._user_id != '')
        assert(self._quiz_id != '')
        self.correct_answers_to_quiz = []
        weight_list = self._progress_db.get_weights(self._user_id, self._quiz_id)
        # "SELECT question_id, weight, last_seen FROM progress"
        ids = [i[0] for i in weight_list]
        if quantity < len(ids): quantity = len(ids)
        weights = [float(i[1]) for i in weight_list]
        q = sum(weights)
        weights = [i/q for i in weights] ## костыль из-за перехода на numpy
        deck_ids = choice(a = ids, size = quantity, replace = False, p = weights)
        ## because I can't control replace parameter in standart (choices) implementation
        deck = self._test_db.get_questions(self._quiz_id, deck_ids) #dict {id: question_object}
        deck_weights = {}
        for i in weight_list:
            if i[0] in deck.keys(): deck_weights[i[0]] = float(i[1])
        assert(len(deck) == len(deck_weights))
        self.deck = deck
        self.exam = exam
        self.deck_weights = deck_weights
        return True

    def get_random_question_from_deck(self):
        if not self.deck: return None
        question = random.choice(list(self.deck.items()))[1]
        Question = namedtuple('Question', ['tag', 'question_text', 'question_picture', 'answers'])
        self._current_question_id = question.tag
        sequence = self._mix(len(question.answers))
        answers, key = [], []
        for i in range(4):
            answer = question.answers[sequence[i]]
            answers.append(answer[1])
            if answer[0]: key.append(i)
        self._current_question_keys = key
        q = Question(question.tag, question.question_text, question.question_picture, answers)
        return q

    def user_answered_question(self, question_id, selected = [], correct = False):
        if set(selected) == set(self._current_question_keys): correct = True
        self.deck_weights[question_id] = self._calc_new_weight(self.deck_weights[question_id], correct)
        if not correct: self.correct_answers_to_quiz.append(self.deck[question_id].get_correct_answers())
        if correct or self.exam: self.deck.pop(question_id)
        return (self.exam, correct, self._current_question_keys) # I don't want to save exam state on client side

    def test_finished(self):
        self._progress_db.update_individual_progress(self._user_id, self._quiz_id, self.deck_weights)
        return self.correct_answers_to_quiz
