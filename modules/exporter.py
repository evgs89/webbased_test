import os
import random
import sqlite3
import pickle
try: from .importer import TestQuestion
except ModuleNotFoundError: from modules.importer import TestQuestion


class simpleExporter:
    def __init__(self):
        self._marks = ['А','Б','В','Г']

    def _mix(self, length = 4):
        dec_counter = length
        sequence = []
        while dec_counter:
            dec_counter -= 1
            added = False
            while not added:
                rand = random.randint(0, length - 1)
                if rand not in sequence:
                    sequence.append(rand)
                    added = True
        return sequence

    def export(self, filename, questions):
        questions_text = ''
        questions_keys = ''
        for current_question in questions:
            sequence = self._mix(4)
            text = '  ' + current_question.number + '\n' + current_question.question + '\n\n'
            variants = ''
            key = ''
            for i in range(4):
                variants += '{mark} - {variant}\n'.format(mark = self._marks[i], variant = current_question.answers[sequence[i]][1])
                if current_question.answers[sequence[i]][0]: key = '{tag} - {mark}\n'.format(tag = current_question.number, mark = self._marks[i])
            questions_text += text + variants + '\n\n'
            questions_keys += key + '\n'
        with open(filename + '_test.txt', 'w') as test:
            test.write(questions_text)
        with open(filename + '_keys.txt', 'w') as keys:
            keys.write(questions_keys)


class TestDatabase:
    def __init__(self, filename):
        self._filename = filename

    def save_to_db(self, questions, replace = False):
        if not os.path.isfile(self._filename) or replace:
            try: os.remove(self._filename)
            except FileNotFoundError: pass
            conn = sqlite3.connect(self._filename)
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

    def load_from_db(self):
        conn = sqlite3.connect(self._filename)
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






