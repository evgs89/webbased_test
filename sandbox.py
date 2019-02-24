from modules.importer import TestQuestion, specialFileImporter
import sys
import pickle


if __name__ == "__main__":
    fi = specialFileImporter()
    questions = fi.open_file('test_questions.txt')
    with open('binary_output', 'wb') as output:
        pickle.dump(questions, output)
