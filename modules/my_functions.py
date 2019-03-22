import hashlib
import random, string

from modules.importer import TestQuestion


def id_generator(size = 12, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def hash_password(password):
    return hashlib.md5(bytes(password, encoding = 'utf8')).hexdigest()


def create_test_questions():
    questions = []
    for i in range(5):
        test_tag = i
        test_text = f"This is test question_text tag {i}"
        test_answers = [(True, 'Answer 1', None),
                        (False, 'Answer 2', None),
                        (False, 'Answer 3', None),
                        (True, 'Answer 4', None)]
        q = TestQuestion()
        q.tag = test_tag
        q.question_text = test_text
        q.answers = test_answers
        questions.append(q)
    return questions