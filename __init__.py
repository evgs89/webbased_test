from modules.importer import TestQuestion
from modules.TestDatabase import TestDatabase
from modules.exporter import simpleExporter
import sys
import pickle


if __name__ == "__main__":
    fe = simpleExporter()
    with open('binary_output', 'rb') as _input:
        questions = pickle.load(_input)
        print(("Loaded {0} questions").format(len(questions)))
        db = TestDatabase('medical_quizz.db')
        db.save_to_db(questions, replace = True)
